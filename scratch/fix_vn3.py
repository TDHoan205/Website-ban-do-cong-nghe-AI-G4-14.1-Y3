# -*- coding: utf-8 -*-
"""Write fresh Vietnamese template content with proper UTF-8 encoding."""
from pathlib import Path

# ============================================================
# FOOTER.HTML
# ============================================================
footer_content = """<footer class="site-footer">
  <div class="container-px">
    <div class="footer-grid">
      <div>
        <a href="/" class="footer-brand">
          <div class="footer-brand-icon"><i class="fas fa-robot"></i></div>
          <div class="footer-brand-name">Tech Store AI</div>
        </a>
        <p class="footer-desc">Cửa hàng công nghệ hàng đầu Việt Nam với trợ lý AI thông minh, giúp bạn tìm kiếm và chọn lựa sản phẩm phù hợp nhất.</p>
        <div class="footer-socials">
          <a href="#" class="footer-social"><i class="fab fa-facebook-f"></i></a>
          <a href="#" class="footer-social"><i class="fab fa-youtube"></i></a>
          <a href="#" class="footer-social"><i class="fab fa-instagram"></i></a>
          <a href="#" class="footer-social"><i class="fab fa-tiktok"></i></a>
        </div>
      </div>
      <div>
        <h4 class="footer-col-title">Mua hàng</h4>
        <ul class="footer-links">
          <li><a href="/Products/"><i class="fas fa-chevron-right"></i> Sản phẩm</a></li>
          <li><a href="/Products/?sort=new"><i class="fas fa-chevron-right"></i> Sản phẩm mới</a></li>
          <li><a href="/Products/?sort=hot"><i class="fas fa-chevron-right"></i> Sản phẩm hot</a></li>
          <li><a href="/Products/?category_id=1"><i class="fas fa-chevron-right"></i> Điện thoại</a></li>
          <li><a href="/Products/?category_id=2"><i class="fas fa-chevron-right"></i> Laptop</a></li>
        </ul>
      </div>
      <div>
        <h4 class="footer-col-title">Hỗ trợ</h4>
        <ul class="footer-links">
          <li><a href="#"><i class="fas fa-chevron-right"></i> Hướng dẫn mua hàng</a></li>
          <li><a href="#"><i class="fas fa-chevron-right"></i> Chính sách đổi trả</a></li>
          <li><a href="#"><i class="fas fa-chevron-right"></i> Chính sách bảo hành</a></li>
          <li><a href="/Chat/"><i class="fas fa-chevron-right"></i> Trợ lý AI</a></li>
          <li><a href="#"><i class="fas fa-chevron-right"></i> Liên hệ</a></li>
        </ul>
      </div>
      <div>
        <h4 class="footer-col-title">Liên hệ</h4>
        <div class="footer-contact-item"><i class="fas fa-map-marker-alt"></i><span>Hà Nội, Việt Nam</span></div>
        <div class="footer-contact-item"><i class="fas fa-phone"></i><span>1800.6601</span></div>
        <div class="footer-contact-item"><i class="fas fa-envelope"></i><span>hotro@techstore.com</span></div>
        <div class="footer-contact-item"><i class="fas fa-clock"></i><span>Thứ 2 - CN: 8:00 - 22:00</span></div>
      </div>
    </div>
    <div class="footer-bottom">
      <div class="footer-copyright">2026 Tech Store AI. Tất cả quyền được bảo lưu.</div>
      <div class="footer-payments">
        <div class="footer-payment">VISA</div>
        <div class="footer-payment">MC</div>
        <div class="footer-payment">JCB</div>
        <div class="footer-payment">COD</div>
      </div>
    </div>
  </div>
</footer>
"""

footer_path = Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\partials\footer.html")
footer_path.write_text(footer_content, encoding='utf-8')
print(f"footer.html: {len(footer_content)} chars written")

