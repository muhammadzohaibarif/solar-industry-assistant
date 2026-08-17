from flask import Flask, request, jsonify
import os

from chatbot import (
    chat_with_memory,
    create_new_conversation
)

from database import (
    initialize_database,
    get_conversations,
    get_messages,
    delete_conversation
)


# ============================================================
# SOLAR INDUSTRY CHATBOT BACKEND
# STEP 17 - PERSISTENT CONVERSATION MANAGEMENT
# ============================================================

app = Flask(__name__)

initialize_database()


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
        "GET, POST, DELETE, OPTIONS"
    )

    return response


# ============================================================
# CURRENT WEB CONVERSATION
# ============================================================

conversation_id = None


def get_current_conversation_id():

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
            "17 - Persistent Conversation Management"

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

        data = request.get_json(
            silent=True
        ) or {}

        title = data.get(
            "title",
            "Web Solar Assistant"
        )

        title = str(title).strip()

        if not title:

            title = "Web Solar Assistant"

        conversation_id = create_new_conversation(
            title
        )

        return jsonify({

            "success": True,

            "conversation_id":
                conversation_id,

            "title":
                title,

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
# GET ALL CONVERSATIONS
# ============================================================

@app.route(
    "/conversations",
    methods=["GET"]
)
def conversations():

    try:

        conversation_list = get_conversations()

        result = []

        for conversation in conversation_list:

            result.append({

                "id":
                    conversation["id"],

                "title":
                    conversation["title"],

                "created_at":
                    conversation["created_at"],

                "updated_at":
                    conversation["updated_at"]

            })

        return jsonify({

            "success": True,

            "conversations":
                result

        })

    except Exception as error:

        return jsonify({

            "success": False,

            "error":
                str(error)

        }), 500


# ============================================================
# GET CONVERSATION MESSAGES
# ============================================================

@app.route(
    "/conversation/<int:conversation_id>",
    methods=["GET"]
)
def conversation_messages(
    conversation_id
):

    try:

        messages = get_messages(
            conversation_id
        )

        result = []

        for message in messages:

            result.append({

                "id":
                    message["id"],

                "role":
                    message["role"],

                "content":
                    message["content"],

                "created_at":
                    message["created_at"]

            })

        return jsonify({

            "success": True,

            "conversation_id":
                conversation_id,

            "messages":
                result

        })

    except Exception as error:

        return jsonify({

            "success": False,

            "error":
                str(error)

        }), 500


# ============================================================
# DELETE CONVERSATION
# ============================================================

@app.route(
    "/conversation/<int:conversation_to_delete>",
    methods=["DELETE"]
)
def remove_conversation(
    conversation_to_delete
):

    global conversation_id

    try:

        delete_conversation(
            conversation_to_delete
        )

        if conversation_id == conversation_to_delete:

            conversation_id = None

        return jsonify({

            "success": True,

            "conversation_id":
                conversation_to_delete,

            "message":
                "Conversation deleted."

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

    global conversation_id

    if request.method == "OPTIONS":

        return jsonify({
            "success": True
        })

    try:

        data = request.get_json(
            silent=True
        )

        if not data:

            return jsonify({

                "success": False,

                "error":
                    "Request body is required."

            }), 400


        question = str(
            data.get(
                "question",
                ""
            )
        ).strip()


        if not question:

            return jsonify({

                "success": False,

                "error":
                    "Question cannot be empty."

            }), 400


        requested_conversation_id = (
            data.get("conversation_id")
        )


        if requested_conversation_id is not None:

            try:

                requested_conversation_id = int(
                    requested_conversation_id
                )

            except (
                TypeError,
                ValueError
            ):

                return jsonify({

                    "success": False,

                    "error":
                        "conversation_id must be an integer."

                }), 400

            current_conversation_id = (
                requested_conversation_id
            )

            conversation_id = (
                current_conversation_id
            )

        else:

            current_conversation_id = (
                get_current_conversation_id()
            )


        answer = chat_with_memory(

            current_conversation_id,

            question

        )


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
        "STEP 17 - PERSISTENT CONVERSATION MANAGEMENT"
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

    print(
        "Conversations: GET /conversations"
    )

    print(
        "Conversation messages: "
        "GET /conversation/<id>"
    )

    print(
        "Delete conversation: "
        "DELETE /conversation/<id>"
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