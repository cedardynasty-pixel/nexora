import streamlit as st
from style import inject_css, hero, section_title
from auth import is_logged_in, is_admin, current_user
import db
import pdf_utils

inject_css()

if not is_logged_in() or not is_admin():
    st.warning("This page is for admins only.")
    st.stop()

hero("Admin Panel", "Manage student and admin accounts, the book library, and AI settings.")

tab_users, tab_books, tab_settings = st.tabs(["👥 Manage Users", "📖 Book Library", "⚙️ Settings"])

# ---------------- USERS TAB ----------------
with tab_users:
    section_title("All Accounts")
    users = db.get_all_users()
    me = current_user()

    for u in users:
        with st.container(border=True):
            cols = st.columns([2, 2, 1, 1, 1, 1])
            cols[0].markdown(f"**{u['username']}**" + (" 🛡️ admin" if u["is_admin"] else ""))
            cols[1].markdown(u["email"] or "—")
            cols[2].markdown(u["grade"] or "—")
            cols[3].markdown(u["created_at"][:10])

            if u["username"] == me:
                cols[4].markdown("_(you)_")
            else:
                if u["is_admin"]:
                    if cols[4].button("Remove admin", key=f"demote_{u['username']}"):
                        db.set_admin(u["username"], False)
                        st.rerun()
                else:
                    if cols[4].button("Make admin", key=f"promote_{u['username']}"):
                        db.set_admin(u["username"], True)
                        st.rerun()

                if cols[5].button("Delete", key=f"delete_{u['username']}"):
                    db.delete_user(u["username"])
                    st.rerun()

    st.divider()
    section_title("Create a New Admin Account")
    with st.form("create_admin_form"):
        new_username = st.text_input("Username")
        new_email = st.text_input("Email")
        new_password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Create Admin Account")
        if submitted:
            ok, message = db.create_user(
                new_username.strip(), new_email.strip(), new_password, "Staff", is_admin=True
            )
            if ok:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

    st.divider()
    section_title("Reset a Password")
    with st.form("reset_password_form"):
        target_username = st.selectbox("Account", [u["username"] for u in users])
        new_pw = st.text_input("New password", type="password")
        reset_submitted = st.form_submit_button("Reset Password")
        if reset_submitted:
            if len(new_pw) < 6:
                st.error("Password should be at least 6 characters.")
            else:
                db.set_password(target_username, new_pw)
                st.success(f"Password reset for {target_username}.")

# ---------------- BOOK LIBRARY TAB ----------------
with tab_books:
    section_title(
        "Book Library",
        "Create a book, then add its chapters one at a time. Students can generate notes, "
        "worksheets, study plans and flashcards grounded in a specific chapter or the whole book.",
    )

    # ---- Create a new book ----
    with st.expander("➕ Create a new book", expanded=False):
        with st.form("create_book_form"):
            new_book_title = st.text_input("Book title", placeholder="e.g. Grade 9 Science Textbook")
            create_book_submitted = st.form_submit_button("Create Book")
            if create_book_submitted:
                if not new_book_title.strip():
                    st.error("Please give the book a title.")
                else:
                    db.create_book(new_book_title.strip(), current_user())
                    st.success(f"Created '{new_book_title.strip()}'. Now add chapters to it below.")
                    st.rerun()

    st.divider()
    section_title("Books & Chapters")
    books = db.get_all_books()

    if not books:
        st.info("No books yet — create one above to get started.")
    else:
        for b in books:
            with st.container(border=True):
                st.markdown(f"### {b['title']}")
                st.caption(
                    f"{b['chapter_count']} chapter(s) · created {b['created_at'][:10]} "
                    f"by {b['created_by'] or '—'}"
                )

                chapters = db.get_chapters(b["id"])
                for ch in chapters:
                    ch_cols = st.columns([1, 4, 2, 1])
                    ch_cols[0].markdown(f"**Ch. {ch['order_index']}**")
                    ch_cols[1].markdown(ch["title"])
                    ch_cols[2].markdown(f"{ch['content_len']:,} characters")
                    if ch_cols[3].button("Delete", key=f"delete_chapter_{ch['id']}"):
                        db.delete_chapter(ch["id"])
                        st.rerun()

                # ---- Add a chapter to this book ----
                with st.expander(f"➕ Add a chapter to '{b['title']}'"):
                    chapter_source = st.radio(
                        "Chapter content source",
                        ["Upload PDF", "Paste text"],
                        key=f"source_{b['id']}",
                        horizontal=True,
                    )
                    with st.form(f"add_chapter_form_{b['id']}"):
                        chapter_title = st.text_input(
                            "Chapter title", key=f"chapter_title_{b['id']}",
                            placeholder="e.g. Chapter 3: Forces and Motion",
                        )
                        chapter_pdf = None
                        chapter_text = ""
                        if chapter_source == "Upload PDF":
                            chapter_pdf = st.file_uploader(
                                "Chapter PDF", type=["pdf"], key=f"chapter_pdf_{b['id']}"
                            )
                        else:
                            chapter_text = st.text_area(
                                "Chapter text", key=f"chapter_text_{b['id']}", height=200
                            )
                        add_chapter_submitted = st.form_submit_button("Add Chapter")

                        if add_chapter_submitted:
                            if not chapter_title.strip():
                                st.error("Please give the chapter a title.")
                            elif chapter_source == "Upload PDF" and chapter_pdf is None:
                                st.error("Please choose a PDF file.")
                            elif chapter_source == "Paste text" and not chapter_text.strip():
                                st.error("Please paste some text.")
                            else:
                                with st.spinner("Processing chapter..."):
                                    try:
                                        if chapter_source == "Upload PDF":
                                            content = pdf_utils.extract_text_from_pdf(chapter_pdf)
                                        else:
                                            content = chapter_text.strip()

                                        if not content.strip():
                                            st.error(
                                                "No extractable text found — if it's a PDF, it may "
                                                "be a scanned image without OCR."
                                            )
                                        else:
                                            db.add_chapter(
                                                b["id"], chapter_title.strip(), content, current_user()
                                            )
                                            st.success(f"Added '{chapter_title.strip()}'.")
                                            st.rerun()
                                    except Exception as e:
                                        st.error(f"Couldn't process that chapter: {e}")

                if st.button("Delete entire book", key=f"delete_book_{b['id']}"):
                    db.delete_book(b["id"])
                    st.rerun()

# ---------------- SETTINGS TAB ----------------
with tab_settings:
    section_title(
        "Gemini API Key",
        "Powers the student AI Study Tools (notes, worksheets, study plans, flashcards).",
    )
    current_key = db.get_setting("gemini_api_key") or ""
    masked = f"{'•' * max(len(current_key) - 4, 0)}{current_key[-4:]}" if current_key else "Not set"
    st.markdown(f"**Current key:** `{masked}`")

    with st.form("gemini_key_form"):
        new_key = st.text_input(
            "Gemini API key",
            type="password",
            placeholder="Paste your key from aistudio.google.com/apikey",
        )
        key_submitted = st.form_submit_button("Save Key")
        if key_submitted:
            if new_key.strip():
                db.set_setting("gemini_api_key", new_key.strip())
                st.success("Gemini API key saved.")
                st.rerun()
            else:
                st.error("Please paste a key before saving.")

    st.caption(
        "Get a free key at aistudio.google.com/apikey. The key is stored in the app's local "
        "database — on Streamlit Community Cloud this can reset if the app restarts, so you "
        "may need to re-enter it occasionally unless you move storage to a persistent database "
        "(see README)."
    )
