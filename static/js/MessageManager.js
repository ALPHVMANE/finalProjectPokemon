export class MessageManager {
    constructor() {
        this.messagesDiv = document.getElementById('messages');
    }

    updateMessages(messages) {
        if (!messages) return;
        this.messagesDiv.innerHTML = messages
            .map(msg => `<div class="message">${msg}</div>`)
            .join('');
        this.messagesDiv.scrollTop = this.messagesDiv.scrollHeight;
    }
}