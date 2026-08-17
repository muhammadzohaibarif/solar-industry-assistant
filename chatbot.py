import requests
import re
import os

from solar_tools import (
    solar_size_tool,
    battery_size_tool,
    backup_time_tool,
    inverter_size_tool,
    system_type_tool,
)

from knowledge_retriever import build_context

from database import (
    initialize_database,
    create_conversation,
    add_message,
    get_messages,
)


# ============================================================
# SOLAR INDUSTRY CHATBOT
# STEP 16 - LOCAL OLLAMA + CLOUD GROQ DEPLOYMENT
# ============================================================

LLM_PROVIDER = os.getenv(
    "LLM_PROVIDER",
    "groq"
).lower()

# ============================================================
# OLLAMA CONFIGURATION
# ============================================================

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/chat"
)

MODEL = os.getenv(
    "MODEL",
    "llama3.2:latest"
)

# ============================================================
# GROQ CONFIGURATION
# ============================================================

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY",
    ""
)

GROQ_URL = (
    "https://api.groq.com/openai/v1/chat/completions"
)

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
)


# ============================================================
# NUMBER EXTRACTION
# ============================================================

def extract_numbers(text):

    numbers = []

    matches = re.findall(
        r"\d+(?:\.\d+)?",
        text
    )

    for match in matches:

        try:
            numbers.append(float(match))

        except ValueError:
            pass

    return numbers


# ============================================================
# OLLAMA
# ============================================================

def ask_ollama(
    question,
    knowledge_context="",
    conversation_context=""
):

    system_prompt = (
        "You are a professional Solar Industry Assistant. "

        "You answer questions about solar panels, inverters, "
        "batteries, solar systems, energy consumption, "
        "installation, maintenance, warranty, pricing concepts "
        "and customer support. "

        "Use the provided knowledge-base information when "
        "relevant. "

        "Use previous conversation information when it is "
        "relevant to the current question. "

        "Do not invent technical facts when relevant "
        "knowledge-base information is available. "

        "Do not provide unsupported exact specifications, "
        "prices, lifespans, voltage ranges, cycle counts, "
        "or performance figures unless supported by the "
        "knowledge base or a calculation tool. "

        "Give clear, concise and customer-friendly answers."
    )

    if conversation_context:

        system_prompt += (
            "\n\nPREVIOUS CONVERSATION:\n"
            f"{conversation_context}"
        )

    if knowledge_context:

        system_prompt += (
            "\n\nKNOWLEDGE BASE:\n"
            f"{knowledge_context}"
        )

    payload = {

        "model": MODEL,

        "messages": [

            {
                "role": "system",
                "content": system_prompt
            },

            {
                "role": "user",
                "content": question
            }

        ],

        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=180
    )

    response.raise_for_status()

    data = response.json()

    return data["message"]["content"]


# ============================================================
# GROQ
# ============================================================

def ask_groq(
    question,
    knowledge_context="",
    conversation_context=""
):

    if not GROQ_API_KEY:

        raise RuntimeError(
            "GROQ_API_KEY is not configured."
        )

    system_prompt = (
        "You are a professional Solar Industry Assistant. "

        "You answer questions about solar panels, inverters, "
        "batteries, solar systems, energy consumption, "
        "installation, maintenance, warranty, pricing concepts "
        "and customer support. "

        "Use the provided knowledge-base information when "
        "relevant. "

        "Use previous conversation information when it is "
        "relevant to the current question. "

        "Do not invent technical facts when relevant "
        "knowledge-base information is available. "

        "Do not provide unsupported exact specifications, "
        "prices, lifespans, voltage ranges, cycle counts, "
        "or performance figures unless supported by the "
        "knowledge base or a calculation tool. "

        "Give clear, concise and customer-friendly answers."
    )

    if conversation_context:

        system_prompt += (
            "\n\nPREVIOUS CONVERSATION:\n"
            f"{conversation_context}"
        )

    if knowledge_context:

        system_prompt += (
            "\n\nKNOWLEDGE BASE:\n"
            f"{knowledge_context}"
        )

    headers = {

        "Authorization":
            f"Bearer {GROQ_API_KEY}",

        "Content-Type":
            "application/json"

    }

    payload = {

        "model": GROQ_MODEL,

        "messages": [

            {
                "role": "system",
                "content": system_prompt
            },

            {
                "role": "user",
                "content": question
            }

        ],

        "temperature": 0.2,

        "stream": False

    }

    response = requests.post(

        GROQ_URL,

        headers=headers,

        json=payload,

        timeout=180

    )

    response.raise_for_status()

    data = response.json()

    return (
        data["choices"][0]["message"]["content"]
    )


