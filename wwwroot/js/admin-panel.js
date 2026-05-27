(function(){
  if (window.__adminPanelLoaded) return; window.__adminPanelLoaded = true;
  function createPanel(){
    if(document.getElementById('admin-side-panel')) return;
    const panel = document.createElement('div');
    panel.id = 'admin-side-panel';
    panel.style.position = 'fixed';
    panel.style.top = '64px';
    panel.style.height = 'calc(100vh - 64px)';
    panel.style.background = '#0b1220';
    panel.style.zIndex = 1300;
    panel.style.display = 'none';
    panel.style.overflow = 'hidden';
    panel.innerHTML = `
      <div style="display:flex;align-items:center;justify-content:space-between;padding:12px 14px;background:#0f172a;color:#e2e8f0;border-bottom:1px solid #334155;">
        <div id="admin-side-panel-title" style="font-weight:700;">Panel</div>
        <div>
          <button id="admin-side-panel-close" style="background:transparent;border:none;color:#94a3b8;cursor:pointer;font-size:1.0rem;padding:6px;">✕</button>
        </div>
      </div>
      <iframe id="admin-side-panel-iframe" src="about:blank" style="width:100%;height:calc(100% - 52px);border:0;background:#020617;color:#e2e8f0;"></iframe>
    `;
    document.body.appendChild(panel);
    document.getElementById('admin-side-panel-close').addEventListener('click', function(){ 
      panel.style.display='none'; 
      // Restore active sidebar link
      const activePanelLink = document.querySelector('[data-admin-panel].active');
      if (activePanelLink) {
        activePanelLink.classList.remove('active');
      }
      if (window.__prevActiveSidebarLink) {
        window.__prevActiveSidebarLink.classList.add('active');
        window.__prevActiveSidebarLink = null;
      }
    });
  }

  function openPanel(title, url, align){
    createPanel();
    const panel = document.getElementById('admin-side-panel');
    const iframe = document.getElementById('admin-side-panel-iframe');
    document.getElementById('admin-side-panel-title').innerText = title || 'Panel';
    iframe.src = url;
    panel.setAttribute('data-align', align || 'right');

    const isMobile = window.innerWidth <= 640;
    if (align === 'left') {
      panel.style.right = '0';
      panel.style.left = isMobile ? '0' : '230px';
      panel.style.width = isMobile ? '100vw' : 'calc(100vw - 230px)';
      panel.style.borderLeft = 'none';
      panel.style.borderRight = 'none';
    } else {
      panel.style.left = isMobile ? '0' : 'auto';
      panel.style.right = '0';
      panel.style.width = isMobile ? '100vw' : 'min(100vw - 230px, 880px)';
      panel.style.borderRight = 'none';
      panel.style.borderLeft = isMobile ? 'none' : '1px solid #334155';
    }
    panel.style.display = 'block';
  }

  window.adminOpenPanel = openPanel;

  document.addEventListener('click', function(e){
    const t = e.target.closest('[data-admin-panel]');
    if(!t) return;
    e.preventDefault();
    const url = t.getAttribute('data-admin-panel');
    const title = t.getAttribute('data-admin-panel-title') || t.textContent.trim();
    const align = t.getAttribute('data-admin-panel-align') || 'right';
    
    // Manage active sidebar link state
    const activePanelLink = document.querySelector('[data-admin-panel].active');
    if (activePanelLink && activePanelLink !== t) {
      activePanelLink.classList.remove('active');
    }
    
    if (!t.classList.contains('active')) {
      const prevActive = document.querySelector('.sidebar-link.active');
      if (prevActive && prevActive !== t) {
        window.__prevActiveSidebarLink = prevActive;
        prevActive.classList.remove('active');
      }
      t.classList.add('active');
    }
    
    openPanel(title, url, align);
  });

  window.addEventListener('resize', function(){
    const panel = document.getElementById('admin-side-panel');
    if(!panel || panel.style.display === 'none') return;
    const align = panel.getAttribute('data-align');
    const isMobile = window.innerWidth <= 640;
    
    if (align === 'left') {
      panel.style.left = isMobile ? '0' : '230px';
      panel.style.width = isMobile ? '100vw' : 'calc(100vw - 230px)';
    } else {
      panel.style.left = isMobile ? '0' : 'auto';
      panel.style.width = isMobile ? '100vw' : 'min(100vw - 230px, 880px)';
    }
    panel.style.height = 'calc(100vh - 64px)';
  });
})();
