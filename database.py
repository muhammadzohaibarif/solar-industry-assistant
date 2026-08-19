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
# UPDATE CONVERSATION TITLE
# ============================================================

def update_conversation_title(
    conversation_id,
    title
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE conversations

        SET title = ?

        WHERE id = ?
        """,
        (
            title,
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
            conversation_id,
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
# GET CONVERSATIONS
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

    # --------------------------------------------------------
    # Delete messages belonging to conversation
    # --------------------------------------------------------

    cursor.execute(
        """
        DELETE FROM messages

        WHERE conversation_id = ?
        """,
        (
            conversation_id,
        )
    )

    # --------------------------------------------------------
    # Delete conversation
    # --------------------------------------------------------

    cursor.execute(
        """
        DELETE FROM conversations

        WHERE id = ?
        """,
        (
            conversation_id,
        )
    )

    deleted = (
        cursor.rowcount > 0
    )

    connection.commit()

    connection.close()

    return deleted


# ============================================================
# INITIALIZE DATABASE
# ============================================================

initialize_database()