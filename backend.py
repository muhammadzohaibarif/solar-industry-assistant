from flask import Flask, request, jsonify
import os

from chatbot import (
    chat_with_memory,
    create_new_conversation
)


# ============================================================
# SOLAR INDUSTRY CHATBOT BACKEND
# STEP 12B - WEB INTERFACE + MEMORY
# ============================================================

app = Flask(__name__)


# ============================================================
# CORS
# ============================================================

@app.after_request
def add_cors_headers(response):

    response.headers["Access-Control-Allow-Origin"] = "*"

    response.headers["Access-Control-Allow-Headers"] = (
        "Content-Type"
    )

    response.headers["Access-Control-Allow-Methods"] = (
        "GET, POST, OPTIONS"
    )

    return response


# ============================================================
# GLOBAL WEB CONVERSATION
# ============================================================

conversation_id = None


def get_conversation_id():

    global conversation_id

    if conversation_id is None:

        conversation_id = create_new_conversation(
            "Web Solar Assistant"
        )

    return conversation_id


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({

        "status": "online",

        "message":
            "Solar Industry Chatbot Backend is running",

        "service":
            "Solar Industry Assistant",

        "step":
            "12B - Web Interface + Memory"

    })


# ============================================================
# CREATE NEW CONVERSATION
# ============================================================

@app.route(
    "/conversation",
    methods=["POST"]
)
def new_conversation():

    global conversation_id

    try:

        conversation_id = create_new_conversation(
            "Web Solar Assistant"
        )

        return jsonify({

            "success": True,

            "conversation_id":
                conversation_id,

            "message":
                "New conversation created."

        })

    except Exception as error:

        return jsonify({

            "success": False,

            "error":
                str(error)

        }), 500


# ============================================================
# CHAT ENDPOINT
# ============================================================

@app.route(
    "/chat",
    methods=["POST", "OPTIONS"]
)
def chat():

    if request.method == "OPTIONS":

        return jsonify({
            "success": True
        })


    try:

        data = request.get_json()

        if not data:

            return jsonify({

                "success": False,

                "error":
                    "Request body is required."

            }), 400


        question = data.get(
            "question",
            ""
        ).strip()


        if not question:

            return jsonify({

                "success": False,

                "error":
                    "Question cannot be empty."

            }), 400


        # ----------------------------------------------------
        # Get current conversation
        # ----------------------------------------------------

        current_conversation_id = (
            get_conversation_id()
        )


        # ----------------------------------------------------
        # Chat with memory
        # ----------------------------------------------------

        answer = chat_with_memory(

            current_conversation_id,

            question

        )


        # ----------------------------------------------------
        # Return response
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "conversation_id":
                current_conversation_id,

            "question":
                question,

            "answer":
                answer

        })


    except Exception as error:

        return jsonify({

            "success": False,

            "error":
                str(error)

        }), 500


# ============================================================
# SERVER
# ============================================================

if __name__ == "__main__":

    print("=" * 70)

    print(
        "SOLAR INDUSTRY CHATBOT BACKEND"
    )

    print(
        "STEP 12B - WEB INTERFACE + MEMORY"
    )

    print("=" * 70)

    print(
        "Server: http://127.0.0.1:5000"
    )

    print(
        "Chat endpoint: POST /chat"
    )

    print(
        "New conversation: POST /conversation"
    )

    print("=" * 70)


    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )


    app.run(

        host="0.0.0.0",

        port=port,

        debug=False

    )