# -*- coding: utf-8 -*-
"""Write the complete premium Apple/Samsung-style CSS design system."""
from pathlib import Path

css = r"""/* ============================================================
   TECH STORE AI — Apple Store / Samsung Premium Design
   Premium | Minimal | Futuristic
   ============================================================ */

/* ── DESIGN TOKENS ── */
:root {
  --blue:       #0071E3;
  --blue-hover: #0077ED;
  --blue-light: #2997FF;
  --blue-pale:  #F5F9FF;
  --blue-glow:   rgba(0,113,227,.12);

  --indigo:     #5856D6;
  --emerald:    #34C759;
  --rose:       #FF3B30;
  --orange:     #FF9500;

  --bg:         #FAFAFA;
  --bg-white:   #FFFFFF;
  --bg-card:    #FFFFFF;
  --bg-hover:   #F5F5F7;

  --text:       #1D1D1F;
  --text-sec:   #86868B;
  --text-link:  #0071E3;

  --border:     #D2D2D7;
  --border-sub: #E8E8ED;

  --shadow-card: 0 1px 3px rgba(0,0,0,.06), 0 4px 16px rgba(0,0,0,.04);
  --shadow-hover: 0 8px 32px rgba(0,0,0,.10), 0 2px 8px rgba(0,0,0,.06);
  --shadow-deep:  0 24px 80px rgba(0,0,0,.14);

  --radius-sm:  8px;
  --radius-md:  12px;
  --radius-lg:  18px;
  --radius-xl:  24px;
  --radius-2xl: 32px;
  --radius-full: 9999px;

  --trans:    all .25s cubic-bezier(.4,0,.2,1);
  --trans-fast: all .15s ease;
  --trans-slow: all .4s cubic-bezier(.4,0,.2,1);

  --container: 1200px;
  --header-h: 52px;
  --nav-h: 44px;
}

/* ── RESET & BASE ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  font-family: 'Inter', -apple-system, 'Be Vietnam Pro', BlinkMacSystemFont, sans-serif;
  font-size: 15px;
  line-height: 1.6;
  color: var(--text);
  background: var(--bg);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
  -webkit-text-size-adjust: 100%;
}
h1,h2,h3,h4,h5,h6 {
  font-family: 'Inter', -apple-system, 'Be Vietnam Pro', BlinkMacSystemFont, sans-serif;
  font-weight: 600;
  line-height: 1.2;
  color: var(--text);
}
a { text-decoration: none; color: var(--text-link); transition: var(--trans-fast); }
a:hover { color: var(--blue-hover); }
img { max-width: 100%; height: auto; display: block; }
button { font-family: inherit; cursor: pointer; }
::selection { background: rgba(0,113,227,.15); color: var(--blue); }
:focus-visible { outline: 2px solid var(--blue); outline-offset: 2px; border-radius: 4px; }
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-sec); }

/* Layout */
.container { max-width: var(--container); margin: 0 auto; padding: 0 24px; }

/* ============================================================
   NAVIGATION BAR
   ============================================================ */
.nav-bar {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: rgba(255,255,255,.8);
  backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  border-bottom: 1px solid var(--border-sub);
  transition: box-shadow .3s ease;
}
.nav-bar.scrolled {
  box-shadow: 0 2px 12px rgba(0,0,0,.06);
}
.nav-inner {
  max-width: var(--container);
  margin: 0 auto;
  padding: 0 24px;
  height: var(--header-h);
  display: flex;
  align-items: center;
  gap: 0;
}

/* Logo */
.nav-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  flex-shrink: 0;
  margin-right: 24px;
}
.nav-logo-icon {
  width: 32px; height: 32px;
  background: linear-gradient(135deg, var(--blue), #0050B3);
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: .95rem;
  transition: transform .2s ease;
}
.nav-logo:hover .nav-logo-icon { transform: scale(1.06); }
.nav-logo-name {
  font-size: 1rem; font-weight: 700; color: var(--text);
  letter-spacing: -.4px;
}

/* Nav Links */
.nav-links {
  display: flex;
  align-items: center;
  list-style: none;
  margin: 0; padding: 0;
  gap: 2px;
  flex: 1;
}
.nav-link {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 6px 13px;
  color: var(--text);
  font-size: .8rem; font-weight: 500;
  border-radius: var(--radius-sm);
  transition: background .15s, color .15s;
  text-decoration: none;
  white-space: nowrap;
}
.nav-link:hover { background: var(--bg-hover); color: var(--blue); }
.nav-link.ai { color: var(--blue); font-weight: 600; }
.nav-link.new { color: var(--emerald); font-weight: 600; }
.nav-link.hot { color: var(--rose); font-weight: 600; }

/* Nav actions */
.nav-actions {
  display: flex;
  align-items: center;
  gap: 4px;
  flex-shrink: 0;
}
.nav-action {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  border-radius: var(--radius-sm);
  font-size: .78rem; font-weight: 500;
  color: var(--text);
  transition: background .15s, color .15s;
  text-decoration: none;
  position: relative;
}
.nav-action:hover { background: var(--bg-hover); color: var(--blue); }
.nav-action-icon { font-size: 1.1rem; }
.nav-action-badge {
  position: absolute;
  top: 2px; right: 2px;
  background: var(--rose);
  color: #fff; font-size: .52rem; font-weight: 700;
  min-width: 16px; height: 16px;
  border-radius: var(--radius-full);
  display: flex; align-items: center; justify-content: center;
  padding: 0 4px;
  border: 2px solid var(--bg-white);
}
.nav-action-label { font-size: .72rem; color: var(--text-sec); }
.nav-action:hover .nav-action-label { color: var(--blue); }

/* User dropdown */
.nav-user { position: relative; }
.nav-user-drop {
  position: absolute; top: calc(100% + 8px); right: 0;
  background: var(--bg-white);
  border: 1px solid var(--border-sub);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-deep);
  min-width: 210px;
  padding: 6px 0;
  z-index: 1001;
  display: none;
}
.nav-user-drop.show { display: block; animation: dropIn .2s ease; }
@keyframes dropIn { from{opacity:0;transform:translateY(-6px)} to{opacity:1;transform:translateY(0)} }
.nav-drop-item {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 16px;
  font-size: .85rem; font-weight: 500;
  color: var(--text);
  transition: background .12s;
  text-decoration: none;
}
.nav-drop-item:hover { background: var(--bg-hover); color: var(--blue); }
.nav-drop-item i { width: 18px; color: var(--text-sec); text-align: center; }
.nav-drop-item.danger { color: var(--rose); }
.nav-drop-item.danger:hover { background: #FFF5F5; color: var(--rose); }
.nav-drop-divider { height: 1px; background: var(--border-sub); margin: 6px 0; }

/* ============================================================
   HERO
   ============================================================ */
.hero {
  background: linear-gradient(160deg, #0A0A14 0%, #1A1A3E 40%, #0F1629 100%);
  padding: 60px 0 72px;
  position: relative;
  overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute; inset: 0;
  background:
    radial-gradient(ellipse 80% 50% at 50% -10%, rgba(0,113,227,.25) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 60%, rgba(88,86,214,.1) 0%, transparent 50%),
    radial-gradient(ellipse 40% 30% at 20% 80%, rgba(0,113,227,.08) 0%, transparent 50%);
}
.hero::after {
  content: '';
  position: absolute; bottom: -1px; left: 0; right: 0;
  height: 60px;
  background: linear-gradient(to bottom, transparent, var(--bg));
}
.hero-inner {
  max-width: var(--container);
  margin: 0 auto;
  padding: 0 24px;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 48px;
  align-items: center;
  position: relative; z-index: 1;
}
.hero-content {}
.hero-eyebrow {
  display: inline-flex; align-items: center; gap: 8px;
  color: var(--blue-light); font-size: .72rem; font-weight: 700;
  letter-spacing: 1.5px; text-transform: uppercase;
  margin-bottom: 16px;
}
.hero-eyebrow i { font-size: .7rem; }
.hero-title {
  font-size: 3.2rem; font-weight: 700; color: #fff;
  line-height: 1.1; letter-spacing: -.8px;
  margin-bottom: 16px;
}
.hero-title em { font-style: normal; color: var(--blue-light); }
.hero-desc {
  font-size: 1rem; color: rgba(255,255,255,.55);
  line-height: 1.7; margin-bottom: 32px; max-width: 440px;
}
.hero-btns { display: flex; gap: 12px; flex-wrap: wrap; }
.hero-btn {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 12px 24px;
  border-radius: var(--radius-full);
  font-size: .9rem; font-weight: 600;
  font-family: inherit; border: none; cursor: pointer;
  transition: var(--trans);
  text-decoration: none;
}
.hero-btn-primary {
  background: var(--blue); color: #fff;
  box-shadow: 0 4px 16px rgba(0,113,227,.35);
}
.hero-btn-primary:hover {
  background: var(--blue-hover);
  transform: translateY(-1px);
  box-shadow: 0 6px 24px rgba(0,113,227,.45);
}
.hero-btn-secondary {
  background: rgba(255,255,255,.08);
  color: #fff;
  border: 1.5px solid rgba(255,255,255,.2);
  backdrop-filter: blur(4px);
}
.hero-btn-secondary:hover {
  background: rgba(255,255,255,.14);
  border-color: rgba(255,255,255,.35);
  transform: translateY(-1px);
}
.hero-visual {
  flex-shrink: 0; width: 320px;
  display: flex; flex-direction: column; gap: 16px;
}
.hero-product-card {
  background: rgba(255,255,255,.06);
  border: 1px solid rgba(255,255,255,.1);
  border-radius: var(--radius-xl);
  padding: 28px;
  backdrop-filter: blur(16px);
  text-align: center;
  animation: hero-float 6s ease-in-out infinite;
}
@keyframes hero-float {
  0%,100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}
.hero-product-img {
  width: 160px; height: 160px; margin: 0 auto 16px;
  background: rgba(255,255,255,.06);
  border-radius: var(--radius-lg);
  display: flex; align-items: center; justify-content: center;
}
.hero-product-img i { font-size: 3.5rem; color: rgba(255,255,255,.25); }
.hero-product-name { font-size: .9rem; font-weight: 600; color: #fff; margin-bottom: 4px; }
.hero-product-rating { color: #FFD60A; font-size: .78rem; margin-bottom: 8px; }
.hero-product-price { font-size: 1.1rem; font-weight: 700; color: #FFD60A; }
.hero-product-orig { font-size: .8rem; color: rgba(255,255,255,.35); text-decoration: line-through; }
.hero-product-btn {
  display: inline-flex; align-items: center; gap: 6px;
  background: var(--blue); color: #fff;
  padding: 9px 18px; border-radius: var(--radius-full);
  font-size: .78rem; font-weight: 600; border: none;
  cursor: pointer; margin-top: 12px;
  font-family: inherit; transition: var(--trans);
  text-decoration: none;
}
.hero-product-btn:hover { background: var(--blue-hover); transform: scale(1.04); }

/* ============================================================
   SECTION WRAPPER
   ============================================================ */
.section { padding: 56px 0; }
.section-alt { background: var(--bg-white); }
.section-header {
  display: flex; align-items: flex-end;
  justify-content: space-between;
  margin-bottom: 28px; gap: 16px;
}
.section-label {
  font-size: .68rem; font-weight: 700; color: var(--blue);
  text-transform: uppercase; letter-spacing: 2px;
  margin-bottom: 4px;
}
.section-title {
  font-size: 1.5rem; font-weight: 700;
  color: var(--text); line-height: 1.2; letter-spacing: -.4px;
}
.section-link {
  display: inline-flex; align-items: center; gap: 6px;
  color: var(--blue); font-size: .82rem; font-weight: 600;
  text-decoration: none; white-space: nowrap;
  transition: gap .2s;
}
.section-link:hover { gap: 10px; color: var(--blue-hover); }

/* ============================================================
   TRUST BADGES
   ============================================================ */
.trust-grid {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px;
}
.trust-card {
  display: flex; align-items: center; gap: 14px;
  padding: 16px 18px;
  background: var(--bg-white);
  border: 1px solid var(--border-sub);
  border-radius: var(--radius-md);
  transition: var(--trans);
}
.trust-card:hover {
  border-color: var(--blue-light);
  box-shadow: var(--shadow-card);
  transform: translateY(-1px);
}
.trust-icon {
  width: 44px; height: 44px; border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.1rem; flex-shrink: 0;
}
.trust-icon.blue { background: var(--blue-pale); color: var(--blue); }
.trust-icon.green { background: #F0FDF4; color: var(--emerald); }
.trust-icon.amber { background: #FFFBEB; color: var(--orange); }
.trust-icon.purple { background: #F5F3FF; color: var(--indigo); }
.trust-title { font-size: .85rem; font-weight: 700; color: var(--text); margin-bottom: 2px; }
.trust-desc { font-size: .72rem; color: var(--text-sec); }

/* ============================================================
   CATEGORIES
   ============================================================ */
.cat-grid {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px;
}
.cat-card {
  background: var(--bg-white);
  border: 1px solid var(--border-sub);
  border-radius: var(--radius-lg);
  padding: 24px 16px;
  text-align: center; text-decoration: none;
  transition: var(--trans);
  display: block;
}
.cat-card:hover {
  border-color: var(--blue-light);
  box-shadow: var(--shadow-hover);
  transform: translateY(-3px);
}
.cat-icon {
  width: 56px; height: 56px; margin: 0 auto 14px;
  background: var(--blue-pale);
  border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.4rem; color: var(--blue);
  transition: var(--trans);
}
.cat-card:hover .cat-icon {
  background: var(--blue);
  color: #fff;
  transform: scale(1.08);
  box-shadow: 0 4px 16px rgba(0,113,227,.3);
}
.cat-name { font-size: .85rem; font-weight: 600; color: var(--text); margin-bottom: 2px; }
.cat-count { font-size: .72rem; color: var(--text-sec); }

/* ============================================================
   PRODUCT TABS
   ============================================================ */
.tabs {
  display: inline-flex; gap: 4px;
  background: var(--bg-white);
  border: 1px solid var(--border-sub);
  padding: 4px;
  border-radius: var(--radius-full);
  margin-bottom: 28px;
}
.tab-btn {
  padding: 8px 20px;
  border-radius: var(--radius-full);
  border: none; background: transparent;
  color: var(--text-sec);
  font-size: .82rem; font-weight: 600;
  font-family: inherit; cursor: pointer;
  transition: var(--trans);
  display: flex; align-items: center; gap: 6px;
}
.tab-btn.active { background: var(--text); color: #fff; }
.tab-btn:not(.active):hover { color: var(--text); background: var(--bg-hover); }
.tab-content { display: none; }
.tab-content.active { display: block; }

/* ============================================================
   PRODUCT CARDS — Apple Store Style
   ============================================================ */
.products-grid {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px;
}
.product-card {
  background: var(--bg-white);
  border: 1px solid var(--border-sub);
  border-radius: var(--radius-lg);
  overflow: hidden;
  transition: var(--trans);
  display: flex; flex-direction: column;
  position: relative;
}
.product-card:hover {
  border-color: rgba(0,113,227,.25);
  box-shadow: var(--shadow-hover);
  transform: translateY(-4px);
}
.product-img {
  position: relative;
  background: var(--bg);
  padding: 20px;
  text-align: center;
  min-height: 180px;
  display: flex; align-items: center; justify-content: center;
  overflow: hidden;
}
.product-img img {
  max-height: 130px; max-width: 100%; object-fit: contain;
  transition: transform .4s ease;
}
.product-card:hover .product-img img { transform: scale(1.05); }
.product-badge {
  position: absolute; top: 10px; left: 10px;
  padding: 3px 9px;
  border-radius: 6px;
  font-size: .65rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: .3px;
}
.badge-new { background: var(--emerald); color: #fff; }
.badge-hot { background: var(--rose); color: #fff; }
.badge-sale { background: var(--orange); color: #fff; }
.product-discount {
  position: absolute; top: 10px; right: 10px;
  background: var(--rose); color: #fff;
  font-size: .65rem; font-weight: 800;
  padding: 3px 8px; border-radius: 6px;
}
.product-body {
  padding: 14px 16px 16px;
  flex: 1; display: flex; flex-direction: column;
}
.product-name {
  font-size: .85rem; font-weight: 600; color: var(--text);
  line-height: 1.4; margin-bottom: 6px;
  display: -webkit-box; -webkit-line-clamp: 2;
  -webkit-box-orient: vertical; overflow: hidden;
  text-decoration: none; transition: color .15s;
}
.product-name:hover { color: var(--blue); }
.product-rating {
  display: flex; align-items: center; gap: 4px; margin-bottom: 10px;
  font-size: .72rem;
}
.product-stars { color: #FFD60A; letter-spacing: -1px; }
.product-reviews { color: var(--text-sec); }
.product-price-wrap { margin-bottom: 10px; }
.product-price {
  font-size: 1.05rem; font-weight: 700; color: var(--text);
}
.product-price-orig {
  font-size: .75rem; color: var(--text-sec);
  text-decoration: line-through; margin-left: 6px;
}
.product-add-btn {
  margin-top: auto;
  display: flex; align-items: center; justify-content: center; gap: 7px;
  background: var(--blue); color: #fff;
  border: none; padding: 10px;
  border-radius: var(--radius-md);
  font-size: .8rem; font-weight: 600;
  font-family: inherit; cursor: pointer;
  transition: var(--trans);
  text-decoration: none;
}
.product-add-btn:hover {
  background: var(--blue-hover);
  box-shadow: 0 4px 14px rgba(0,113,227,.35);
  transform: translateY(-1px);
}
.product-empty {
  grid-column: 1 / -1; text-align: center;
  padding: 60px 20px; color: var(--text-sec);
}
.product-empty i { font-size: 2.5rem; margin-bottom: 10px; color: var(--border); }

/* ============================================================
   WHY US
   ============================================================ */
.why-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.why-card {
  padding: 28px 22px;
  background: var(--bg-white);
  border: 1px solid var(--border-sub);
  border-radius: var(--radius-xl);
  text-align: center;
  transition: var(--trans);
}
.why-card:hover {
  border-color: rgba(0,113,227,.2);
  box-shadow: var(--shadow-hover);
  transform: translateY(-3px);
}
.why-icon {
  width: 56px; height: 56px; margin: 0 auto 16px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.3rem;
}
.why-icon.blue { background: var(--blue-pale); color: var(--blue); }
.why-icon.green { background: #F0FDF4; color: var(--emerald); }
.why-icon.amber { background: #FFFBEB; color: var(--orange); }
.why-icon.purple { background: #F5F3FF; color: var(--indigo); }
.why-icon.rose { background: #FFF1F2; color: var(--rose); }
.why-icon.dark { background: #F5F5F7; color: var(--text); }
.why-title { font-size: .95rem; font-weight: 700; color: var(--text); margin-bottom: 8px; }
.why-desc { font-size: .82rem; color: var(--text-sec); line-height: 1.6; }

/* ============================================================
   SUPPORT BANNER
   ============================================================ */
.support-banner {
  background: var(--text);
  padding: 60px 0;
  text-align: center;
  position: relative; overflow: hidden;
}
.support-banner::before {
  content: '';
  position: absolute; inset: 0;
  background:
    radial-gradient(ellipse 50% 80% at 50% 0%, rgba(0,113,227,.2) 0%, transparent 60%);
}
.support-title {
  font-size: 2rem; font-weight: 700; color: #fff;
  margin-bottom: 8px; position: relative; z-index: 1;
}
.support-sub {
  font-size: 1rem; color: rgba(255,255,255,.5);
  margin-bottom: 24px; position: relative; z-index: 1;
}
.support-hotline {
  font-size: 2rem; font-weight: 800; color: var(--blue-light);
  margin-bottom: 28px; position: relative; z-index: 1;
  letter-spacing: -.5px;
}
.support-btns { display: flex; justify-content: center; gap: 14px; flex-wrap: wrap; position: relative; z-index: 1; }
.support-btn {
  display: inline-flex; align-items: center; gap: 10px;
  padding: 13px 28px; border-radius: var(--radius-full);
  font-size: .9rem; font-weight: 600;
  font-family: inherit; cursor: pointer;
  transition: var(--trans); text-decoration: none;
}
.support-btn-phone { background: #fff; color: var(--text); border: none; }
.support-btn-phone:hover { background: var(--blue); color: #fff; transform: translateY(-1px); }
.support-btn-chat {
  background: transparent; color: #fff;
  border: 2px solid rgba(255,255,255,.25);
}
.support-btn-chat:hover { background: rgba(255,255,255,.08); border-color: rgba(255,255,255,.5); transform: translateY(-1px); }

/* ============================================================
   FOOTER
   ============================================================ */
.site-footer {
  background: var(--bg-white);
  border-top: 1px solid var(--border-sub);
  padding: 48px 0 0;
}
.footer-grid {
  display: grid;
  grid-template-columns: 1.6fr 1fr 1fr 1fr;
  gap: 40px;
  padding-bottom: 40px;
}
.footer-brand {
  display: flex; align-items: center; gap: 10px;
  margin-bottom: 14px; text-decoration: none;
}
.footer-brand-icon {
  width: 34px; height: 34px;
  background: linear-gradient(135deg, var(--blue), #0050B3);
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: .9rem;
}
.footer-brand-name { font-size: 1rem; font-weight: 700; color: var(--text); }
.footer-desc { font-size: .82rem; color: var(--text-sec); line-height: 1.65; margin-bottom: 14px; }
.footer-socials { display: flex; gap: 6px; }
.footer-social {
  width: 34px; height: 34px;
  background: var(--bg);
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  color: var(--text-sec); font-size: .88rem;
  transition: var(--trans-fast); text-decoration: none;
}
.footer-social:hover { background: var(--blue); color: #fff; }
.footer-col-title {
  font-size: .78rem; font-weight: 700; color: var(--text);
  margin-bottom: 12px; text-transform: uppercase; letter-spacing: .5px;
}
.footer-links { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 8px; }
.footer-links li a {
  color: var(--text-sec); font-size: .82rem;
  display: flex; align-items: center; gap: 5px;
  transition: var(--trans-fast); text-decoration: none;
}
.footer-links li a:hover { color: var(--blue); }
.footer-links li a i { font-size: .55rem; color: var(--blue-light); }
.footer-contact-item {
  display: flex; align-items: flex-start; gap: 10px;
  margin-bottom: 10px; font-size: .82rem;
}
.footer-contact-item i { color: var(--blue); margin-top: 2px; width: 14px; text-align: center; }
.footer-bottom {
  border-top: 1px solid var(--border-sub);
  padding: 16px 0;
  display: flex; align-items: center;
  justify-content: space-between; flex-wrap: wrap; gap: 10px;
}
.footer-copyright { font-size: .75rem; color: var(--text-sec); }
.footer-payments { display: flex; gap: 6px; align-items: center; }
.footer-payment {
  width: 38px; height: 24px;
  background: var(--bg);
  border-radius: 4px;
  display: flex; align-items: center;
  justify-content: center;
  font-size: .6rem; color: var(--text-sec);
  font-weight: 700;
}

/* ============================================================
   AI CHATBOT WIDGET — Apple-style glassmorphism
   ============================================================ */
.cb-toggle {
  position: fixed; bottom: 28px; right: 28px; z-index: 9999;
  width: 58px; height: 58px; border-radius: 50%;
  background: rgba(0,113,227,.92);
  backdrop-filter: blur(20px);
  border: none; color: #fff; font-size: 1.3rem;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
  box-shadow: 0 6px 24px rgba(0,113,227,.45), 0 0 0 1px rgba(0,113,227,.3);
  transition: transform .25s ease, box-shadow .25s ease;
}
.cb-toggle:hover {
  transform: scale(1.1);
  box-shadow: 0 10px 36px rgba(0,113,227,.55), 0 0 0 1px rgba(0,113,227,.4);
}
.cb-toggle .badge-dot {
  position: absolute; top: 5px; right: 5px;
  width: 12px; height: 12px;
  background: var(--emerald); border-radius: 50%;
  border: 2.5px solid var(--bg-white);
}
.cb-popup {
  position: fixed; bottom: 100px; right: 28px; z-index: 9998;
  width: 380px; max-height: 560px;
  border-radius: var(--radius-xl);
  background: rgba(255,255,255,.96);
  backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(0,113,227,.12);
  box-shadow: var(--shadow-deep);
  display: none; flex-direction: column;
  overflow: hidden;
  animation: cb-in .3s cubic-bezier(.4,0,.2,1);
  font-family: 'Inter', sans-serif;
}
.cb-popup.active { display: flex; }
@keyframes cb-in { from{opacity:0;transform:translateY(16px) scale(.96)} to{opacity:1;transform:translateY(0) scale(1)} }
.cb-hdr {
  background: linear-gradient(135deg, #001B44, var(--blue));
  color: #fff; padding: 16px 18px;
  display: flex; align-items: center; gap: 12px; flex-shrink: 0;
}
.cb-hdr-icon {
  width: 40px; height: 40px;
  background: rgba(255,255,255,.15);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.1rem;
  flex-shrink: 0;
}
.cb-hdr-info { flex: 1; }
.cb-hdr-info h6 { margin: 0; font-weight: 700; font-size: .9rem; }
.cb-hdr-info small { opacity: .7; font-size: .72rem; }
.cb-hdr-actions { display: flex; gap: 5px; }
.cb-hdr-actions button {
  background: rgba(255,255,255,.12); border: none; color: #fff;
  width: 32px; height: 32px; border-radius: 50%;
  cursor: pointer; display: flex; align-items: center; justify-content: center;
  font-size: .8rem; transition: background .15s;
}
.cb-hdr-actions button:hover { background: rgba(255,255,255,.22); }
.cb-msgs {
  flex: 1; overflow-y: auto; padding: 14px;
  background: #F5F5F7;
  min-height: 260px; max-height: 380px;
}
.cb-msg { display: flex; margin-bottom: 12px; animation: cb-msg .25s ease; }
@keyframes cb-msg { from{opacity:0;transform:translateY(6px)} to{opacity:1;transform:translateY(0)} }
.cb-msg.user { flex-direction: row-reverse; }
.cb-avatar {
  width: 30px; height: 30px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: .72rem; flex-shrink: 0; margin: 0 7px;
}
.cb-msg.bot .cb-avatar { background: var(--blue-pale); color: var(--blue); }
.cb-msg.user .cb-avatar { background: var(--blue); color: #fff; }
.cb-bubble {
  max-width: 78%; padding: 10px 13px;
  border-radius: 14px;
  font-size: .82rem; line-height: 1.55; word-wrap: break-word;
}
.cb-msg.bot .cb-bubble {
  background: #fff; color: var(--text);
  border-bottom-left-radius: 4px;
  box-shadow: 0 1px 3px rgba(0,0,0,.06);
}
.cb-msg.user .cb-bubble {
  background: var(--blue); color: #fff;
  border-bottom-right-radius: 4px;
}
.cb-bubble p { margin: 0 0 4px; }
.cb-bubble p:last-child { margin-bottom: 0; }
.cb-bubble strong { font-weight: 600; }
.cb-time { font-size: .65rem; color: var(--text-sec); margin-top: 3px; padding: 0 3px; }
.cb-msg.user .cb-time { text-align: right; }
.cb-typing .cb-bubble { padding: 12px 16px; }
.cb-dots { display: flex; gap: 3px; align-items: center; }
.cb-dots span {
  width: 6px; height: 6px; background: var(--text-sec);
  border-radius: 50%; animation: cb-bounce 1.3s infinite;
}
.cb-dots span:nth-child(2){animation-delay:.18s}
.cb-dots span:nth-child(3){animation-delay:.36s}
@keyframes cb-bounce { 0%,60%,100%{transform:translateY(0)} 30%{transform:translateY(-5px)} }
.cb-quick {
  padding: 9px 12px;
  border-top: 1px solid var(--border-sub);
  background: #fff;
  display: flex; flex-wrap: wrap; gap: 5px;
  flex-shrink: 0;
}
.cb-quick-btn {
  padding: 5px 11px;
  font-size: .7rem; border-radius: var(--radius-full);
  border: 1.5px solid rgba(0,113,227,.2); color: var(--blue);
  background: #fff;
  cursor: pointer; font-family: inherit; font-weight: 600;
  transition: var(--trans-fast);
}
.cb-quick-btn:hover { background: var(--blue); color: #fff; border-color: var(--blue); }
.cb-input {
  padding: 11px 12px;
  border-top: 1px solid var(--border-sub);
  background: #fff;
  display: flex; gap: 7px; align-items: center; flex-shrink: 0;
}
.cb-input input {
  flex: 1;
  border: 1.5px solid var(--border);
  border-radius: var(--radius-full);
  padding: 9px 16px; font-size: .82rem; outline: none;
  font-family: inherit; transition: border-color .2s;
  background: var(--bg);
}
.cb-input input:focus { border-color: var(--blue); background: #fff; }
.cb-send {
  width: 38px; height: 38px; border-radius: 50%; border: none;
  background: var(--blue); color: #fff;
  cursor: pointer; display: flex; align-items: center; justify-content: center;
  font-size: .82rem; transition: var(--trans-fast);
  flex-shrink: 0;
}
.cb-send:hover { background: var(--blue-hover); transform: scale(1.06); }
.cb-send:disabled { opacity: .4; cursor: not-allowed; transform: none; }

/* ============================================================
   TOAST NOTIFICATIONS
   ============================================================ */
#toast-container {
  position: fixed;
  top: 70px; right: 20px;
  z-index: 99999;
  display: flex; flex-direction: column;
  gap: 8px; pointer-events: none;
}
.ts-toast {
  display: flex; align-items: center; gap: 11px;
  padding: 13px 16px;
  background: rgba(255,255,255,.96);
  backdrop-filter: blur(12px);
  border-radius: var(--radius-md);
  box-shadow: 0 4px 24px rgba(0,0,0,.1), 0 1px 4px rgba(0,0,0,.06);
  pointer-events: all;
  max-width: 340px; min-width: 260px;
  transform: translateX(120%);
  opacity: 0;
  transition: all .35s cubic-bezier(.4,0,.2,1);
  border: 1px solid var(--border-sub);
}
.ts-toast--in { transform: translateX(0); opacity: 1; }
.ts-toast--out { transform: translateX(120%); opacity: 0; }
.ts-toast--success { border-left: 4px solid var(--emerald); }
.ts-toast--danger  { border-left: 4px solid var(--rose); }
.ts-toast--warning { border-left: 4px solid var(--orange); }
.ts-toast--info    { border-left: 4px solid var(--blue); }
.ts-toast__content { display: flex; align-items: center; gap: 9px; flex: 1; }
.ts-toast__icon { font-size: 1rem; display: flex; align-items: center; }
.ts-toast--success .ts-toast__icon { color: var(--emerald); }
.ts-toast--danger  .ts-toast__icon { color: var(--rose); }
.ts-toast--warning .ts-toast__icon { color: var(--orange); }
.ts-toast--info    .ts-toast__icon { color: var(--blue); }
.ts-toast__message { font-size: .82rem; font-weight: 500; color: var(--text); line-height: 1.4; }
.ts-toast__close {
  background: none; border: none; cursor: pointer;
  color: var(--text-sec); font-size: .82rem; padding: 4px;
  display: flex; align-items: center;
  transition: color .15s; flex-shrink: 0;
}
.ts-toast__close:hover { color: var(--text); }

/* ============================================================
   PAGINATION
   ============================================================ */
.pagination { display: flex; justify-content: center; gap: 5px; margin-top: 32px; flex-wrap: wrap; }
.page-btn {
  min-width: 36px; height: 36px;
  border-radius: var(--radius-sm);
  border: 1.5px solid var(--border-sub);
  background: var(--bg-white); color: var(--text);
  font-size: .82rem; font-weight: 600;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; transition: var(--trans-fast);
  text-decoration: none; padding: 0 10px;
  font-family: inherit;
}
.page-btn.active, .page-btn:hover {
  background: var(--blue); color: #fff;
  border-color: var(--blue);
  box-shadow: 0 3px 10px rgba(0,113,227,.25);
}

/* ============================================================
   RESPONSIVE
   ============================================================ */
@media (max-width: 1024px) {
  .hero-inner { grid-template-columns: 1fr; gap: 32px; }
  .hero-visual { width: 100%; max-width: 340px; margin: 0 auto; }
  .hero-title { font-size: 2.4rem; }
  .trust-grid { grid-template-columns: repeat(2, 1fr); }
  .cat-grid { grid-template-columns: repeat(3, 1fr); }
  .products-grid { grid-template-columns: repeat(3, 1fr); }
  .why-grid { grid-template-columns: repeat(2, 1fr); }
  .footer-grid { grid-template-columns: repeat(2, 1fr); gap: 28px; }
}
@media (max-width: 768px) {
  .nav-logo-name { display: none; }
  .nav-link { padding: 6px 10px; font-size: .78rem; }
  .nav-action-label { display: none; }
  .hero { padding: 48px 0 56px; }
  .hero-title { font-size: 2rem; }
  .hero-desc { font-size: .95rem; }
  .section { padding: 44px 0; }
  .section-title { font-size: 1.3rem; }
  .trust-grid { grid-template-columns: repeat(2, 1fr); }
  .cat-grid { grid-template-columns: repeat(3, 1fr); }
  .products-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
  .why-grid { grid-template-columns: 1fr; }
  .footer-grid { grid-template-columns: 1fr 1fr; gap: 24px; }
  .footer-bottom { flex-direction: column; text-align: center; }
  .cb-popup { width: calc(100vw - 24px); right: 12px; bottom: 88px; max-height: 65vh; }
}
@media (max-width: 480px) {
  .nav-inner { padding: 0 12px; }
  .nav-link:not(.ai):not(.new):not(.hot) { display: none; }
  .hero-title { font-size: 1.7rem; }
  .hero-btns { flex-direction: column; }
  .hero-btn { justify-content: center; }
  .cat-grid { grid-template-columns: repeat(2, 1fr); }
  .trust-grid { grid-template-columns: 1fr; }
  .footer-grid { grid-template-columns: 1fr; gap: 20px; }
  .products-grid { grid-template-columns: repeat(2, 1fr); gap: 10px; }
}
"""

p = Path(r"d:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3\wwwroot\css\style.css")
p.write_text(css, encoding='utf-8')
print(f"CSS written: {len(css)} chars")
