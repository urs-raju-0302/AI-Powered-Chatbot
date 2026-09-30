import re
from difflib import SequenceMatcher

FAQS = [
    {
        "intent": "greeting",
        "questions": ["hello", "hi", "hey", "good morning", "good evening"],
        "response": "Hello! How can I help you today?"
    },
    {
        "intent": "password_reset",
        "questions": [
            "forgot password",
            "reset password",
            "change password",
            "cannot login",
            "can't login",
            "lost my password"
        ],
        "response": "You can reset your password from the account settings page."
    },
    {
        "intent": "pricing",
        "questions": [
            "price",
            "pricing",
            "cost",
            "plans",
            "how much does it cost"
        ],
        "response": "Please visit the pricing section to view the latest plans and costs."
    },
    {
        "intent": "contact_support",
        "questions": [
            "contact support",
            "customer care",
            "contact you",
            "support team",
            "need help"
        ],
        "response": "You can contact our support team through the Contact Us section."
    },
    {
        "intent": "refund",
        "questions": [
            "refund",
            "get my money back",
            "return my payment",
            "cancel and refund"
        ],
        "response": "For a refund request, please contact support with your order or transaction details."
    },
    {
        "intent": "thanks",
        "questions": ["thanks", "thank you", "thankyou", "appreciate it"],
        "response": "You're welcome! Is there anything else I can help you with?"
    },
]


def clean(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s']", " ", text)
    return " ".join(text.split())


def similarity(a, b):
    return SequenceMatcher(None, clean(a), clean(b)).ratio()


def get_response(message):
    cleaned = clean(message)

    # Fast keyword/phrase matching
    best_intent = "unknown"
    best_response = "I'm sorry, I don't understand that yet. Try asking about passwords, pricing, refunds, or support."
    best_score = 0.0

    for faq in FAQS:
        for question in faq["questions"]:
            if question in cleaned:
                score = 0.95
            else:
                score = similarity(cleaned, question)

            if score > best_score:
                best_score = score
                best_intent = faq["intent"]
                best_response = faq["response"]

    # Avoid confidently answering unrelated questions.
    if best_score < 0.42:
        best_intent = "unknown"
        best_response = "I'm sorry, I don't understand that yet. Try asking about passwords, pricing, refunds, or support."

    return {
        "intent": best_intent,
        "confidence": round(best_score, 3),
        "response": best_response
    }
