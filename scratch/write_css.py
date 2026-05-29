# -*- coding: utf-8 -*-
from pathlib import Path

# Read existing CSS
css_path = Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\wwwroot\css\style.css")
css = css_path.read_text(encoding='utf-8')

# Define what to remove and what to add
# We need to replace the entire ANNOUNCEMENT BAR + HEADER + NAVBAR section

old_section = """/* ============================================================
   TOP ANNOUNCEMENT BAR
   ============================================================ */
.ann-bar {
  background: var(--bg-dark);
  color: rgba(255,255,255,.75);
  font-size: .75rem;
  padding: 7px 0;
  text-align: center;
  letter-spacing: .3px;
}
.ann-bar strong { color: #fbbf24; }
.ann-bar a { color: var(--primary-light); font-weight: 600; }
.ann-bar a:hover { color: #fff; }

/* ============================================================
   HEADER
   ============================================================ */
.site-header {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: rgba(255,255,255,.88);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid var(--border-light);
  box-shadow: var(--shadow-xs);
  transition: var(--transition);
}
.site-header.scrolled {
  box-shadow: var(--shadow-md);
  background: rgba(255,255,255,.96);
}

.header-inner {
  max-width: var(--container);
  margin: 0 auto;
  padding: 0 24px;
  height: 68px;
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  flex-shrink: 0;
}
.header-logo-icon {
  width: 40px; height: 40px;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 1.1rem;
  box-shadow: 0 4px 12px rgba(59,130,246,.35);
  transition: var(--transition);
}
.header-logo:hover .header-logo-icon {
  transform: translateY(-1px) scale(1.04);
  box-shadow: var(--shadow-primary);
}
.header-logo-name {
  font-size: 1.05rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -.3px;
  line-height: 1.2;
}
.header-logo-name span { color: var(--primary); }
.header-logo-sub {
  font-size: .65rem;
  color: var(--text-muted);
  font-weight: 400;
}

/* Search */
.header-search {
  flex: 1;
  max-width: 520px;
}
.search-form {
  display: flex;
  border: 1.5px solid var(--border);
  border-radius: var(--radius-full);
  background: var(--bg-gray-50);
  overflow: hidden;
  transition: var(--transition);
}
.search-form:focus-within {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px var(--primary-glow);
  background: #fff;
}
.search-form input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  padding: 10px 18px;
  font-size: .85rem;
  font-family: inherit;
  color: var(--text-primary);
}
.search-form input::placeholder { color: var(--text-muted); }
.search-form button {
  background: var(--primary);
  color: #fff;
  border: none;
  padding: 8px 18px;
  font-size: .82rem;
  font-weight: 600;
  cursor: pointer;
  display: flex; align-items: center; gap: 6px;
  font-family: inherit;
  transition: var(--transition);
  white-space: nowrap;
}
.search-form button:hover { background: var(--primary-dark); }

/* Header actions */
.header-actions { display: flex; align-items: center; gap: 6px; flex-shrink: 0; }
.header-act {
  display: flex; align-items: center; gap: 8px;
  padding: 8px 14px;
  border-radius: var(--radius-md);
  font-size: .8rem;
  font-weight: 500;
  color: var(--text-secondary);
  transition: var(--transition);
  position: relative;
  cursor: pointer;
  background: none; border: none;
  text-decoration: none;
}
.header-act:hover { background: var(--bg-gray-100); color: var(--text-primary); }
.header-act-icon { font-size: 1.25rem; color: var(--text-secondary); position: relative; }
.header-act-badge {
  position: absolute; top: -6px; right: -8px;
  background: var(--danger);
  color: #fff; font-size: .58rem; font-weight: 700;
  min-width: 17px; height: 17px;
  border-radius: var(--radius-full);
  display: flex; align-items: center; justify-content: center;
  padding: 0 4px;
  border: 2px solid #fff;
}
.header-act-label { font-size: .7rem; color: var(--text-muted); font-weight: 400; }
.header-act:hover .header-act-icon { color: var(--primary); }

/* User dropdown */
.user-menu { position: relative; }
.user-drop {
  position: absolute; top: calc(100% + 8px); right: 0;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  min-width: 200px;
  padding: 8px 0;
  z-index: 1001;
  display: none;
}
.user-drop.show { display: block; animation: dropIn .2s ease; }
@keyframes dropIn { from { opacity: 0; transform: translateY(-8px); } to { opacity: 1; transform: translateY(0); } }
.user-drop-item {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 16px;
  font-size: .85rem; font-weight: 500;
  color: var(--text-secondary);
  transition: var(--transition-fast);
  text-decoration: none;
}
.user-drop-item:hover { background: var(--bg-gray-50); color: var(--primary); }
.user-drop-item i { width: 18px; text-align: center; color: var(--text-muted); }
.user-drop-item.danger { color: var(--danger); }
.user-drop-item.danger:hover { background: #fef2f2; color: var(--danger); }
.user-drop-divider { height: 1px; background: var(--border-light); margin: 6px 0; }

/* ============================================================
   NAVBAR
   ============================================================ */
.navbar {
  background: var(--primary);
  position: sticky;
  top: 68px;
  z-index: 999;
}
.navbar-inner {
  max-width: var(--container);
  margin: 0 auto;
  padding: 0 24px;
  height: 46px;
  display: flex;
  align-items: center;
  gap: 0;
}
.navbar-cats-btn {
  background: rgba(255,255,255,.12);
  border: none;
  color: #fff;
  font-size: .8rem;
  font-weight: 600;
  padding: 7px 14px;
  border-radius: var(--radius-md);
  cursor: pointer;
  display: flex; align-items: center; gap: 7px;
  font-family: inherit;
  margin-right: 16px;
  transition: var(--transition-fast);
  white-space: nowrap;
}
.navbar-cats-btn:hover { background: rgba(255,255,255,.22); }
.navbar-links {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 2px;
  flex: 1;
  overflow: hidden;
}
.navbar-links li a {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 7px 13px;
  color: rgba(255,255,255,.85);
  font-size: .82rem;
  font-weight: 500;
  border-radius: var(--radius-md);
  transition: var(--transition-fast);
  text-decoration: none;
  white-space: nowrap;
}
.navbar-links li a:hover { background: rgba(255,255,255,.14); color: #fff; }
.navbar-links li a.ai { color: #93C5FD; font-weight: 700; }
.navbar-links li a.ai:hover { background: rgba(147,197,253,.18); color: #bfdbfe; }
.navbar-support {
  color: rgba(255,255,255,.6);
  font-size: .75rem;
  margin-left: 16px;
  white-space: nowrap;
  display: flex; align-items: center; gap: 6px;
}"""

