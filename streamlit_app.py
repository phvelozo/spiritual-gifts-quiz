import json
import os
from datetime import datetime

import streamlit as st

from test import QuizScorer, gift_names, gifts, questions

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

# Configure page
st.set_page_config(
    page_title="Teste de Dons Espirituais", page_icon="🎁", layout="centered"
)

# Initialize session state
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "scorer" not in st.session_state:
    st.session_state.scorer = None
if "current_question" not in st.session_state:
    st.session_state.current_question = 1
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False


def save_progress_web(name, scorer, filename="quiz_progress.json"):
    """Save user progress to Firebase or JSON file as fallback."""
    progress_data = {
        "answers": scorer.answers,
        "scores": scorer.scores,
        "last_updated": datetime.now().isoformat(),
        "completed": len(scorer.answers) == 45,
    }

    # Try Firebase first
    if FIREBASE_ENABLED and db:
        try:
            # Convert integer keys to strings for Firestore compatibility
            firebase_data = {
                "answers": {str(k): v for k, v in scorer.answers.items()},
                "scores": scorer.scores,
                "last_updated": datetime.now().isoformat(),
                "completed": len(scorer.answers) == 45,
            }
            db.collection("quiz_progress").document(name).set(firebase_data)
            print(f"✅ Progress saved to Firebase for {name}")
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

    data[name] = progress_data

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_progress_web(name, filename="quiz_progress.json"):
    """Load user progress from Firebase or JSON file as fallback."""
    # Try Firebase first
    if FIREBASE_ENABLED and db:
        try:
            doc = db.collection("quiz_progress").document(name).get()
            if doc.exists:
                data = doc.to_dict()
                # Convert string keys back to integers for answers
                if "answers" in data and isinstance(data["answers"], dict):
                    data["answers"] = {int(k): v for k, v in data["answers"].items()}
                print(f"✅ Progress loaded from Firebase for {name}")
                return data
        except Exception as e:
            print(f"⚠️ Firebase load failed: {e}, falling back to JSON")

    # Fallback to JSON file
    if not os.path.exists(filename):
        return None

    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get(name)
    except (json.JSONDecodeError, IOError):
        return None


# Header
st.title("🎁 Teste de Dons Espirituais")
st.markdown("---")

# Step 1: Get user name
if st.session_state.user_name is None:
    st.subheader("Bem-vindo!")

    with st.form("name_form"):
        user_name = st.text_input("Por favor, digite seu nome:", key="name_input")
        submit = st.form_submit_button("Começar")

        if submit and user_name.strip():
            st.session_state.user_name = user_name.strip()
            st.session_state.scorer = QuizScorer(gifts)

            # Check for existing progress
            saved_progress = load_progress_web(user_name)
            if saved_progress and not saved_progress.get("completed", False):
                st.session_state.has_progress = True
                st.session_state.saved_progress = saved_progress
            elif saved_progress and saved_progress.get("completed", False):
                st.session_state.has_completed = True

            st.rerun()

# Step 2: Handle existing progress
elif not st.session_state.quiz_started:
    st.write(f"### Olá, {st.session_state.user_name}! 👋")

    if hasattr(st.session_state, "has_progress") and st.session_state.has_progress:
        num_answered = len(st.session_state.saved_progress["answers"])
        st.info(
            f"📋 Encontramos um questionário em andamento!\n\nVocê respondeu {num_answered} de 45 perguntas."
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Continuar de onde parei", use_container_width=True):
                # Load previous answers
                st.session_state.scorer.answers = {
                    int(k): v
                    for k, v in st.session_state.saved_progress["answers"].items()
                }
                st.session_state.scorer.scores = st.session_state.saved_progress[
                    "scores"
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
            if st.button("🔄 Começar novo questionário", use_container_width=True):
                st.session_state.scorer = QuizScorer(gifts)
                st.session_state.current_question = 1
                st.session_state.quiz_started = True
                st.rerun()

    elif hasattr(st.session_state, "has_completed") and st.session_state.has_completed:
        st.success("✅ Você já completou este questionário anteriormente!")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refazer questionário", use_container_width=True):
                st.session_state.scorer = QuizScorer(gifts)
                st.session_state.current_question = 1
                st.session_state.quiz_started = True
                st.rerun()
        with col2:
            if st.button("👋 Sair"):
                st.session_state.clear()
                st.rerun()

    else:
        st.info("Pronto para começar o questionário!")
        if st.button("▶️ Iniciar Questionário", use_container_width=True):
            st.session_state.quiz_started = True
            st.rerun()

# Step 3: Quiz questions
elif st.session_state.current_question <= 45:
    q_num = st.session_state.current_question

    # Progress bar
    progress = (q_num - 1) / 45
    st.progress(progress, text=f"Progresso: {q_num - 1}/45 perguntas respondidas")

    st.markdown("---")

    # Question
    st.subheader(f"Pergunta {q_num} de 45")
    st.write(questions[q_num])

    # Show previous answer if exists
    if q_num in st.session_state.scorer.answers:
        prev_answer = st.session_state.scorer.answers[q_num]
        st.caption(f"Resposta anterior: {prev_answer}")

    st.markdown("---")

    # Answer options
    st.write("**Escolha uma opção:**")

    answer = st.radio(
        "Sua resposta:",
        options=[3, 2, 1, 0],
        format_func=lambda x: {
            3: "3 - Descreve-me de forma correta",
            2: "2 - É uma tendência minha",
            1: "1 - Tenho pequena inclinação para isto",
            0: "0 - Não tem nada a ver comigo",
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
            if st.button("⬅️ Voltar", use_container_width=True):
                st.session_state.current_question -= 1
                st.rerun()

    with col2:
        if st.button("💾 Salvar e Sair", use_container_width=True):
            save_progress_web(st.session_state.user_name, st.session_state.scorer)
            st.success("✅ Progresso salvo!")
            st.info("Você pode continuar mais tarde.")
            if st.button("OK"):
                st.session_state.clear()
                st.rerun()

    with col3:
        if answer is not None:
            if st.button("Próxima ➡️", use_container_width=True, type="primary"):
                # Save answer
                st.session_state.scorer.answer_question(q_num, answer)
                save_progress_web(st.session_state.user_name, st.session_state.scorer)
                st.session_state.current_question += 1
                st.rerun()

# Step 4: Show results
else:
    st.balloons()
    st.success("🎉 Questionário Completo!")

    st.markdown("---")

    st.subheader(f"📊 Resultados de {st.session_state.user_name}")

    # Get results
    ranked_results = st.session_state.scorer.get_ranked_results()

    # Show top 3
    st.markdown("### 🏆 Seus Principais Dons Espirituais:")

    top_3 = st.session_state.scorer.get_top_n_gifts(3)

    medals = ["🥇", "🥈", "🥉"]
    for i, (gift, score) in enumerate(top_3):
        gift_name = gift_names.get(gift, gift)
        st.metric(
            label=f"{medals[i]} {i + 1}º lugar: {gift_name}", value=f"{score} pontos"
        )

    st.markdown("---")

    # Show all results
    with st.expander("📈 Ver todos os resultados"):
        for rank, (gift, score) in enumerate(ranked_results, 1):
            gift_name = gift_names.get(gift, gift)
            st.write(f"{rank}. **{gift_name}** ({gift}): {score} pontos")
            st.progress(score / 15)  # Max score is 15

    st.markdown("---")

    if st.button("🔄 Fazer novo teste"):
        st.session_state.clear()
        st.rerun()
