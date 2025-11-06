import json
import os
import re
import unicodedata
from datetime import datetime

import streamlit as st

from test import QuizScorer, gifts
from translations import LANGUAGES, get_gift_name, get_question, get_translations

# Firebase setup
try:
    import firebase_admin
    from firebase_admin import credentials, firestore

    # Initialize Firebase (only once)
    if not firebase_admin._apps:
        # Try to get credentials from Streamlit secrets
        if "firebase" in st.secrets:
            # Convert secrets to proper dict format for Firebase
            # Explicitly convert to string to ensure compatibility
            cred_dict = {
                "type": str(st.secrets["firebase"]["type"]),
                "project_id": str(st.secrets["firebase"]["project_id"]),
                "private_key_id": str(st.secrets["firebase"]["private_key_id"]),
                "private_key": str(st.secrets["firebase"]["private_key"]),
                "client_email": str(st.secrets["firebase"]["client_email"]),
                "client_id": str(st.secrets["firebase"]["client_id"]),
                "auth_uri": str(st.secrets["firebase"]["auth_uri"]),
                "token_uri": str(st.secrets["firebase"]["token_uri"]),
                "auth_provider_x509_cert_url": str(
                    st.secrets["firebase"]["auth_provider_x509_cert_url"]
                ),
                "client_x509_cert_url": str(
                    st.secrets["firebase"]["client_x509_cert_url"]
                ),
            }
            # Add optional fields if present
            if "universe_domain" in st.secrets["firebase"]:
                cred_dict["universe_domain"] = str(
                    st.secrets["firebase"]["universe_domain"]
                )

            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            FIREBASE_ENABLED = True
            print("✅ Firebase initialized successfully!")
        else:
            FIREBASE_ENABLED = False
            db = None
            print("ℹ️ Firebase secrets not configured, using JSON fallback")
    else:
        db = firestore.client()
        FIREBASE_ENABLED = True
except Exception as e:
    FIREBASE_ENABLED = False
    db = None
    print(f"⚠️ Firebase initialization failed: {e}")
    import traceback

    traceback.print_exc()

# Initialize session state
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "church_name" not in st.session_state:
    st.session_state.church_name = None
if "scorer" not in st.session_state:
    st.session_state.scorer = None
if "current_question" not in st.session_state:
    st.session_state.current_question = 1
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "language" not in st.session_state:
    st.session_state.language = "pt"  # Default to Portuguese

# Get current language translations
translations = get_translations(st.session_state.language)
ui = translations["ui"]

# Configure page
st.set_page_config(page_title=ui["page_title"], page_icon="🎁", layout="centered")

# Language selector in sidebar
with st.sidebar:
    st.header("🌐 " + ui["language"])
    lang_options = list(LANGUAGES.keys())
    current_index = (
        lang_options.index(st.session_state.language)
        if st.session_state.language in lang_options
        else 0
    )
    selected_language = st.selectbox(
        ui["language"],
        options=lang_options,
        format_func=lambda x: LANGUAGES[x],
        key="language_selector",
        index=current_index,
    )

    # Update language if changed
    if selected_language != st.session_state.language:
        st.session_state.language = selected_language
        translations = get_translations(st.session_state.language)
        ui = translations["ui"]
        st.rerun()


def normalize_username_key(name):
    """
    Normalize username to create a safe, consistent key for storage.

    This function:
    - Converts to lowercase for case-insensitive matching
    - Removes/replaces special characters that could cause issues
    - Handles Unicode characters (accents, etc.)
    - Replaces spaces with underscores
    - Removes leading/trailing whitespace

    Args:
        name: Original username string

    Returns:
        Normalized key string safe for use as document ID or JSON key
    """
    if not name:
        return ""

    # Normalize Unicode characters (e.g., "Maíra" -> "Maira")
    name = unicodedata.normalize("NFKD", name)

    # Convert to lowercase
    name = name.lower()

    # Replace spaces with underscores
    name = name.replace(" ", "_")

    # Remove or replace special characters, keep only alphanumeric and underscores
    # This ensures Firebase document ID compatibility
    name = re.sub(r"[^a-z0-9_-]", "", name)

    # Remove multiple consecutive underscores
    name = re.sub(r"_+", "_", name)

    # Remove leading/trailing underscores
    name = name.strip("_")

    # Ensure it's not empty (fallback to 'user' if somehow empty)
    if not name:
        name = "user"

    return name