# ============================================================
# SOLAR SIZE
# ============================================================

def handle_solar_size(
    question,
    previous_messages=None
):

    numbers = extract_numbers(
        question
    )

    question_text = question.lower()

    consumption_keywords = [

        "kwh",
        "monthly consumption",
        "electricity consumption",
        "monthly electricity",
        "electricity usage",
        "energy consumption",
        "energy usage",
        "use per month",
        "uses per month",
        "consume per month",
        "consumes per month",
        "consumption per month"

    ]

    current_has_consumption = any(

        keyword in question_text

        for keyword in consumption_keywords

    )

    if (
        not current_has_consumption
        and previous_messages
    ):

        for message in reversed(
            previous_messages
        ):

            if message["role"] != "user":
                continue

            previous_text = (
                message["content"]
                .lower()
                .strip()
            )

            if (
                "battery" in previous_text
                or "backup" in previous_text
                or "inverter" in previous_text
            ):
                continue

            previous_has_consumption = any(

                keyword in previous_text

                for keyword in consumption_keywords

            )

            if not previous_has_consumption:
                continue

            previous_numbers = extract_numbers(
                previous_text
            )

            if previous_numbers:

                numbers = [
                    previous_numbers[0]
                ]

                break

    if not numbers:

        return (
            "Please provide your monthly electricity "
            "consumption in kWh.\n\n"
            "Example: I use 300 kWh per month."
        )

    monthly_consumption = numbers[0]

    panel_wattage = 550

    current_numbers = extract_numbers(
        question
    )

    for number in current_numbers:

        if (
            100 <= number <= 1000
            and number != monthly_consumption
        ):

            panel_wattage = int(
                number
            )

            break

    result = solar_size_tool(
        monthly_consumption,
        panel_wattage
    )

    return (
        "\nSOLAR CALCULATION RESULT\n"
        "----------------------------------------\n"
        f"Monthly Consumption: "
        f"{result['monthly_consumption_kwh']} kWh\n"
        f"Daily Consumption: "
        f"{result['daily_consumption_kwh']} kWh\n"
        f"Estimated Solar Capacity: "
        f"{result['solar_capacity_kw']} kW\n"
        f"Panel Wattage: "
        f"{result['panel_wattage_w']} W\n"
        f"Estimated Number of Panels: "
        f"{result['panel_count']}\n"
        f"Actual Panel Capacity: "
        f"{result['actual_panel_capacity_kw']} kW\n"
        "----------------------------------------\n\n"
        "Note: This is an estimated system size. "
        "Final sizing should be verified by a qualified "
        "solar professional based on site conditions, "
        "loads, equipment specifications and local "
        "requirements."
    )


# ============================================================
# BATTERY SIZE
# ============================================================

