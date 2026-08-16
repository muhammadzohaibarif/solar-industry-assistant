import streamlit as st
import requests


# ============================================================
# SOLAR INDUSTRY CHATBOT
# STEP 10B - WEB INTERFACE
# ============================================================

BACKEND_URL = "http://127.0.0.1:5000/chat"


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Solar Industry Assistant",
    page_icon="☀️",
    layout="centered"
)


# ============================================================
# HEADER
# ============================================================

st.title("☀️ Solar Industry Assistant")

st.caption(
    "AI-powered solar industry assistant "
    "for calculations, recommendations and "
    "solar knowledge."
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:

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
    # Display user question
    # --------------------------------------------------------

    st.session_state.messages.append({

        "role": "user",

        "content": question

    })


    with st.chat_message("user"):

        st.markdown(
            question
        )


    # --------------------------------------------------------
    # Send to backend
    # --------------------------------------------------------

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "Solar Assistant is thinking..."
        ):

            try:

                response = requests.post(

                    BACKEND_URL,

                    json={
                        "question": question
                    },

                    timeout=120

                )


                response.raise_for_status()

                data = response.json()


                if data.get(
                    "success",
                    True
                ):

                    answer = data.get(
                        "answer",
                        "No answer received."
                    )

                else:

                    answer = (
                        "Backend error: "
                        + data.get(
                            "error",
                            "Unknown error."
                        )
                    )


            except requests.exceptions.ConnectionError:

                answer = (
                    "❌ Could not connect to the "
                    "Solar Industry backend.\n\n"
                    "Make sure `backend.py` is running "
                    "on port 5000."
                )


            except requests.exceptions.Timeout:

                answer = (
                    "⏳ The request took too long. "
                    "Please try again."
                )


            except Exception as error:

                answer = (
                    f"❌ Error: {error}"
                )


        st.markdown(
            answer
        )


    # --------------------------------------------------------
    # Save assistant response
    # --------------------------------------------------------

    st.session_state.messages.append({

        "role": "assistant",

        "content": answer

    })


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header(
        "☀️ Solar Assistant"
    )

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


    st.divider()


    if st.button(
        "🗑️ Clear Conversation"
    ):

        st.session_state.messages = []

        st.rerun()