def save_progress_web(name, scorer, church_name=None, filename="quiz_progress.json"):
    """
    Save user progress to Firebase or JSON file as fallback.

    Uses normalized username as key for consistency and safety.
    Stores original display name in the data for backward compatibility.
    """
    # Normalize the username to create a safe key
    normalized_key = normalize_username_key(name)

    progress_data = {
        "display_name": name,  # Store original name for display
        "answers": scorer.answers,
        "scores": scorer.scores,
        "last_updated": datetime.now().isoformat(),
        "completed": len(scorer.answers) == 45,
    }

    # Add church name if provided
    if church_name:
        progress_data["church_name"] = church_name

    # Try Firebase first
    if FIREBASE_ENABLED and db:
        try:
            # Convert integer keys to strings for Firestore compatibility
            firebase_data = {
                "display_name": name,  # Store original name for display
                "answers": {str(k): v for k, v in scorer.answers.items()},
                "scores": scorer.scores,
                "last_updated": datetime.now().isoformat(),
                "completed": len(scorer.answers) == 45,
            }
            if church_name:
                firebase_data["church_name"] = church_name

            # Check if old document exists with original name (for migration)
            if name != normalized_key:
                old_doc = db.collection("quiz_progress").document(name).get()
                if old_doc.exists:
                    # Migrate: delete old document after saving new one
                    print(
                        f"🔄 Migrating Firebase data from '{name}' to '{normalized_key}'"
                    )
                    # Delete old document
                    db.collection("quiz_progress").document(name).delete()
                    print(f"🗑️  Deleted old Firebase document '{name}'")

            # Use normalized key as document ID
            db.collection("quiz_progress").document(normalized_key).set(firebase_data)
            print(f"✅ Progress saved to Firebase for {name} (key: {normalized_key})")
            return
        except Exception as e:
            print(f"⚠️ Firebase save failed: {e}, falling back to JSON")

    # Fallback to JSON file
    data = {}
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            data = {}

    # Use normalized key, but also check for backward compatibility
    # If old key exists, migrate it
    if name in data and name != normalized_key:
        # Migrate old data to new normalized key
        old_data = data.pop(name)
        if "display_name" not in old_data:
            old_data["display_name"] = name
        data[normalized_key] = old_data
        print(f"🔄 Migrated data from '{name}' to '{normalized_key}'")

    data[normalized_key] = progress_data

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_progress_web(name, filename="quiz_progress.json"):
    """
    Load user progress from Firebase or JSON file as fallback.

    Tries normalized key first, then falls back to original name for backward compatibility.
    """
    # Normalize the username to create a safe key
    normalized_key = normalize_username_key(name)

    # Try Firebase first
    if FIREBASE_ENABLED and db:
        try:
            # Try normalized key first
            doc = db.collection("quiz_progress").document(normalized_key).get()
            if doc.exists:
                data = doc.to_dict()
                # Convert string keys back to integers for answers
                if "answers" in data and isinstance(data["answers"], dict):
                    data["answers"] = {int(k): v for k, v in data["answers"].items()}
                print(
                    f"✅ Progress loaded from Firebase for {name} (key: {normalized_key})"
                )
                return data
            # Fallback: try original name for backward compatibility
            if name != normalized_key:
                doc = db.collection("quiz_progress").document(name).get()
                if doc.exists:
                    data = doc.to_dict()
                    if "answers" in data and isinstance(data["answers"], dict):
                        data["answers"] = {
                            int(k): v for k, v in data["answers"].items()
                        }
                    print(f"✅ Progress loaded from Firebase for {name} (legacy key)")
                    return data
        except Exception as e:
            print(f"⚠️ Firebase load failed: {e}, falling back to JSON")

    # Fallback to JSON file
    if not os.path.exists(filename):
        return None

    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Try normalized key first
            if normalized_key in data:
                return data[normalized_key]
            # Fallback: try original name for backward compatibility
            if name in data:
                return data[name]
            return None
    except (json.JSONDecodeError, IOError):
        return None