def handle_battery_size(
    question,
    previous_messages=None
):

    numbers = extract_numbers(
        question
    )

    if len(numbers) < 2 and previous_messages:

        for message in reversed(
            previous_messages
        ):

            if message["role"] != "user":
                continue

            previous_text = (
                message["content"]
                .lower()
            )

            if (
                "battery" not in previous_text
                and "backup" not in previous_text
            ):
                continue

            previous_numbers = extract_numbers(
                previous_text
            )

            if len(previous_numbers) >= 2:

                numbers = previous_numbers

                break

    if len(numbers) < 2:

        return (
            "Please provide the backup load in kW "
            "and required backup time in hours."
        )

    backup_load = numbers[0]
    backup_hours = numbers[1]

    result = battery_size_tool(
        backup_load,
        backup_hours
    )

    return (
        "\nBATTERY CALCULATION RESULT\n"
        "----------------------------------------\n"
        f"Backup Load: "
        f"{result['backup_load_kw']} kW\n"
        f"Required Backup Time: "
        f"{result['backup_hours']} hours\n"
        f"Estimated Battery Capacity: "
        f"{result['battery_capacity_kwh']} kWh\n"
        "----------------------------------------"
    )


# ============================================================
# BACKUP TIME
# ============================================================

def handle_backup_time(
    question,
    previous_messages=None
):

    numbers = extract_numbers(
        question
    )

    if len(numbers) < 2 and previous_messages:

        for message in reversed(
            previous_messages
        ):

            if message["role"] != "user":
                continue

            previous_text = (
                message["content"]
                .lower()
            )

            if (
                "battery" not in previous_text
                and "backup" not in previous_text
            ):
                continue

            previous_numbers = extract_numbers(
                previous_text
            )

            if len(previous_numbers) >= 2:

                numbers = previous_numbers

                break

    if len(numbers) < 2:

        return (
            "Please provide battery capacity "
            "and load in kW."
        )

    battery_capacity = numbers[0]
    load = numbers[1]

    result = backup_time_tool(
        battery_capacity,
        load
    )

    return (
        "\nBATTERY BACKUP RESULT\n"
        "----------------------------------------\n"
        f"Battery Capacity: "
        f"{result['battery_capacity_kwh']} kWh\n"
        f"Load: "
        f"{result['load_kw']} kW\n"
        f"Estimated Backup Time: "
        f"{result['backup_hours']} hours\n"
        "----------------------------------------"
    )


# ============================================================
# INVERTER SIZE
# ============================================================

def handle_inverter_size(
    question,
    previous_messages=None
):

    numbers = extract_numbers(
        question
    )

    if not numbers and previous_messages:

        for message in reversed(
            previous_messages
        ):

            if message["role"] != "user":
                continue

            previous_text = (
                message["content"]
                .lower()
            )

            if (
                "load" not in previous_text
                and "kw" not in previous_text
                and "inverter" not in previous_text
            ):
                continue

            previous_numbers = extract_numbers(
                previous_text
            )

            if previous_numbers:

                numbers = previous_numbers

                break

    if not numbers:

        return (
            "Please provide your peak electrical "
            "load in kW."
        )

    peak_load = numbers[0]

    result = inverter_size_tool(
        peak_load
    )

    return (
        "\nINVERTER CALCULATION RESULT\n"
        "----------------------------------------\n"
        f"Peak Load: "
        f"{result['peak_load_kw']} kW\n"
        f"Calculated Inverter Requirement: "
        f"{result['required_inverter_kw']} kW\n"
        f"Recommended Inverter Size: "
        f"{result['recommended_inverter_kw']} kW\n"
        "----------------------------------------"
    )


# ============================================================
# SYSTEM TYPE
# ============================================================

