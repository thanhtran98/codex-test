(() => {
  const launcher = document.querySelector('#chat-launcher');
  const panel = document.querySelector('#chat-panel');
  const input = document.querySelector('#chat-input');
  const form = document.querySelector('#chat-form');
  const messages = document.querySelector('#chat-messages');
  const status = document.querySelector('#chat-status');
  const send = document.querySelector('#chat-send');
  const reset = document.querySelector('#chat-reset');
  const welcome = messages.firstElementChild.cloneNode(true);
  let history = [];
  let pending = false;

  function setOpen(open) {
    panel.hidden = !open;
    launcher.setAttribute('aria-expanded', String(open));
    (open ? input : launcher).focus();
  }

  function appendMessage(role, content) {
    const bubble = document.createElement('p');
    bubble.className = `chat-message chat-${role}`;
    bubble.textContent = content;
    messages.append(bubble);
    messages.scrollTop = messages.scrollHeight;
    return bubble;
  }

  launcher.addEventListener('click', () => setOpen(panel.hidden));
  document.querySelector('#chat-close').addEventListener('click', () => setOpen(false));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && !panel.hidden) setOpen(false);
  });
  input.addEventListener('keydown', event => {
    if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) {
      event.preventDefault();
      form.requestSubmit();
    }
  });
  reset.addEventListener('click', () => {
    if (pending) return;
    history = [];
    messages.replaceChildren(welcome.cloneNode(true));
    status.textContent = '';
    input.value = '';
    input.focus();
  });
  form.addEventListener('submit', async event => {
    event.preventDefault();
    const content = input.value.trim();
    if (!content || pending) return;
    pending = true;
    send.disabled = reset.disabled = true;
    input.readOnly = true;
    status.textContent = 'Đắk Lắk Ơi đang trả lời…';
    const bubble = appendMessage('user', content);
    input.value = '';
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 50000);
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: [...history.slice(-10), { role: 'user', content }] }),
        signal: controller.signal,
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(data.error || 'Chưa kết nối được trợ lý. Hãy chạy website cùng máy chủ API.');
      if (typeof data.reply !== 'string' || !data.reply.trim()) throw new Error('Trợ lý chưa có câu trả lời. Vui lòng thử lại.');
      appendMessage('assistant', data.reply);
      history = [...history.slice(-10), { role: 'user', content }, { role: 'assistant', content: data.reply.slice(0, 4000) }];
      status.textContent = '';
    } catch (error) {
      bubble.remove();
      input.value = content;
      status.textContent = error.name === 'AbortError' ? 'Kết nối quá lâu. Bạn có thể gửi lại câu hỏi.' : error.message;
    } finally {
      clearTimeout(timeout);
      pending = false;
      send.disabled = reset.disabled = false;
      input.readOnly = false;
    }
  });
})();
