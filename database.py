import sqlite3
from datetime import datetime


DATABASE_NAME = "solar_chat.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# CREATE TABLES
# ============================================================

def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    # --------------------------------------------------------
    # Conversations
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT,

            created_at TEXT NOT NULL,

            updated_at TEXT NOT NULL

        )
    """)

    # --------------------------------------------------------
    # Messages
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            conversation_id INTEGER NOT NULL,

            role TEXT NOT NULL,

            content TEXT NOT NULL,

            created_at TEXT NOT NULL,

            FOREIGN KEY (
                conversation_id
            )
            REFERENCES conversations(id)

        )
    """)

    connection.commit()

    connection.close()


# ============================================================
# CREATE CONVERSATION
# ============================================================

def create_conversation(
    title="Solar Conversation"
):

    connection = get_connection()

    cursor = connection.cursor()

    now = datetime.now().isoformat()

    cursor.execute(
        """
        INSERT INTO conversations
        (
            title,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?)
        """,
        (
            title,
            now,
            now
        )
    )

    conversation_id = cursor.lastrowid

    connection.commit()

    connection.close()

    return conversation_id


# ============================================================
# ADD MESSAGE
# ============================================================

def add_message(
    conversation_id,
    role,
    content
):

    connection = get_connection()

    cursor = connection.cursor()

    now = datetime.now().isoformat()

    cursor.execute(
        """
        INSERT INTO messages
        (
            conversation_id,
            role,
            content,
            created_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            conversation_id,
            role,
            content,
            now
        )
    )

    cursor.execute(
        """
        UPDATE conversations

        SET updated_at = ?

        WHERE id = ?
        """,
        (
            now,
            conversation_id
        )
    )

    connection.commit()

    connection.close()


# ============================================================
# GET CONVERSATION MESSAGES
# ============================================================

def get_messages(
    conversation_id
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            role,
            content,
            created_at

        FROM messages

        WHERE conversation_id = ?

        ORDER BY id ASC
        """,
        (
            conversation_id,
        )
    )

    messages = cursor.fetchall()

    connection.close()

    return messages


# ============================================================
# GET ALL CONVERSATIONS
# ============================================================

def get_conversations():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            title,
            created_at,
            updated_at

        FROM conversations

        ORDER BY updated_at DESC
        """
    )

    conversations = cursor.fetchall()

    connection.close()

    return conversations


# ============================================================
# DELETE CONVERSATION
# ============================================================

def delete_conversation(
    conversation_id
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM messages

        WHERE conversation_id = ?
        """,
        (
            conversation_id,
        )
    )

    cursor.execute(
        """
        DELETE FROM conversations

        WHERE id = ?
        """,
        (
            conversation_id,
        )
    )

    connection.commit()

    connection.close()


# ============================================================
# DATABASE TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)

    print(
        "SOLAR INDUSTRY CHATBOT"
    )

    print(
        "STEP 11A - DATABASE TEST"
    )

    print("=" * 70)

    initialize_database()

    conversation_id = create_conversation(
        "Solar Test Conversation"
    )

    add_message(
        conversation_id,
        "user",
        "I use 300 kWh per month."
    )

    add_message(
        conversation_id,
        "assistant",
        "Your estimated solar capacity is approximately 2.5 kW."
    )

    messages = get_messages(
        conversation_id
    )

    print(
        "\nCONVERSATION ID:"
    )

    print(
        conversation_id
    )

    print(
        "\nMESSAGES:"
    )

    print("-" * 70)

    for message in messages:

        print(
            f"{message['role'].upper()}: "
            f"{message['content']}"
        )

    print("-" * 70)

    conversations = get_conversations()

    print(
        "\nTOTAL CONVERSATIONS:"
    )

    print(
        len(conversations)
    )

    print("=" * 70)

    print(
        "STEP 11A TEST COMPLETED"
    )

    print("=" * 70)