def handle_system_type(
    question
):

    text = question.lower().strip()

    grid_available = True

    unavailable_keywords = [

        "no grid",
        "without grid",
        "grid unavailable",
        "grid is unavailable",
        "no electricity grid",
        "grid is not available",
        "grid not available",
        "no electricity connection",
        "no grid connection"

    ]

    if any(
        keyword in text
        for keyword in unavailable_keywords
    ):

        grid_available = False

    grid_reliable = True

    unreliable_keywords = [

        "unreliable",
        "not reliable",
        "isn't reliable",
        "is not reliable",
        "frequent outage",
        "frequent outages",
        "power cut",
        "power cuts",
        "load shedding",
        "power outage",
        "power outages"

    ]

    if any(
        keyword in text
        for keyword in unreliable_keywords
    ):

        grid_reliable = False

    no_backup_keywords = [

        "don't need backup",
        "do not need backup",
        "dont need backup",
        "no backup",
        "backup is not required",
        "backup not required",
        "backup isn't required",
        "backup is unnecessary",
        "without backup",

        "don't need battery backup",
        "do not need battery backup",
        "dont need battery backup",
        "no battery backup",
        "battery backup is not required",
        "battery backup not required",

        "don't need battery",
        "do not need battery",
        "dont need battery",
        "no battery",
        "battery is not required",
        "battery not required",
        "battery isn't required"

    ]

    no_backup_required = any(
        keyword in text
        for keyword in no_backup_keywords
    )

    backup_required = False

    backup_keywords = [

        "backup",
        "backup power",
        "backup electricity",
        "power backup",
        "backup required",
        "need backup",
        "need battery backup"

    ]

    if any(
        keyword in text
        for keyword in backup_keywords
    ):

        backup_required = True

    if no_backup_required:

        backup_required = False

    battery_required = False

    battery_keywords = [

        "battery",
        "battery storage",
        "energy storage",
        "need battery",
        "battery required"

    ]

    if any(
        keyword in text
        for keyword in battery_keywords
    ):

        battery_required = True

    if no_backup_required:

        battery_required = False

    if backup_required:

        battery_required = True

    result = system_type_tool(

        grid_available=grid_available,

        grid_reliable=grid_reliable,

        backup_required=backup_required,

        battery_required=battery_required

    )

    return (
        "\nSYSTEM RECOMMENDATION\n"
        "----------------------------------------\n"
        f"Grid Available: "
        f"{'Yes' if grid_available else 'No'}\n"
        f"Grid Reliable: "
        f"{'Yes' if grid_reliable else 'No'}\n"
        f"Backup Required: "
        f"{'Yes' if backup_required else 'No'}\n"
        f"Battery Required: "
        f"{'Yes' if battery_required else 'No'}\n\n"
        f"Recommended System: "
        f"{result['system_type']}\n"
        f"Reason: "
        f"{result['reason']}\n"
        "----------------------------------------\n\n"
        "Note: Final system selection should be confirmed "
        "by a qualified solar professional after evaluating "
        "site conditions, electrical loads, grid conditions "
        "and applicable requirements."
    )


# ============================================================
# TOOL DETECTION
# ============================================================

def detect_tool(
    question
):

    text = question.lower().strip()

    information_phrases = [

        "what is",
        "what are",
        "what does",
        "what do",
        "what's",
        "explain",
        "define",
        "meaning of",
        "difference between",
        "how does",
        "how do",
        "why is",
        "why are",
        "tell me about",
        "information about"

    ]

    is_information_question = any(

        phrase in text

        for phrase in information_phrases

    )

    if is_information_question:

        return None

    if (

        "on-grid" in text
        or "off-grid" in text
        or "hybrid" in text
        or "on grid" in text
        or "off grid" in text
        or "system type" in text
        or "which system" in text
        or "what system" in text

        or (

            "grid" in text

            and (

                "backup" in text
                or "unreliable" in text
                or "outage" in text
                or "outages" in text
                or "load shedding" in text
                or "power cut" in text
                or "no electricity" in text
                or "not available" in text

            )

        )

    ):

        return "system"

    if (

        "battery" in text

        and (

            "size" in text
            or "capacity" in text
            or "need" in text
            or "how much" in text
            or "require" in text
            or "required" in text

        )

    ):

        return "battery"

    if (

        (

            "how long" in text
            or "backup time" in text
            or "last" in text
            or "hours" in text

        )

        and (

            "battery" in text
            or "battery capacity" in text

        )

    ):

        return "backup"

    if (

        "inverter" in text

        and (

            "size" in text
            or "capacity" in text
            or "need" in text
            or "require" in text
            or "required" in text

        )

    ):

        return "inverter"

    if (

        "solar size" in text
        or "solar capacity" in text
        or "solar system size" in text
        or "solar requirement" in text
        or "how many solar panels" in text
        or "how many panels" in text
        or "number of solar panels" in text
        or "number of panels" in text

        or (

            "solar panels" in text

            and (

                "need" in text
                or "require" in text
                or "how much" in text

            )

        )

    ):

        return "solar"

    return None


