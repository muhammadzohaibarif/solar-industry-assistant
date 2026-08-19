import os
import streamlit as st
import requests


# ============================================================
# SOLAR INDUSTRY CHATBOT
# STEP 17 - PERSISTENT CONVERSATION WEB INTERFACE
# ============================================================

BACKEND_BASE_URL = os.environ.get(
    "BACKEND_URL",
    "http://127.0.0.1:5000"
).rstrip("/")


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Solar Industry Assistant",
    page_icon="☀️",
    layout="centered"
)


# ============================================================
# SESSION STATE
# ============================================================

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversations" not in st.session_state:
    st.session_state.conversations = []


# ============================================================
# BACKEND FUNCTIONS
# ============================================================

def get_conversations():

    try:

        response = requests.get(
            f"{BACKEND_BASE_URL}/conversations",
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if data.get("success"):
            return data.get(
                "conversations",
                []
            )

    except Exception:
        return []

    return []


def create_conversation():

    try:

        response = requests.post(
            f"{BACKEND_BASE_URL}/conversation",
            json={
                "title": "New Solar Conversation"
            },
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if data.get("success"):

            return data.get(
                "conversation_id"
            )

    except Exception as error:

        st.error(
            f"Could not create conversation: {error}"
        )

    return None


def load_conversation(
    conversation_id
):

    try:

        response = requests.get(

            f"{BACKEND_BASE_URL}/conversation/"
            f"{conversation_id}",

            timeout=10

        )

        response.raise_for_status()

        data = response.json()

        if data.get("success"):

            return data.get(
                "messages",
                []
            )

    except Exception as error:

        st.error(
            f"Could not load conversation: {error}"
        )

    return []


def delete_conversation(
    conversation_id
):

    try:

        response = requests.delete(

            f"{BACKEND_BASE_URL}/conversation/"
            f"{conversation_id}",

            timeout=10

        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "success",
            False
        )

    except Exception as error:

        st.error(
            f"Could not delete conversation: {error}"
        )

    return False


def send_message(
    question,
    conversation_id
):

    try:

        response = requests.post(

            f"{BACKEND_BASE_URL}/chat",

            json={

                "question":
                    question,

                "conversation_id":
                    conversation_id

            },

            timeout=180

        )

        response.raise_for_status()

        data = response.json()

        if data.get("success"):

            return data.get(
                "answer",
                "No answer received."
            )

        return (
            "Backend error: "
            + data.get(
                "error",
                "Unknown error."
            )
        )

    except requests.exceptions.ConnectionError:

        return (
            "⚠️ Cannot connect to the backend. "
            "Please check the backend service."
        )

    except requests.exceptions.Timeout:

        return (
            "⏳ The request took too long. "
            "Please try again."
        )

    except Exception as error:

        return (
            f"⚠️ Error: {error}"
        )


# ============================================================
# LOAD CONVERSATIONS
# ============================================================

st.session_state.conversations = (
    get_conversations()
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("☀️ Solar Assistant")

    st.divider()


    # --------------------------------------------------------
    # NEW CHAT
    # --------------------------------------------------------

    if st.button(
        "➕ New Chat",
        use_container_width=True
    ):

        new_id = create_conversation()

        if new_id is not None:

            st.session_state.conversation_id = (
                new_id
            )

            st.session_state.messages = []

            st.rerun()


    st.divider()


    # --------------------------------------------------------
    # CONVERSATION HISTORY
    # --------------------------------------------------------

    st.subheader(
        "💬 Conversations"
    )


    if not st.session_state.conversations:

        st.caption(
            "No saved conversations yet."
        )

    else:

        for conversation in (
            st.session_state.conversations
        ):

            conversation_id = (
                conversation["id"]
            )

            title = (
                conversation["title"]
                or "Solar Conversation"
            )


            # ------------------------------------------------
            # SELECT CONVERSATION
            # ------------------------------------------------

            if st.button(

                title,

                key=f"conversation_{conversation_id}",

                use_container_width=True

            ):

                messages = load_conversation(
                    conversation_id
                )

                st.session_state.conversation_id = (
                    conversation_id
                )

                st.session_state.messages = [

                    {

                        "role":
                            message["role"],

                        "content":
                            message["content"]

                    }

                    for message in messages

                ]

                st.rerun()


            # ------------------------------------------------
            # DELETE CONVERSATION
            # ------------------------------------------------

            if st.button(

                "🗑️ Delete",

                key=f"delete_{conversation_id}",

                use_container_width=True

            ):

                deleted = delete_conversation(
                    conversation_id
                )

                if deleted:

                    if (
                        st.session_state.conversation_id
                        == conversation_id
                    ):

                        st.session_state.conversation_id = (
                            None
                        )

                        st.session_state.messages = []

                    st.rerun()


    st.divider()


    # --------------------------------------------------------
    # CLEAR CURRENT CHAT
    # --------------------------------------------------------

    if st.button(
        "🧹 Clear Current Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# ============================================================
# HEADER
# ============================================================

st.title(
    "☀️ Solar Industry Assistant"
)

st.caption(
    "AI-powered solar industry assistant "
    "for calculations, recommendations and "
    "solar knowledge."
)


# ============================================================
# CREATE INITIAL CONVERSATION
# ============================================================

if st.session_state.conversation_id is None:

    new_id = create_conversation()

    if new_id is not None:

        st.session_state.conversation_id = (
            new_id
        )

        st.session_state.messages = []


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask a solar question..."
)


# ============================================================
# PROCESS QUESTION
# ============================================================

if question:

    # --------------------------------------------------------
    # USER MESSAGE
    # --------------------------------------------------------

    st.session_state.messages.append({

        "role":
            "user",

        "content":
            question

    })


    with st.chat_message("user"):

        st.markdown(
            question
        )


    # --------------------------------------------------------
    # ASSISTANT RESPONSE
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Solar Assistant is thinking..."
        ):

            answer = send_message(

                question,

                st.session_state.conversation_id

            )


        st.markdown(
            answer
        )


    # --------------------------------------------------------
    # SAVE RESPONSE IN UI
    # --------------------------------------------------------

    st.session_state.messages.append({

        "role":
            "assistant",

        "content":
            answer

    })


    st.rerun()


# ============================================================
# INFORMATION SECTION
# ============================================================

with st.expander(
    "ℹ️ About Solar Assistant"
):

    st.write(
        "Your AI assistant for solar "
        "industry questions."
    )

    st.divider()

    st.subheader(
        "Available Features"
    )

    st.write(
        "✅ Solar panel calculations"
    )

    st.write(
        "✅ Battery sizing"
    )

    st.write(
        "✅ Inverter sizing"
    )

    st.write(
        "✅ System recommendations"
    )

    st.write(
        "✅ Energy consumption"
    )

    st.write(
        "✅ Solar knowledge base"
    )

    st.write(
        "✅ RAG-powered answers"
    )

    st.write(
        "✅ Persistent conversation history"
    )

    st.write(
        "✅ Multiple saved conversations"
    )