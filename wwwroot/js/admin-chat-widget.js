(function () {
  if (window.__adminChatWidgetInitialized) return;
  window.__adminChatWidgetInitialized = true;

  const style = document.createElement("style");
  style.textContent = `
    .admin-chat-widget {
      position: fixed;
      right: 24px;
      bottom: 102px;
      z-index: 1100;
      width: 360px;
      max-height: 560px;
      display: none;
      flex-direction: column;
      border: 1px solid #334155;
      border-radius: 14px;
      overflow: hidden;
      background: #0f172a;
      box-shadow: 0 16px 48px rgba(0,0,0,0.4);
      font-family: 'Be Vietnam Pro', sans-serif;
    }
    .admin-chat-widget.active { display: flex; }
    .admin-chat-head {
      background: #1e293b;
      color: #e2e8f0;
      padding: 10px 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid #334155;
    }
    .admin-chat-head h6 {
      margin: 0;
      font-size: 0.9rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .admin-chat-head button {
      border: none;
      background: transparent;
      color: #94a3b8;
      cursor: pointer;
      font-size: 0.9rem;
    }
    .admin-chat-head button:hover { color: #e2e8f0; }
    .admin-chat-msgs {
      background: #020617;
      padding: 12px;
      overflow-y: auto;
      min-height: 240px;
      max-height: 360px;
    }
    .admin-chat-row { display: flex; margin-bottom: 10px; }
    .admin-chat-row.user { justify-content: flex-end; }
    .admin-chat-row.bot { justify-content: flex-start; }
    .admin-chat-bubble {
      max-width: 78%;
      padding: 8px 10px;
      border-radius: 10px;
      font-size: 0.82rem;
      line-height: 1.5;
      word-break: break-word;
    }
    .admin-chat-row.user .admin-chat-bubble {
      background: #2563eb;
      color: #fff;
      border-bottom-right-radius: 2px;
    }
    .admin-chat-row.bot .admin-chat-bubble {
      background: #1e293b;
      color: #e2e8f0;
      border: 1px solid #334155;
      border-bottom-left-radius: 2px;
    }
    .admin-chat-input {
      display: flex;
      gap: 8px;
      padding: 10px;
      border-top: 1px solid #334155;
      background: #0f172a;
    }
    .admin-chat-input input {
      flex: 1;
      border: 1px solid #334155;
      border-radius: 10px;
      background: #020617;
      color: #e2e8f0;
      padding: 8px 10px;
      font-size: 0.82rem;
      outline: none;
    }
    .admin-chat-input button {
      border: none;
      width: 36px;
      border-radius: 10px;
      background: #2563eb;
      color: #fff;
      cursor: pointer;
      font-size: 0.86rem;
    }
    @media (max-width: 768px) {
      .admin-chat-widget {
        right: 12px;
        left: 12px;
        width: auto;
        bottom: 12px;
      }
    }
  `;
  document.head.appendChild(style);

  const panel = document.createElement("div");
  panel.className = "admin-chat-widget";
  panel.id = "admin-chat-widget";
  panel.innerHTML = `
    <div class="admin-chat-head">
      <h6><i class="fas fa-robot"></i> AI Chatbot</h6>
      <button type="button" id="admin-chat-close" aria-label="Close"><i class="fas fa-times"></i></button>
    </div>
    <div class="admin-chat-msgs" id="admin-chat-msgs">
      <div class="admin-chat-row bot"><div class="admin-chat-bubble">Xin chào! Tôi có thể hỗ trợ bạn ngay trong trang admin.</div></div>
    </div>
    <div class="admin-chat-input">
      <input id="admin-chat-input" type="text" placeholder="Nhập nội dung..." />
      <button id="admin-chat-send" type="button"><i class="fas fa-paper-plane"></i></button>
    </div>
  `;
  document.body.appendChild(panel);

  const msgs = document.getElementById("admin-chat-msgs");
  const input = document.getElementById("admin-chat-input");
  const send = document.getElementById("admin-chat-send");
  const close = document.getElementById("admin-chat-close");

  let sessionUuid = localStorage.getItem("admin_cb_session") || "";
  let sending = false;

  function escHtml(text) {
    const d = document.createElement("div");
    d.textContent = text || "";
    return d.innerHTML;
  }

  function renderMd(text) {
    let h = escHtml(text);
    h = h.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
    h = h.replace(/\n/g, "<br>");
    return h;
  }

  function addMsg(content, sender) {
    const row = document.createElement("div");
    row.className = `admin-chat-row ${sender}`;
    const bubble = sender === "bot" ? renderMd(content) : escHtml(content);
    row.innerHTML = `<div class="admin-chat-bubble">${bubble}</div>`;
    msgs.appendChild(row);
    msgs.scrollTop = msgs.scrollHeight;
  }

  async function initSession() {
    if (sessionUuid) return;
    try {
      const r = await fetch("/Chat/Widget/Init", { method: "POST" });
      const d = await r.json();
      if (d.success && d.session_uuid) {
        sessionUuid = d.session_uuid;
        localStorage.setItem("admin_cb_session", sessionUuid);
      }
    } catch (_) {}
  }

  async function sendMessage() {
    const message = input.value.trim();
    if (!message || sending) return;

    sending = true;
    send.disabled = true;
    input.value = "";
    addMsg(message, "user");

    try {
      await initSession();
      const r = await fetch("/Chat/Widget/Send", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_uuid: sessionUuid, message }),
      });
      const d = await r.json();
      if (d.success) {
        if (d.session_uuid) {
          sessionUuid = d.session_uuid;
          localStorage.setItem("admin_cb_session", sessionUuid);
        }
        addMsg(d.response || "Đã nhận được tin nhắn.", "bot");
      } else {
        addMsg("He thong dang ban, vui long thu lai.", "bot");
      }
    } catch (_) {
      addMsg("Không thể kết nối chatbot.", "bot");
    }

    sending = false;
    send.disabled = false;
    input.focus();
  }

  function togglePanel() {
    const willOpen = !panel.classList.contains("active");
    if (willOpen && typeof window.closeAdminFinanceWidget === "function") {
      window.closeAdminFinanceWidget();
    }
    panel.classList.toggle("active");
    if (panel.classList.contains("active")) {
      initSession();
      input.focus();
    }
  }

  close.addEventListener("click", function () {
    panel.classList.remove("active");
  });
  send.addEventListener("click", sendMessage);
  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage();
    }
  });

  window.toggleAdminChatWidget = function (e) {
    if (e) e.preventDefault();
    togglePanel();
  };

  window.closeAdminChatWidget = function () {
    panel.classList.remove("active");
  };

  document.addEventListener("click", function (e) {
    const link = e.target.closest(".js-admin-chat-toggle");
    if (!link) return;
    e.preventDefault();
    togglePanel();
  });
})();