# ============================================================
# MAIN CHAT ENGINE
# ============================================================

def solar_chat(
    question,
    previous_messages=None
):

    if previous_messages is None:

        previous_messages = []

    tool = detect_tool(
        question
    )

    try:

        if tool == "solar":

            return handle_solar_size(
                question,
                previous_messages
            )

        if tool == "battery":

            return handle_battery_size(
                question,
                previous_messages
            )

        if tool == "backup":

            return handle_backup_time(
                question,
                previous_messages
            )

        if tool == "inverter":

            return handle_inverter_size(
                question,
                previous_messages
            )

        if tool == "system":

            return handle_system_type(
                question
            )

        knowledge_context = build_context(
            question,
            top_k=3
        )

        conversation_context = ""

        for message in previous_messages:

            conversation_context += (

                f"{message['role'].upper()}: "

                f"{message['content']}\n"

            )

        if LLM_PROVIDER == "groq":

            return ask_groq(
                question,
                knowledge_context,
                conversation_context
            )

        return ask_ollama(
            question,
            knowledge_context,
            conversation_context
        )

    except requests.exceptions.RequestException as error:

        return (
            f"Connection error: {error}"
        )

    except Exception as error:

        return (
            f"Error: {error}"
        )


# ============================================================
# MEMORY CHAT
# ============================================================

def create_new_conversation(
    title="Solar Conversation"
):

    initialize_database()

    return create_conversation(
        title
    )


def chat_with_memory(
    conversation_id,
    question
):

    previous_messages = get_messages(
        conversation_id
    )

    add_message(
        conversation_id,
        "user",
        question
    )

    answer = solar_chat(
        question,
        previous_messages
    )

    add_message(
        conversation_id,
        "assistant",
        answer
    )

    return answer


# ============================================================
# TERMINAL TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)

    print(
        "SOLAR INDUSTRY CHATBOT"
    )

    print(
        "STEP 16 - LOCAL OLLAMA + CLOUD GROQ"
    )

    print(
        f"LLM Provider: {LLM_PROVIDER}"
    )

    if LLM_PROVIDER == "groq":

        print(
            f"Groq Model: {GROQ_MODEL}"
        )

    else:

        print(
            f"Ollama Model: {MODEL}"
        )

    print("=" * 70)

    initialize_database()

    conversation_id = create_new_conversation(
        "Solar Memory Test"
    )

    print(
        f"\nConversation ID: "
        f"{conversation_id}"
    )

    question1 = input(
        "\nUser: "
    )

    answer1 = chat_with_memory(
        conversation_id,
        question1
    )

    print(
        "\nSolar Assistant:"
    )

    print(
        answer1
    )

    question2 = input(
        "\nUser: "
    )

    answer2 = chat_with_memory(
        conversation_id,
        question2
    )

    print(
        "\nSolar Assistant:"
    )

    print(
        answer2
    )

    print(
        "\n" + "=" * 70
    )

    print(
        "SAVED CONVERSATION"
    )

    print(
        "=" * 70
    )

    messages = get_messages(
        conversation_id
    )

    for message in messages:

        print(
            f"\n{message['role'].upper()}:"
        )

        print(
            message["content"]
        )

    print(
        "\n" + "=" * 70
    )

    print(
        "STEP 16 TEST COMPLETED"
    )

    print(
        "=" * 70
    )