# ============================================================
# CHATBOT.HTML
# ============================================================
chatbot_content = """<style>
/* AI Chatbot - Futuristic Widget */
.cb-toggle {
  position: fixed; bottom: 28px; right: 28px; z-index: 9999;
  width: 64px; height: 64px; border-radius: 50%;
  background: linear-gradient(135deg, #3B82F6, #0EA5E9);
  border: none; color: #fff; font-size: 1.5rem;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; box-shadow: 0 8px 28px rgba(59,130,246,.5);
  transition: all .3s cubic-bezier(.4,0,.2,1);
  animation: cb-glow 3s ease-in-out infinite;
}
@keyframes cb-glow {
  0%,100%{box-shadow:0 6px 24px rgba(59,130,246,.45),0 0 0 0 rgba(59,130,246,.25);}
  50%{box-shadow:0 10px 40px rgba(59,130,246,.65),0 0 0 14px rgba(59,130,246,0);}
}
.cb-toggle:hover {
  transform: scale(1.12);
  box-shadow: 0 14px 48px rgba(59,130,246,.65),0 0 50px rgba(59,130,246,.2);
}
.cb-toggle .badge-dot {
  position: absolute; top: 5px; right: 5px; width: 14px; height: 14px;
  background: #10B981; border-radius: 50%;
  border: 2.5px solid #fff;
  animation: cb-online 2s infinite;
}
@keyframes cb-online {
  0%,100%{box-shadow:0 0 0 0 rgba(16,185,129,.5);}
  50%{box-shadow:0 0 0 7px rgba(16,185,129,0);}
}
.cb-popup {
  position: fixed; bottom: 108px; right: 28px; z-index: 9998;
  width: 400px; max-height: 620px; border-radius: 20px;
  background: #fff; display: none; flex-direction: column;
  overflow: hidden; animation: cb-in .35s cubic-bezier(.4,0,.2,1);
  font-family: 'Be Vietnam Pro',sans-serif;
  border: 1px solid rgba(59,130,246,.15);
  box-shadow: 0 24px 80px rgba(0,0,0,.14),0 0 40px rgba(59,130,246,.08);
}
.cb-popup.active { display: flex; }
@keyframes cb-in {
  from{opacity:0;transform:translateY(24px) scale(.94);}
  to{opacity:1;transform:translateY(0) scale(1);}
}
.cb-hdr {
  background: linear-gradient(135deg, #1E40AF, #3B82F6);
  color: #fff; padding: 18px 20px;
  display: flex; align-items: center; gap: 14px; flex-shrink: 0;
}
.cb-hdr-icon {
  width: 46px; height: 46px;
  background: rgba(255,255,255,.18);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.25rem;
  box-shadow: 0 0 24px rgba(96,165,250,.45);
  animation: cb-icon-pulse 2.5s ease-in-out infinite alternate;
}
@keyframes cb-icon-pulse {
  from{box-shadow:0 0 16px rgba(96,165,250,.35);}
  to{box-shadow:0 0 30px rgba(96,165,250,.7);}
}
.cb-hdr-info { flex: 1; }
.cb-hdr-info h6 { margin: 0; font-weight: 700; font-size: .95rem; }
.cb-hdr-info small { opacity: .8; font-size: .75rem; }
.cb-hdr-actions { display: flex; gap: 6px; }
.cb-hdr-actions button {
  background: rgba(255,255,255,.18); border: none; color: #fff;
  width: 34px; height: 34px; border-radius: 50%;
  cursor: pointer; display: flex; align-items: center; justify-content: center;
  font-size: .85rem; transition: all .15s;
}
.cb-hdr-actions button:hover { background: rgba(255,255,255,.32); }
.cb-msgs {
  flex: 1; overflow-y: auto; padding: 16px;
  background: #F8FAFC;
  min-height: 300px; max-height: 420px;
  scroll-behavior: smooth;
}
.cb-msg { display: flex; margin-bottom: 14px; animation: cb-msg .3s ease; }
@keyframes cb-msg { from{opacity:0;transform:translateY(10px);} to{opacity:1;transform:translateY(0);} }
.cb-msg.user { flex-direction: row-reverse; }
.cb-avatar {
  width: 34px; height: 34px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: .8rem; flex-shrink: 0; margin: 0 8px;
}
.cb-msg.bot .cb-avatar { background: #EFF6FF; color: #3B82F6; }
.cb-msg.user .cb-avatar { background: #3B82F6; color: #fff; }
.cb-bubble {
  max-width: 80%; padding: 11px 15px; border-radius: 16px;
  font-size: .85rem; line-height: 1.55; word-wrap: break-word;
}
.cb-msg.bot .cb-bubble {
  background: #fff; border: 1px solid #E2E8F0;
  color: #0F172A; border-bottom-left-radius: 5px;
  box-shadow: 0 1px 3px rgba(0,0,0,.05);
}
.cb-msg.user .cb-bubble {
  background: linear-gradient(135deg, #3B82F6, #0EA5E9);
  color: #fff; border-bottom-right-radius: 5px;
}
.cb-bubble p { margin: 0 0 5px; }
.cb-bubble p:last-child { margin-bottom: 0; }
.cb-bubble strong { font-weight: 600; }
.cb-time { font-size: .68rem; color: #94A3B8; margin-top: 4px; padding: 0 4px; }
.cb-msg.user .cb-time { text-align: right; }
.cb-typing .cb-bubble { padding: 14px 18px; }
.cb-dots { display: flex; gap: 4px; }
.cb-dots span {
  width: 7px; height: 7px; background: #94A3B8;
  border-radius: 50%; animation: cb-bounce 1.4s infinite;
}
.cb-dots span:nth-child(2){animation-delay:.18s}
.cb-dots span:nth-child(3){animation-delay:.36s}
@keyframes cb-bounce { 0%,60%,100%{transform:translateY(0)} 30%{transform:translateY(-7px)} }
.cb-quick {
  padding: 10px 14px; border-top: 1px solid #F1F5F9;
  background: #fff; display: flex; flex-wrap: wrap; gap: 6px; flex-shrink: 0;
}
.cb-quick-btn {
  padding: 5px 13px; font-size: .73rem; border-radius: 999px;
  border: 1.5px solid #93C5FD; color: #3B82F6; background: #fff;
  cursor: pointer; font-family: inherit; font-weight: 600;
  transition: all .2s;
}
.cb-quick-btn:hover { background: #3B82F6; color: #fff; border-color: #3B82F6; }
.cb-input {
  padding: 12px 14px; border-top: 1px solid #F1F5F9;
  background: #fff; display: flex; gap: 8px;
  align-items: center; flex-shrink: 0;
}
.cb-input input {
  flex: 1; border: 1.5px solid #E2E8F0; border-radius: 999px;
  padding: 10px 18px; font-size: .85rem; outline: none;
  font-family: inherit; transition: all .2s; background: #F8FAFC;
}
.cb-input input:focus {
  border-color: #3B82F6;
  box-shadow: 0 0 0 3px rgba(59,130,246,.12);
  background: #fff;
}
.cb-send {
  width: 42px; height: 42px; border-radius: 50%; border: none;
  background: linear-gradient(135deg, #3B82F6, #0EA5E9); color: #fff;
  cursor: pointer; display: flex; align-items: center; justify-content: center;
  font-size: .88rem; transition: all .2s;
  box-shadow: 0 4px 14px rgba(59,130,246,.3);
}
.cb-send:hover { transform: scale(1.1); box-shadow: 0 8px 28px rgba(59,130,246,.45); }
.cb-send:disabled { opacity: .45; cursor: not-allowed; transform: none; }
@media (max-width: 480px) {
  .cb-popup {
    width: calc(100vw - 20px); right: 10px;
    bottom: 96px; max-height: 75vh;
  }
}
</style>

<button class="cb-toggle" id="cb-toggle" title="Chat với AI">
  <i class="fas fa-comments"></i>
  <span class="badge-dot"></span>
</button>

<div class="cb-popup" id="cb-popup">
  <div class="cb-hdr">
    <div class="cb-hdr-icon"><i class="fas fa-robot"></i></div>
    <div class="cb-hdr-info">
      <h6>Trợ lý AI Tech Store</h6>
      <small><i class="fas fa-circle" style="font-size:.45rem;color:#10B981"></i> Sẵn sàng hỗ trợ</small>
    </div>
    <div class="cb-hdr-actions">
      <button onclick="window.open('/Chat/','_blank')" title="Mở trang chat lớn"><i class="fas fa-expand-alt"></i></button>
      <button onclick="cbClose()" title="Đóng"><i class="fas fa-times"></i></button>
    </div>
  </div>
  <div class="cb-msgs" id="cb-msgs">
    <div class="cb-msg bot">
      <div class="cb-avatar"><i class="fas fa-robot"></i></div>
      <div>
        <div class="cb-bubble">
          Xin chào! Tôi là <strong>Trợ lý AI</strong> của Tech Store.<br><br>
          Tôi có thể giúp bạn:<br>
          Tìm và tư vấn sản phẩm công nghệ<br>
          So sánh giá, thông số kỹ thuật<br>
          Tra cứu đơn hàng, khuyến mãi<br><br>
          Bạn cần hỗ trợ gì?
        </div>
        <div class="cb-time">Vừa xong</div>
      </div>
    </div>
  </div>
  <div class="cb-quick" id="cb-quick">
    <button class="cb-quick-btn" onclick="cbSend('Sản phẩm nổi bật?')">Sản phẩm HOT</button>
    <button class="cb-quick-btn" onclick="cbSend('Có khuyến mãi gì?')">Khuyến mãi</button>
    <button class="cb-quick-btn" onclick="cbSend('Tư vấn laptop')">Tư vấn laptop</button>
  </div>
  <div class="cb-input">
    <input type="text" id="cb-input" placeholder="Nhập tin nhắn..." autocomplete="off" />
    <button class="cb-send" id="cb-send" onclick="cbSendInput()"><i class="fas fa-paper-plane"></i></button>
  </div>
</div>

<script>
(function(){
  var toggle=document.getElementById('cb-toggle');
  var popup=document.getElementById('cb-popup');
  var msgs=document.getElementById('cb-msgs');
  var input=document.getElementById('cb-input');
  var sendBtn=document.getElementById('cb-send');
  var sessionUuid=localStorage.getItem('cb_session')||'',sending=false;

  toggle.addEventListener('click',function(){
    popup.classList.toggle('active');
    if(popup.classList.contains('active')){
      toggle.innerHTML='<i class="fas fa-times"></i>';
      input.focus();
      if(!sessionUuid)initSession();
    } else {
      toggle.innerHTML='<i class="fas fa-comments"></i><span class="badge-dot"></span>';
    }
  });

  window.cbClose=function(){
    popup.classList.remove('active');
    toggle.innerHTML='<i class="fas fa-comments"></i><span class="badge-dot"></span>';
  };

  input.addEventListener('keydown',function(e){
    if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();cbSendInput();}
  });

  async function initSession(){
    try{
      var r=await fetch('/Chat/Widget/Init',{method:'POST'});
      var d=await r.json();
      if(d.success){sessionUuid=d.session_uuid;localStorage.setItem('cb_session',sessionUuid);}
    } catch(e){}
  }

  window.cbSendInput=function(){
    var msg=input.value.trim();
    if(!msg||sending)return;
    input.value='';
    cbSend(msg);
  };

  window.cbSend=async function(message){
    if(sending)return;
    if(!sessionUuid)await initSession();
    sending=true;sendBtn.disabled=true;
    addMsg(message,'user');
    document.getElementById('cb-quick').style.display='none';
    var typ=document.createElement('div');
    typ.className='cb-msg bot cb-typing';
    typ.id='cb-typing';
    typ.innerHTML='<div class="cb-avatar"><i class="fas fa-robot"></i></div><div><div class="cb-bubble"><div class="cb-dots"><span></span><span></span><span></span></div></div></div>';
    msgs.appendChild(typ);
    msgs.scrollTop=msgs.scrollHeight;
    try{
      var r=await fetch('/Chat/Widget/Send',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session_uuid:sessionUuid,message:message})});
      var d=await r.json();
      var t=document.getElementById('cb-typing');
      if(t)t.remove();
      if(d.success){
        if(d.session_uuid){sessionUuid=d.session_uuid;localStorage.setItem('cb_session',sessionUuid);}
        addMsg(d.response,'bot');
      } else {
        addMsg('Đã xảy ra lỗi. Vui lòng thử lại.','bot');
      }
    } catch(e){
      var t=document.getElementById('cb-typing');
      if(t)t.remove();
      addMsg('Không thể kết nối server.','bot');
    }
    sending=false;sendBtn.disabled=false;input.focus();
  };

  function addMsg(content,sender){
    var div=document.createElement('div');
    div.className='cb-msg '+sender;
    var icon=sender==='bot'?'fa-robot':'fa-user';
    var now=new Date().toLocaleTimeString('vi-VN',{hour:'2-digit',minute:'2-digit'});
    var rendered=sender==='bot'?renderMd(escHtml(content)):escHtml(content);
    div.innerHTML='<div class="cb-avatar"><i class="fas '+icon+'"></i></div><div><div class="cb-bubble">'+rendered+'</div><div class="cb-time">'+now+'</div></div>';
    msgs.appendChild(div);
    msgs.scrollTop=msgs.scrollHeight;
  }

  function escHtml(s){var d=document.createElement('div');d.textContent=s;return d.innerHTML;}

  function renderMd(t){
    if(!t)return'';
    var h=escHtml(t);
    h=h.replace(/\\*\\*(.+?)\\*\\*/g,'<strong>$1</strong>');
    h=h.replace(/\\*(.+?)\\*/g,'<em>$1</em>');
    h=h.replace(/`(.+?)`/g,'<code style="background:#f1f5f9;padding:1px 5px;border-radius:4px;font-size:.82em">$1</code>');
    h=h.replace(/^[-•]\\s+(.+)/gm,'<li>$1</li>');
    h=h.replace(/(<li>.*<\\/li>)/gs,'<ul style="margin:4px 0;padding-left:18px">$1</ul>');
    h=h.replace(/\\n/g,'<br>');
    h=h.replace(/(<br>){3,}/g,'<br><br>');
    return h;
  }
})();
</script>
"""