def get_churches_list(filename="churches.json"):
    """Get list of all churches from Firebase or JSON file as fallback."""
    # Try Firebase first
    if FIREBASE_ENABLED and db:
        try:
            churches_ref = db.collection("churches")
            docs = churches_ref.stream()
            churches = []
            for doc in docs:
                data = doc.to_dict()
                # Get the name field, or use doc.id as fallback
                church_name = data.get("name", doc.id) if data else doc.id
                churches.append(church_name)
            print(f"✅ Loaded {len(churches)} churches from Firebase")
            return sorted(churches) if churches else []
        except Exception as e:
            print(f"⚠️ Firebase load failed: {e}, falling back to JSON")

    # Fallback to JSON file
    if not os.path.exists(filename):
        return []

    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            churches = data.get("churches", [])
            return sorted(churches) if churches else []
    except (json.JSONDecodeError, IOError):
        return []


def add_church(church_name, filename="churches.json"):
    """Add a new church to the list in Firebase or JSON file as fallback."""
    church_name = church_name.strip()
    if not church_name:
        return False

    # Try Firebase first
    if FIREBASE_ENABLED and db:
        try:
            # Use church name as document ID (normalized)
            doc_id = church_name.lower().strip()
            db.collection("churches").document(doc_id).set(
                {"name": church_name, "created_at": datetime.now().isoformat()}
            )
            print(f"✅ Church '{church_name}' added to Firebase")
            return True
        except Exception as e:
            print(f"⚠️ Firebase save failed: {e}, falling back to JSON")

    # Fallback to JSON file
    data = {"churches": []}
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            data = {"churches": []}

    # Add church if not already present
    if church_name not in data.get("churches", []):
        if "churches" not in data:
            data["churches"] = []
        data["churches"].append(church_name)
        data["churches"] = sorted(
            list(set(data["churches"]))
        )  # Remove duplicates and sort

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ Church '{church_name}' added to JSON")
        return True

    return False


# Header
st.title(f"🎁 {ui['page_title']}")
st.markdown("---")

# Step 1: Get user name
if st.session_state.user_name is None:
    st.subheader(ui["welcome"])

    with st.form("name_form"):
        user_name = st.text_input(ui["enter_name"], key="name_input")
        submit = st.form_submit_button(ui["start"])

        if submit and user_name.strip():
            st.session_state.user_name = user_name.strip()
            st.session_state.scorer = QuizScorer(gifts)
            # Check for existing progress and load church if available
            saved_progress = load_progress_web(user_name)
            if saved_progress:
                if "church_name" in saved_progress:
                    st.session_state.church_name = saved_progress["church_name"]
                # Set progress flags
                if not saved_progress.get("completed", False):
                    st.session_state.has_progress = True
                    st.session_state.saved_progress = saved_progress
                else:
                    st.session_state.has_completed = True
            st.rerun()

