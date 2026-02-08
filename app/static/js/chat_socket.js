const socket = io();

let currentRoom = "Introductions";
let username = "Guest";
const roomMessages = {};

document.addEventListener("DOMContentLoaded", () => {
    const el = document.getElementById("username");
    if (el) username = el.textContent.trim();

    document.querySelectorAll(".room-item").forEach(item => {
        if (item.textContent.trim() === currentRoom) {
            item.classList.add("active-room");
        }
    });
});

// ---------------- SOCKET EVENTS ----------------

socket.on("connect", () => {
    joinRoom(currentRoom);
});

socket.on("message", (data) => {
    addMessage(
        data.from,
        data.msg,
        data.from === username ? "own" : "other"
    );
});

socket.on("private_message", (data) => {
    addMessage(
        data.from,
        `[Private] ${data.msg}`,
        "private"
    );
});

socket.on("active_users", (data) => {
    const usersList = document.getElementById("active-users");
    if (!usersList) return;

    usersList.innerHTML = "";
    data.users.forEach(user => {
        const div = document.createElement("div");
        div.className = "user-item";
        div.textContent = user === username ? `${user} (you)` : user;
        div.onclick = () => insertPrivateMessage(user);
        usersList.appendChild(div);
    });
});

socket.on("status", (data) => {
    addMessage("System", data.msg, "system");
});

// ---------------- HELPERS ----------------

function renderMessage(sender, message, type) {
    const chat = document.getElementById("chat");
    if (!chat) return;

    const msgDiv = document.createElement("div");
    msgDiv.className = `message ${type}`;
    msgDiv.textContent = `${sender}: ${message}`;
    chat.appendChild(msgDiv);
    chat.scrollTop = chat.scrollHeight;
}

function addMessage(sender, message, type) {
    if (!roomMessages[currentRoom]) {
        roomMessages[currentRoom] = [];
    }
    roomMessages[currentRoom].push({ sender, message, type });
    renderMessage(sender, message, type);
}

function sendMessage() {
    const input = document.getElementById("message");
    const message = input.value.trim();
    if (!message) return;

    if (message.startsWith("@")) {
        const [target, ...rest] = message.substring(1).split(" ");
        const privateMsg = rest.join(" ");
        if (privateMsg) {
            socket.emit("message", {
                type: "private_message",
                target,
                msg: privateMsg,
            });
        }
    } else {
        socket.emit("message", {
            room: currentRoom,
            msg: message,
        });
    }

    input.value = "";
    input.focus();
}

function joinRoom(room) {
    socket.emit("leave", { room: currentRoom });
    currentRoom = room;
    socket.emit("join", { room });

    const chat = document.getElementById("chat");
    if (!chat) return;

    chat.innerHTML = "";
    (roomMessages[room] || []).forEach(m =>
        renderMessage(m.sender, m.message, m.type)
    );
}

function insertPrivateMessage(user) {
    const input = document.getElementById("message");
    input.value = `@${user} `;
    input.focus();
}

function handleKeyPress(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}