chatbot_path = Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\partials\chatbot.html")
chatbot_path.write_text(chatbot_content, encoding='utf-8')
print(f"chatbot.html: {len(chatbot_content)} chars written")

# ============================================================
# BASE.HTML
# ============================================================
base_content = """<!doctype html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Tech Store AI</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />
  <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/static/css/style.css?v=4" />
  <link rel="icon" type="image/svg+xml" href="/static/favicon.svg" />
  {% block extra_head %}{% endblock %}
</head>
<body>
  <div class="ann-bar">
    <strong><i class="fas fa-truck"></i> Miễn phí vận chuyển</strong> toàn quốc cho đơn từ 500.000đ &nbsp;|&nbsp;
    <a href="/Products/"><i class="fas fa-bolt"></i> Khuyến mãi hôm nay</a>
  </div>

  <header class="site-header" id="site-header">
    <div class="header-inner">
      <a href="/" class="header-logo">
        <div class="header-logo-icon"><i class="fas fa-robot"></i></div>
        <div>
          <div class="header-logo-name">Tech <span>Store</span> AI</div>
          <div class="header-logo-sub">Công nghệ thông minh</div>
        </div>
      </a>
      <div class="header-search">
        <form action="/Products/" method="GET" class="search-form">
          <input type="text" name="search" placeholder="Tìm kiếm sản phẩm..." value="{{ search | default('') }}" />
          <button type="submit"><i class="fas fa-search"></i> Tìm</button>
        </form>
      </div>
      <div class="header-actions">
        <a href="/Cart/" class="header-act">
          <div class="header-act-icon">
            <i class="fas fa-shopping-bag"></i>
            <span class="header-act-badge">{{ cart_count | default(0) }}</span>
          </div>
          <div class="header-act-label">Giỏ hàng</div>
        </a>
        {% if current_user %}
        <div class="user-menu">
          <a href="#" class="header-act" onclick="return false">
            <div class="header-act-icon" style="color:#10B981"><i class="fas fa-user-circle"></i></div>
            <div class="header-act-label" style="color:#10B981">{{ current_user.full_name or current_user.username }}</div>
          </a>
          <div class="user-drop" id="userDrop">
            <a href="/Auth/Profile" class="user-drop-item"><i class="fas fa-user"></i> Thông tin cá nhân</a>
            <a href="/Orders/" class="user-drop-item"><i class="fas fa-shopping-bag"></i> Đơn hàng</a>
            {% if current_user.role_name == 'Admin' %}
            <a href="/Admin/Dashboard" class="user-drop-item"><i class="fas fa-cog"></i> Quản lý Admin</a>
            {% endif %}
            <div class="user-drop-divider"></div>
            <a href="/Auth/Logout" class="user-drop-item danger"><i class="fas fa-sign-out-alt"></i> Đăng xuất</a>
          </div>
        </div>
        {% else %}
        <a href="/Auth/Login" class="header-act">
          <div class="header-act-icon"><i class="fas fa-user"></i></div>
          <div class="header-act-label">Đăng nhập</div>
        </a>
        {% endif %}
      </div>
    </div>
  </header>

  <nav class="navbar">
    <div class="navbar-inner">
      <button class="navbar-cats-btn"><i class="fas fa-bars"></i> <span>Danh mục</span></button>
      <ul class="navbar-links">
        <li><a href="/"><i class="fas fa-home"></i> Trang chủ</a></li>
        <li><a href="/Products/">Sản phẩm</a></li>
        <li><a href="/Cart/">Giỏ hàng</a></li>
        <li><a href="/Chat/" class="ai-link"><i class="fas fa-robot"></i> AI Tư vấn</a></li>
        <li><a href="/Products/?sort=new" style="color:#fde68a;font-weight:700"><i class="fas fa-bolt"></i> Mới nhất</a></li>
        <li><a href="/Products/?sort=hot" style="color:#fca5a5;font-weight:700"><i class="fas fa-fire"></i> Hot</a></li>
      </ul>
      <div class="navbar-support"><i class="fas fa-headset"></i> Hỗ trợ: 1800.6601</div>
    </div>
  </nav>

  {% block content %}{% endblock %}

  {% include "partials/footer.html" %}

  {% include "partials/chatbot.html" %}

  <div id="toast-container" aria-live="polite" aria-atomic="true"></div>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
  <script src="/static/js/main.js?v=4"></script>
  <script>
  (function(){
    var um=document.querySelector('.user-menu');
    if(um&&document.getElementById('userDrop')){
      um.querySelector('.header-act').addEventListener('click',function(e){e.preventDefault();e.stopPropagation();document.getElementById('userDrop').classList.toggle('show');});
      document.addEventListener('click',function(e){if(!um.contains(e.target))document.getElementById('userDrop').classList.remove('show');});
    }
    window.addEventListener('scroll',function(){
      var h=document.getElementById('site-header');
      if(h)h.classList.toggle('scrolled',window.scrollY>5);
    });
  })();
  </script>
</body>
</html>
"""

base_path = Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\Views\Shared\base.html")
base_path.write_text(base_content, encoding='utf-8')
print(f"base.html: {len(base_content)} chars written")

print("\nAll files written successfully!")