new_section = """/* ============================================================
   UNIFIED PREMIUM HEADER
   ============================================================ */
.premium-header {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: #fff;
  box-shadow: 0 1px 0 rgba(0,0,0,.06);
  transition: box-shadow .25s ease;
}
.premium-header.scrolled {
  box-shadow: 0 4px 24px rgba(0,0,0,.08);
}

/* Header row — logo, search, actions */
.premium-header-inner {
  max-width: var(--container);
  margin: 0 auto;
  padding: 0 24px;
  height: 68px;
  display: flex;
  align-items: center;
  gap: 20px;
}

/* Logo */
.premium-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  flex-shrink: 0;
}
.premium-logo-icon {
  width: 40px; height: 40px;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 1.1rem;
  box-shadow: 0 4px 12px rgba(59,130,246,.35);
  transition: transform .2s ease, box-shadow .2s ease;
}
.premium-logo:hover .premium-logo-icon {
  transform: translateY(-1px) scale(1.04);
  box-shadow: 0 8px 24px rgba(59,130,246,.45);
}
.premium-logo-name {
  font-size: 1.05rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -.3px;
  line-height: 1.2;
}
.premium-logo-name span { color: var(--primary); }
.premium-logo-sub {
  font-size: .65rem;
  color: var(--text-muted);
  font-weight: 400;
}

/* Search */
.premium-search {
  flex: 1;
  max-width: 560px;
  display: flex;
  gap: 8px;
}
.premium-search-box {
  flex: 1;
  display: flex;
  align-items: center;
  border: 1.5px solid var(--border);
  border-radius: var(--radius-full);
  background: var(--bg-gray-50);
  overflow: hidden;
  transition: border-color .2s, box-shadow .2s, background .2s;
  padding: 0 16px;
}
.premium-search-box:focus-within {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(59,130,246,.12);
  background: #fff;
}
.premium-search-icon { color: var(--text-muted); font-size: .85rem; flex-shrink: 0; }
.premium-search input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  padding: 10px 12px;
  font-size: .85rem;
  font-family: inherit;
  color: var(--text-primary);
}
.premium-search input::placeholder { color: var(--text-muted); }
.premium-search button {
  background: var(--primary);
  color: #fff;
  border: none;
  padding: 10px 18px;
  border-radius: var(--radius-full);
  font-size: .82rem;
  font-weight: 600;
  cursor: pointer;
  display: flex; align-items: center;
  font-family: inherit;
  transition: background .2s, box-shadow .2s;
  box-shadow: 0 2px 8px rgba(59,130,246,.3);
}
.premium-search button:hover {
  background: var(--primary-dark);
  box-shadow: 0 4px 16px rgba(59,130,246,.4);
}

/* Header actions */
.premium-actions {
  display: flex;
  align-items: center;
  gap: 4px;
  flex-shrink: 0;
}
.premium-action {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: var(--radius-md);
  font-size: .8rem;
  font-weight: 500;
  color: var(--text-secondary);
  transition: background .15s, color .15s;
  position: relative;
  text-decoration: none;
  cursor: pointer;
}
.premium-action:hover { background: var(--bg-gray-50); color: var(--primary); }
.premium-action-icon {
  font-size: 1.25rem;
  color: var(--text-secondary);
  transition: color .15s;
}
.premium-action:hover .premium-action-icon { color: var(--primary); }
.premium-action-badge {
  position: absolute;
  top: 2px; right: 2px;
  background: var(--danger);
  color: #fff; font-size: .55rem; font-weight: 700;
  min-width: 17px; height: 17px;
  border-radius: var(--radius-full);
  display: flex; align-items: center; justify-content: center;
  padding: 0 4px;
  border: 2px solid #fff;
}
.premium-action-label { font-size: .7rem; color: var(--text-muted); font-weight: 500; }

/* User dropdown */
.premium-user { position: relative; }
.premium-user-drop {
  position: absolute;
  top: calc(100% + 8px); right: 0;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: 0 20px 60px rgba(0,0,0,.12);
  min-width: 210px;
  padding: 8px 0;
  z-index: 1001;
  display: none;
}
.premium-user-drop.show {
  display: block;
  animation: dropIn .2s ease;
}
@keyframes dropIn {
  from { opacity: 0; transform: translateY(-8px); }
  to { opacity: 1; transform: translateY(0); }
}
.premium-drop-item {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 16px;
  font-size: .85rem; font-weight: 500;
  color: var(--text-secondary);
  transition: background .15s, color .15s;
  text-decoration: none;
}
.premium-drop-item:hover { background: var(--bg-gray-50); color: var(--primary); }
.premium-drop-item i { width: 18px; text-align: center; color: var(--text-muted); }
.premium-drop-item.danger { color: var(--danger); }
.premium-drop-item.danger:hover { background: #fef2f2; color: var(--danger); }
.premium-drop-divider { height: 1px; background: var(--border-light); margin: 6px 0; }

/* ============================================================
   PREMIUM NAV STRIP
   ============================================================ */
.premium-nav {
  background: linear-gradient(135deg, var(--primary-dark), var(--primary));
  box-shadow: 0 2px 12px rgba(37,99,235,.25);
}
.premium-nav-inner {
  max-width: var(--container);
  margin: 0 auto;
  padding: 0 24px;
  height: 46px;
  display: flex;
  align-items: center;
  gap: 0;
}
.premium-nav-cats {
  background: rgba(255,255,255,.14);
  border: none;
  color: #fff;
  font-size: .8rem;
  font-weight: 600;
  padding: 7px 14px;
  border-radius: var(--radius-md);
  cursor: pointer;
  display: flex; align-items: center; gap: 7px;
  font-family: inherit;
  margin-right: 16px;
  transition: background .15s;
  white-space: nowrap;
}
.premium-nav-cats:hover { background: rgba(255,255,255,.24); }
.premium-nav-links {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 2px;
  flex: 1;
  overflow: hidden;
}
.premium-nav-link {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 7px 13px;
  color: rgba(255,255,255,.85);
  font-size: .82rem;
  font-weight: 500;
  border-radius: var(--radius-md);
  transition: background .15s, color .15s;
  text-decoration: none;
  white-space: nowrap;
}
.premium-nav-link:hover { background: rgba(255,255,255,.14); color: #fff; }
.premium-nav-link.ai { color: #93C5FD; font-weight: 700; }
.premium-nav-link.ai:hover { background: rgba(147,197,253,.18); color: #bfdbfe; }
.premium-nav-link.new { color: #fde68a; font-weight: 700; }
.premium-nav-link.new:hover { background: rgba(253,230,138,.18); color: #fef08a; }
.premium-nav-link.hot { color: #fca5a5; font-weight: 700; }
.premium-nav-link.hot:hover { background: rgba(252,165,165,.18); color: #fecaca; }
.premium-nav-support {
  color: rgba(255,255,255,.6);
  font-size: .75rem;
  margin-left: 16px;
  white-space: nowrap;
  display: flex; align-items: center; gap: 6px;
}"""

# Replace
if old_section in css:
    css = css.replace(old_section, new_section)
    print("CSS section replaced successfully")
else:
    print("WARNING: Old CSS section not found exactly. Trying fuzzy match...")
    # Try to find where the section starts and ends
    start = css.find("/* ============================================================\n   TOP ANNOUNCEMENT BAR")
    end_marker = "/* ============================================================\n   HERO"
    end = css.find(end_marker)
    if start >= 0 and end >= 0:
        css = css[:start] + new_section + "\n\n" + css[end:]
        print("Fuzzy replace done")
    else:
        print(f"Could not find section: start={start}, end={end}")

css_path.write_text(css, encoding='utf-8')
print(f"CSS written: {len(css)} chars")