# Step 2: Get church selection
elif st.session_state.church_name is None:
    st.write(f"### {ui['hello'].format(st.session_state.user_name)}")
    st.subheader(ui["select_church"])

    # Get list of existing churches
    churches_list = get_churches_list()

    # Create options list with "Add new" option
    ADD_NEW_OPTION = "➕ " + ui["add_new_church"]
    church_options = (
        churches_list + [ADD_NEW_OPTION] if churches_list else [ADD_NEW_OPTION]
    )

    selected_option = st.selectbox(
        ui["church_name"], options=church_options, key="church_select"
    )

    # Show text input if "Add new" is selected
    new_church_name = None
    if selected_option == ADD_NEW_OPTION:
        new_church_name = st.text_input(ui["enter_church_name"], key="new_church_input")

    if st.button(ui["start"], type="primary"):
        if selected_option != ADD_NEW_OPTION:
            # User selected an existing church
            st.session_state.church_name = selected_option
            # Check for existing progress
            saved_progress = load_progress_web(st.session_state.user_name)
            if saved_progress and not saved_progress.get("completed", False):
                st.session_state.has_progress = True
                st.session_state.saved_progress = saved_progress
                # Use church from saved progress if available, otherwise keep selected
                if "church_name" in saved_progress:
                    st.session_state.church_name = saved_progress["church_name"]
            elif saved_progress and saved_progress.get("completed", False):
                st.session_state.has_completed = True
                if "church_name" in saved_progress:
                    st.session_state.church_name = saved_progress["church_name"]
            st.rerun()
        elif new_church_name and new_church_name.strip():
            # User wants to add a new church
            church_name = new_church_name.strip()
            if add_church(church_name):
                st.session_state.church_name = church_name
                st.success(ui["church_added"])
                # Check for existing progress
                saved_progress = load_progress_web(st.session_state.user_name)
                if saved_progress and not saved_progress.get("completed", False):
                    st.session_state.has_progress = True
                    st.session_state.saved_progress = saved_progress
                    # Use church from saved progress if available
                    if "church_name" in saved_progress:
                        st.session_state.church_name = saved_progress["church_name"]
                elif saved_progress and saved_progress.get("completed", False):
                    st.session_state.has_completed = True
                    if "church_name" in saved_progress:
                        st.session_state.church_name = saved_progress["church_name"]
                st.rerun()
            else:
                # Translation for warning - using a simple approach
                warning_msg = {
                    "pt": "Por favor, digite um nome válido para a igreja.",
                    "es": "Por favor, ingrese un nombre válido para la iglesia.",
                    "en": "Please enter a valid church name.",
                }
                st.warning(
                    warning_msg.get(st.session_state.language, warning_msg["en"])
                )

# Step 3: Handle existing progress
elif not st.session_state.quiz_started:
    st.write(f"### {ui['hello'].format(st.session_state.user_name)}")

    if hasattr(st.session_state, "has_progress") and st.session_state.has_progress:
        num_answered = len(st.session_state.saved_progress["answers"])
        st.info(ui["progress_found"].format(num_answered))

        col1, col2 = st.columns(2)
        with col1:
            if st.button(ui["continue"], use_container_width=True):
                # Load previous answers
                st.session_state.scorer.answers = {
                    int(k): v
                    for k, v in st.session_state.saved_progress["answers"].items()
                }
                st.session_state.scorer.scores = st.session_state.saved_progress[
                    "scores"
                ]
                # Load church name if available
                if "church_name" in st.session_state.saved_progress:
                    st.session_state.church_name = st.session_state.saved_progress[
                        "church_name"
                    ]
                st.session_state.current_question = (
                    max(
                        int(k)
                        for k in st.session_state.saved_progress["answers"].keys()
                    )
                    + 1
                )
                st.session_state.quiz_started = True
                st.rerun()

        with col2:
            if st.button(ui["start_new"], use_container_width=True):
                st.session_state.scorer = QuizScorer(gifts)
                st.session_state.current_question = 1
                st.session_state.quiz_started = True
                st.rerun()

    elif hasattr(st.session_state, "has_completed") and st.session_state.has_completed:
        st.success(ui["already_completed"])

        col1, col2 = st.columns(2)
        with col1:
            if st.button(ui["retake"], use_container_width=True):
                st.session_state.scorer = QuizScorer(gifts)
                st.session_state.current_question = 1
                st.session_state.quiz_started = True
                st.rerun()
        with col2:
            if st.button(ui["exit"]):
                st.session_state.clear()
                st.rerun()

    else:
        st.info(ui["ready_to_start"])
        if st.button(ui["start_quiz"], use_container_width=True):
            st.session_state.quiz_started = True
            st.rerun()

