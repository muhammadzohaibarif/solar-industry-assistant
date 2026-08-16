
import os
import re


KNOWLEDGE_BASE_DIR = "knowledge_base"


# ============================================================
# TOPIC KEYWORDS
# ============================================================

TOPIC_KEYWORDS = {

    "batteries.txt": [
        "battery",
        "batteries",
        "lead acid",
        "lead-acid",
        "lithium",
        "lithium-ion",
        "depth of discharge",
        "backup",
        "cycle life",
    ],

    "panels.txt": [
        "panel",
        "panels",
        "photovoltaic",
        "pv",
        "solar panel",
        "watt",
        "wattage",
    ],

    "inverters.txt": [
        "inverter",
        "inverters",
        "mppt",
        "conversion",
        "ac",
        "dc",
    ],

    "systems.txt": [
        "on-grid",
        "off-grid",
        "hybrid",
        "grid",
        "system type",
    ],

    "energy_consumption.txt": [
        "energy consumption",
        "electricity consumption",
        "kwh",
        "units",
        "appliance",
        "load",
        "peak load",
    ],

    "sizing.txt": [
        "sizing",
        "system size",
        "solar size",
        "capacity",
        "calculate",
        "required",
    ],

    "installation.txt": [
        "installation",
        "install",
        "roof",
        "mounting",
        "wiring",
        "commissioning",
    ],

    "maintenance.txt": [
        "maintenance",
        "cleaning",
        "service",
        "inspection",
        "maintenance schedule",
    ],

    "pricing.txt": [
        "price",
        "pricing",
        "cost",
        "expensive",
        "budget",
        "quotation",
    ],

    "warranty.txt": [
        "warranty",
        "guarantee",
        "claim",
        "coverage",
    ],

    "faq.txt": [
        "faq",
        "question",
        "common",
        "customer",
    ],
}


# ============================================================
# STOP WORDS
# ============================================================

STOP_WORDS = {
    "the",
    "a",
    "an",
    "is",
    "are",
    "was",
    "were",
    "what",
    "why",
    "how",
    "can",
    "could",
    "would",
    "should",
    "do",
    "does",
    "did",
    "i",
    "we",
    "you",
    "my",
    "your",
    "for",
    "to",
    "of",
    "in",
    "on",
    "and",
    "or",
    "with",
    "about",
    "tell",
    "me",
    "please",
    "between",
}


# ============================================================
# LOAD DOCUMENTS
# ============================================================

def load_documents():

    documents = []

    if not os.path.exists(KNOWLEDGE_BASE_DIR):

        raise FileNotFoundError(
            f"Knowledge base folder not found: "
            f"{KNOWLEDGE_BASE_DIR}"
        )

    for filename in os.listdir(
        KNOWLEDGE_BASE_DIR
    ):

        if not filename.lower().endswith(
            ".txt"
        ):
            continue

        filepath = os.path.join(
            KNOWLEDGE_BASE_DIR,
            filename
        )

        try:

            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as file:

                content = file.read().strip()

            if not content:
                continue

            documents.append({
                "filename": filename,
                "content": content
            })

        except Exception as error:

            print(
                f"Warning: Could not read "
                f"{filename}: {error}"
            )

    return documents


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text):

    text = text.lower()

    text = text.replace(
        "-",
        " "
    )

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# EXTRACT KEYWORDS
# ============================================================

def extract_keywords(text):

    words = normalize_text(
        text
    ).split()

    keywords = []

    for word in words:

        if word in STOP_WORDS:
            continue

        if len(word) < 2:
            continue

        keywords.append(word)

    return keywords


# ============================================================
# SCORE DOCUMENT
# ============================================================

def score_document(
    query,
    document
):

    query_normalized = normalize_text(
        query
    )

    query_keywords = extract_keywords(
        query
    )

    document_text = normalize_text(
        document["content"]
    )

    filename = document[
        "filename"
    ].lower()

    score = 0


    # --------------------------------------------------------
    # Normal keyword matching
    # --------------------------------------------------------

    for keyword in query_keywords:

        occurrences = document_text.count(
            keyword
        )

        score += min(
            occurrences,
            5
        )


    # --------------------------------------------------------
    # Filename matching
    # --------------------------------------------------------

    for keyword in query_keywords:

        if keyword in filename:

            score += 5


    # --------------------------------------------------------
    # Topic boosting
    # --------------------------------------------------------

    topic_keywords = TOPIC_KEYWORDS.get(
        filename,
        []
    )

    for topic_keyword in topic_keywords:

        normalized_topic = normalize_text(
            topic_keyword
        )

        if normalized_topic in query_normalized:

            score += 15


    return score


# ============================================================
# RETRIEVE DOCUMENTS
# ============================================================

def retrieve_documents(
    query,
    top_k=3
):

    documents = load_documents()

    scored_documents = []


    for document in documents:

        score = score_document(
            query,
            document
        )

        if score > 0:

            scored_documents.append(
                (
                    score,
                    document
                )
            )


    scored_documents.sort(
        key=lambda item: item[0],
        reverse=True
    )


    return [

        {
            "filename": document[
                "filename"
            ],

            "content": document[
                "content"
            ],

            "score": score
        }

        for score, document
        in scored_documents[:top_k]

    ]


# ============================================================
# BUILD CONTEXT
# ============================================================

def build_context(
    query,
    top_k=3
):

    results = retrieve_documents(
        query,
        top_k
    )


    if not results:

        return (
            "No directly relevant information "
            "was found in the solar knowledge base."
        )


    context_parts = []


    for result in results:

        context_parts.append(

            "\n"
            f"--- SOURCE: {result['filename']} ---\n"
            f"{result['content']}\n"

        )


    return "\n".join(
        context_parts
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)

    print(
        "SOLAR KNOWLEDGE RETRIEVER"
    )

    print(
        "STEP 9 - IMPROVED RAG TEST"
    )

    print("=" * 70)


    question = input(
        "\nEnter a solar question: "
    )


    results = retrieve_documents(
        question,
        top_k=3
    )


    print(
        "\nRELEVANT DOCUMENTS"
    )

    print(
        "-" * 70
    )


    if not results:

        print(
            "No relevant documents found."
        )

    else:

        for result in results:

            print(
                f"{result['filename']} "
                f"(score: {result['score']})"
            )


    print(
        "\nRETRIEVED CONTEXT"
    )

    print(
        "-" * 70
    )


    print(
        build_context(
            question,
            top_k=3
        )
    )


    print(
        "\n" + "=" * 70
    )

    print(
        "STEP 9 RAG TEST COMPLETED"
    )

    print(
        "=" * 70
    )