const form = document.getElementById("chat-form");
const input = document.getElementById("message-input");
const messages = document.getElementById("messages");

function addMessage(text, type, meta = "") {
    const box = document.createElement("div");
    box.className = `message ${type}`;

    const label = document.createElement("span");
    label.className = "label";
    label.textContent = type === "user" ? "You" : "Bot";

    const p = document.createElement("p");
    p.textContent = text;

    box.appendChild(label);
    box.appendChild(p);

    if (meta) {
        const small = document.createElement("small");
        small.textContent = meta;
        small.style.opacity = "0.65";
        box.appendChild(small);
    }

    messages.appendChild(box);
    messages.scrollTop = messages.scrollHeight;
}

async function sendMessage(message) {
    addMessage(message, "user");
    input.value = "";

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Request failed");
        }

        const confidence = Math.round(data.confidence * 100);
        addMessage(
            data.response,
            "bot",
            `Intent: ${data.intent} • Confidence: ${confidence}%`
        );
    } catch (error) {
        addMessage("Something went wrong. Please try again.", "bot");
        console.error(error);
    }
}

form.addEventListener("submit", (event) => {
    event.preventDefault();
    const message = input.value.trim();
    if (message) sendMessage(message);
});

document.querySelectorAll(".quick-actions button").forEach(button => {
    button.addEventListener("click", () => {
        sendMessage(button.dataset.message);
    });
});