# Step 3: Quiz questions
elif st.session_state.current_question <= 45:
    q_num = st.session_state.current_question

    # Progress bar
    progress = (q_num - 1) / 45
    st.progress(progress, text=ui["progress"].format(q_num - 1))

    st.markdown("---")

    # Question
    st.subheader(ui["question"].format(q_num))
    st.write(get_question(q_num, st.session_state.language))

    # Show previous answer if exists
    if q_num in st.session_state.scorer.answers:
        prev_answer = st.session_state.scorer.answers[q_num]
        st.caption(ui["previous_answer"].format(prev_answer))

    st.markdown("---")

    # Answer options
    st.write(ui["choose_option"])

    answer = st.radio(
        ui["your_answer"],
        options=[3, 2, 1, 0],
        format_func=lambda x: {
            3: ui["answer_3"],
            2: ui["answer_2"],
            1: ui["answer_1"],
            0: ui["answer_0"],
        }[x],
        key=f"q_{q_num}",
        index=None
        if q_num not in st.session_state.scorer.answers
        else [3, 2, 1, 0].index(st.session_state.scorer.answers[q_num]),
    )

    st.markdown("---")

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if q_num > 1:
            if st.button(ui["back"], use_container_width=True):
                st.session_state.current_question -= 1
                st.rerun()

    with col2:
        if st.button(ui["save_exit"], use_container_width=True):
            save_progress_web(
                st.session_state.user_name,
                st.session_state.scorer,
                st.session_state.church_name,
            )
            st.success(ui["progress_saved"])
            st.info(ui["continue_later"])
            if st.button(ui["ok"]):
                st.session_state.clear()
                st.rerun()

    with col3:
        if answer is not None:
            if st.button(ui["next"], use_container_width=True, type="primary"):
                # Save answer
                st.session_state.scorer.answer_question(q_num, answer)
                save_progress_web(
                    st.session_state.user_name,
                    st.session_state.scorer,
                    st.session_state.church_name,
                )
                st.session_state.current_question += 1
                st.rerun()

# Step 4: Show results
else:
    st.balloons()
    st.success(ui["quiz_complete"])

    st.markdown("---")

    st.subheader(ui["results"].format(st.session_state.user_name))

    # Get results
    ranked_results = st.session_state.scorer.get_ranked_results()

    # Show top 3
    st.markdown(f"### {ui['top_gifts']}")

    top_3 = st.session_state.scorer.get_top_n_gifts(3)

    medals = ["🥇", "🥈", "🥉"]
    for i, (gift, score) in enumerate(top_3):
        gift_name = get_gift_name(gift, st.session_state.language)
        # Format place text based on language
        if st.session_state.language == "en":
            place_suffix = {0: "st", 1: "nd", 2: "rd"}.get(i, "th")
            place_text = f"{medals[i]} {i + 1}{place_suffix} place: {gift_name}"
        else:
            place_text = f"{medals[i]} {i + 1}º lugar: {gift_name}"
        st.metric(label=place_text, value=ui["points"].format(score))

    st.markdown("---")

    # Show all results
    with st.expander(ui["view_all"]):
        for rank, (gift, score) in enumerate(ranked_results, 1):
            gift_name = get_gift_name(gift, st.session_state.language)
            st.write(f"{rank}. **{gift_name}** ({gift}): {ui['points'].format(score)}")
            st.progress(score / 15)  # Max score is 15

    st.markdown("---")

    if st.button(ui["new_test"]):
        st.session_state.clear()
        st.rerun()
