"""
ReliefLink AI — Streamlit Frontend (Redesigned)
Black / White / Red minimal theme — Magazine serif typography.
"""
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# ─────────────────────────────────────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ReliefLink AI | Crisis Awareness Platform",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS — Black / White Minimal + Playfair Display Magazine Theme
# ─────────────────────────────────────────────────────────────────────────────
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;0,800;1,400;1,600&family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, .stDeployButton { visibility: hidden !important; }

/* ── Base ── */
.stApp {
    background: #0A0A0A !important;
    color: #E8E8E8 !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #111111 !important;
    border-right: 1px solid #222222 !important;
}
section[data-testid="stSidebar"] .stRadio label {
    color: #999999 !important;
    font-size: 0.85rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.3px !important;
    padding: 5px 0 !important;
    cursor: pointer !important;
    transition: color 0.15s !important;
}
section[data-testid="stSidebar"] .stRadio label:hover { color: #FFFFFF !important; }
section[data-testid="stSidebar"] [aria-checked="true"] + label,
section[data-testid="stSidebar"] [data-checked="true"] label { color: #FFFFFF !important; }

/* ── Buttons ── */
.stButton > button {
    background: #FFFFFF !important;
    color: #0A0A0A !important;
    border: none !important;
    border-radius: 4px !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
    transition: background 0.15s, transform 0.1s !important;
    padding: 8px 16px !important;
}
.stButton > button:hover {
    background: #E8E8E8 !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="secondary"] {
    background: #1A1A1A !important;
    color: #AAAAAA !important;
    border: 1px solid #333333 !important;
}
.stButton > button[kind="secondary"]:hover {
    background: #222222 !important;
    color: #FFFFFF !important;
}

/* ── Preset region chips ── */
.stButton > button.preset-btn {
    background: #1A1A1A !important;
    color: #CCCCCC !important;
    border: 1px solid #333333 !important;
    font-size: 0.75rem !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
    padding: 5px 12px !important;
}

/* ── Text inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #111111 !important;
    border: 1px solid #2A2A2A !important;
    border-radius: 4px !important;
    color: #E8E8E8 !important;
    font-size: 0.88rem !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #555555 !important;
    box-shadow: none !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder { color: #555 !important; }

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: #111111 !important;
    border: 1px solid #2A2A2A !important;
    border-radius: 4px !important;
    color: #E8E8E8 !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #111111 !important;
    border-radius: 4px !important;
    padding: 3px !important;
    gap: 2px !important;
    border: 1px solid #222 !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 3px !important;
    color: #777777 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.3px !important;
}
.stTabs [aria-selected="true"] {
    background: #222222 !important;
    color: #FFFFFF !important;
}

/* ── Form ── */
.stForm {
    background: #0F0F0F !important;
    border: 1px solid #1E1E1E !important;
    border-radius: 6px !important;
    padding: 24px !important;
}

/* ── Multiselect ── */
.stMultiSelect > div {
    background: #111111 !important;
    border: 1px solid #2A2A2A !important;
    border-radius: 4px !important;
}
.stMultiSelect span[data-baseweb="tag"] {
    background: #222222 !important;
    border: 1px solid #333 !important;
    color: #CCC !important;
}

/* ── Checkbox ── */
.stCheckbox label { color: #AAAAAA !important; font-size: 0.85rem !important; }

/* ── Success / Error / Info ── */
.stSuccess { background: #0F1F0F !important; border: 1px solid #2A5A2A !important; border-radius: 6px !important; }
.stError   { background: #1A0A0A !important; border: 1px solid #5A2A2A !important; border-radius: 6px !important; }
.stInfo    { background: #111111 !important; border: 1px solid #333 !important; border-radius: 6px !important; }

/* ── Divider ── */
hr { border-color: #1E1E1E !important; margin: 12px 0 !important; }

/* ── Spinner ── */
.stSpinner > div { color: #FFFFFF !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0A0A0A; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 2px; }

/* ── Playfair headlines ── */
.pf { font-family: 'Playfair Display', Georgia, serif !important; }

/* ── Urgency labels ── */
.urgency-high {
    background: #1A0000;
    border: 1px solid #DC2626;
    color: #DC2626;
    padding: 2px 10px;
    border-radius: 2px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    display: inline-block;
}
.urgency-med {
    background: #111111;
    border: 1px solid #555;
    color: #888;
    padding: 2px 10px;
    border-radius: 2px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    display: inline-block;
}
.urgency-low {
    background: #111111;
    border: 1px solid #333;
    color: #555;
    padding: 2px 10px;
    border-radius: 2px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    display: inline-block;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Session State
# ─────────────────────────────────────────────────────────────────────────────
_DEFAULTS = {
    "page": "🌐 Crisis Feed",
    "carousel_index": 0,
    "crisis_feed": [],
    "chat_history": [],
    "help_requests": [],
    "approved_help_requests": [],
    "blog_content": "",
    "blog_region": "",
    "donor_analysis": None,
    "donor_region_text": "",
    "blog_region_text": "",
    "pending_approval": None,
}
for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────────────────────────────
# API Helper
# ─────────────────────────────────────────────────────────────────────────────
def call_api(endpoint: str, method: str = "GET", data: dict = None, timeout: int = 60) -> dict:
    url = f"{BACKEND_URL}{endpoint}"
    try:
        r = requests.get(url, timeout=timeout) if method == "GET" else requests.post(url, json=data, timeout=timeout)
        return r.json() if r.status_code == 200 else {"error": f"API {r.status_code}: {r.text[:200]}"}
    except requests.exceptions.ConnectionError:
        return {"error": "Backend offline. Run:  uvicorn backend.main:app --reload"}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out — try again shortly."}
    except Exception as exc:
        return {"error": str(exc)}

# ─────────────────────────────────────────────────────────────────────────────
# Utility Renderers
# ─────────────────────────────────────────────────────────────────────────────
def urgency_badge(urgency: str) -> str:
    if urgency == "High":
        return '<span class="urgency-high">ALERT</span>'
    elif urgency == "Medium":
        return '<span class="urgency-med">MEDIUM URGENCY</span>'
    else:
        return '<span class="urgency-low">LOWER URGENCY</span>'


def needs_chips(needs: list) -> str:
    return "".join(
        f'<span style="background:#1A1A1A;border:1px solid #2A2A2A;color:#888888;'
        f'padding:2px 8px;border-radius:2px;font-size:0.68rem;margin:2px;'
        f'display:inline-block;letter-spacing:0.5px;text-transform:uppercase;">{n}</span>'
        for n in needs[:5]
    )


def section_header(title: str, subtitle: str = ""):
    st.markdown(
        f'<h2 class="pf" style="color:#FFFFFF;font-size:1.8rem;font-weight:700;'
        f'margin:0 0 2px 0;letter-spacing:-0.5px;">{title}</h2>'
        + (f'<p style="color:#555555;font-size:0.78rem;letter-spacing:1px;'
           f'text-transform:uppercase;margin:0 0 22px 0;">{subtitle}</p>'
           if subtitle else '<div style="margin-bottom:22px"></div>'),
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        # Masthead
        st.markdown(
            """
            <div style="padding:28px 0 16px;border-bottom:1px solid #1E1E1E;">
                <div style="font-family:'Playfair Display',Georgia,serif;font-size:1.3rem;
                            font-weight:800;color:#FFFFFF;letter-spacing:-0.5px;">ReliefLink AI</div>
                <div style="color:#444444;font-size:0.65rem;letter-spacing:2px;
                            text-transform:uppercase;margin-top:3px;">Crisis Awareness Platform</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        # Navigation
        pages = ["🌐 Crisis Feed", "💰 Donor Hub", "🏥 Physical Aid", "🆘 Help Center", "📰 Crisis Blog"]
        selected = st.radio("Navigate", pages, index=pages.index(st.session_state.page), label_visibility="collapsed")
        st.session_state.page = selected

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        st.divider()

        # AI Chat label
        st.markdown(
            '<div style="color:#666666;font-size:0.7rem;letter-spacing:1.5px;'
            'text-transform:uppercase;margin-bottom:10px;">AI Crisis Assistant</div>',
            unsafe_allow_html=True,
        )

        # Chat history
        for msg in st.session_state.chat_history[-6:]:
            if msg["role"] == "user":
                st.markdown(
                    f'<div style="background:#1A1A1A;border-left:2px solid #444;'
                    f'border-radius:2px;padding:7px 10px;margin:3px 0;font-size:0.76rem;color:#CCCCCC;">'
                    f'{msg["content"]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div style="background:#0F0F0F;border-left:2px solid #DC2626;'
                    f'border-radius:2px;padding:7px 10px;margin:3px 0;font-size:0.76rem;color:#AAAAAA;">'
                    f'{msg["content"]}</div>',
                    unsafe_allow_html=True,
                )

        # Input form
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input("Message", placeholder="How can I help in Sudan?", label_visibility="collapsed")
            send = st.form_submit_button("Send", use_container_width=True)

        if send and user_input.strip():
            st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
            with st.spinner("Thinking..."):
                result = call_api("/api/chat/message", "POST",
                                  {"message": user_input.strip(), "history": st.session_state.chat_history[-4:]},
                                  timeout=30)
            reply = result.get("response", result.get("error", "Unable to respond."))
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

        # Quick suggestions — text only, no emojis
        st.markdown(
            '<div style="color:#333333;font-size:0.65rem;margin:8px 0 4px;letter-spacing:0.5px;">Suggested questions</div>',
            unsafe_allow_html=True,
        )
        for s in ["What is needed in Gaza?", "Best orgs for Sudan?", "How to donate effectively?"]:
            if st.button(s, key=f"s_{s}", use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": s})
                r = call_api("/api/chat/message", "POST", {"message": s, "history": []}, timeout=30)
                st.session_state.chat_history.append({"role": "assistant", "content": r.get("response", "")})
                st.rerun()

        if st.session_state.chat_history:
            if st.button("Clear", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# HEADER — Editorial / Masthead Style
# ─────────────────────────────────────────────────────────────────────────────
def render_header():
    st.markdown(
        """
        <div style="border-top:3px solid #DC2626;border-bottom:1px solid #222;
                    padding:28px 40px 24px;margin-bottom:32px;background:#0D0D0D;">
            <div style="text-align:center;">
                <div style="font-family:'Playfair Display',Georgia,serif;font-size:2.8rem;
                            font-weight:800;color:#FFFFFF;letter-spacing:-1px;line-height:1;">
                    RELIEFLINK AI
                </div>
                <div style="color:#444444;font-size:0.7rem;letter-spacing:3px;
                            text-transform:uppercase;margin:8px 0 20px;">
                    Real-Time Crisis Awareness &amp; Trusted Donation Platform
                </div>
                <div style="display:flex;justify-content:center;gap:48px;flex-wrap:wrap;
                            padding-top:16px;border-top:1px solid #1E1E1E;">
                    <div style="text-align:center;">
                        <div style="color:#DC2626;font-family:'Playfair Display',serif;
                                    font-size:1.8rem;font-weight:700;">12+</div>
                        <div style="color:#444;font-size:0.65rem;letter-spacing:1.5px;
                                    text-transform:uppercase;margin-top:2px;">Active Crises</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="color:#FFFFFF;font-family:'Playfair Display',serif;
                                    font-size:1.8rem;font-weight:700;">850M+</div>
                        <div style="color:#444;font-size:0.65rem;letter-spacing:1.5px;
                                    text-transform:uppercase;margin-top:2px;">People Affected</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="color:#AAAAAA;font-family:'Playfair Display',serif;
                                    font-size:1.8rem;font-weight:700;">48</div>
                        <div style="color:#444;font-size:0.65rem;letter-spacing:1.5px;
                                    text-transform:uppercase;margin-top:2px;">Trusted Orgs</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="color:#AAAAAA;font-family:'Playfair Display',serif;
                                    font-size:1.8rem;font-weight:700;">RAG</div>
                        <div style="color:#444;font-size:0.65rem;letter-spacing:1.5px;
                                    text-transform:uppercase;margin-top:2px;">AI-Powered</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="color:#AAAAAA;font-family:'Playfair Display',serif;
                                    font-size:1.8rem;font-weight:700;">FAISS</div>
                        <div style="color:#444;font-size:0.65rem;letter-spacing:1.5px;
                                    text-transform:uppercase;margin-top:2px;">Vector DB</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 1 — Live Crisis Feed
# ─────────────────────────────────────────────────────────────────────────────
def render_crisis_feed():
    section_header("Live Crisis Feed", "AI-analyzed real-time humanitarian alerts")

    c1, c2, c3 = st.columns([2, 2, 1])
    with c2:
        region_filter = st.selectbox(
            "Filter",
            ["All", "Sudan", "Gaza", "Ukraine", "Haiti", "Syria", "Yemen", "Somalia", "Ethiopia"],
            label_visibility="collapsed",
        )
    with c3:
        if st.button("Refresh", use_container_width=True):
            with st.spinner("Running LangGraph pipeline..."):
                result = call_api(
                    "/api/crisis/process", "POST",
                    {"region": "global" if region_filter == "All" else region_filter},
                    timeout=90,
                )
            if "error" in result:
                st.error(result["error"])
            else:
                st.session_state.crisis_feed = result.get("feed", [])
                st.session_state.carousel_index = 0
                st.success(f"{result.get('crisis_count', 0)} crisis reports processed.")
                st.rerun()

    # Load feed
    if not st.session_state.crisis_feed:
        with st.spinner("Loading crisis data..."):
            result = call_api("/api/crisis/feed")
        if "error" not in result:
            st.session_state.crisis_feed = result.get("feed", [])
        else:
            st.error(result["error"])
            return

    feed = st.session_state.crisis_feed
    if not feed:
        st.info("No data loaded. Click Refresh to fetch live crisis data.")
        return

    # ── Carousel ──────────────────────────────────────────────────────────────
    items_pp = 3
    total = len(feed)
    start = st.session_state.carousel_index
    end = min(start + items_pp, total)
    page_items = feed[start:end]

    st.markdown(
        f'<div style="color:#333333;font-size:0.72rem;letter-spacing:1px;text-transform:uppercase;'
        f'margin-bottom:18px;border-bottom:1px solid #1A1A1A;padding-bottom:10px;">'
        f'Showing {start+1}–{end} of {total} reports &nbsp;|&nbsp; LangGraph + OpenAI Analysis</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(len(page_items) or 1)
    for col, crisis in zip(cols, page_items):
        urgency = crisis.get("urgency", "Medium")
        border_color = "#DC2626" if urgency == "High" else ("#444444" if urgency == "Medium" else "#1E1E1E")
        badge = urgency_badge(urgency)
        chips = needs_chips(crisis.get("needs", []))
        src = crisis.get("source", "")
        region_loc = crisis.get("region", "Unknown")
        crisis_type = crisis.get("crisis_type", "")

        with col:
            st.markdown(
                f"""
                <div style="background:#0F0F0F;border:1px solid #1A1A1A;border-radius:4px;
                            padding:22px;min-height:380px;display:flex;flex-direction:column;
                            justify-content:space-between;border-top:3px solid {border_color};">
                    <div>
                        <div style="display:flex;justify-content:space-between;
                                    align-items:center;margin-bottom:12px;">
                            {badge}
                            <span style="color:#333333;font-size:0.68rem;letter-spacing:0.5px;">{src}</span>
                        </div>
                        <div style="color:#555;font-size:0.7rem;letter-spacing:0.5px;
                                    text-transform:uppercase;margin-bottom:8px;">
                            📍 {region_loc} &nbsp;·&nbsp; {crisis_type}
                        </div>
                        <div class="pf" style="color:#FFFFFF;font-size:1.05rem;font-weight:700;
                                    line-height:1.4;margin-bottom:10px;">
                            {crisis.get('title','')[:90]}{'…' if len(crisis.get('title',''))>90 else ''}
                        </div>
                        <div style="color:#666666;font-size:0.78rem;line-height:1.6;
                                    border-top:1px solid #1A1A1A;padding-top:10px;">
                            {crisis.get('summary','')[:210]}…
                        </div>
                    </div>
                    <div style="margin-top:16px;">
                        <div style="color:#333333;font-size:0.65rem;letter-spacing:1px;
                                    text-transform:uppercase;margin-bottom:6px;">Needs</div>
                        <div>{chips}</div>
                        <div style="color:#DC2626;font-size:0.72rem;font-weight:600;
                                    margin-top:10px;letter-spacing:0.3px;">
                            {crisis.get('people_affected','Unknown')} people affected
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Navigation ────────────────────────────────────────────────────────────
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    n1, n2, n3 = st.columns([1, 3, 1])
    with n1:
        if st.button("Prev", disabled=(start == 0), use_container_width=True):
            st.session_state.carousel_index = max(0, start - items_pp)
            st.rerun()
    with n2:
        pages_count = (total + items_pp - 1) // items_pp
        cur_p = start // items_pp
        dots = "".join(
            f'<span style="display:inline-block;width:{"10px" if i==cur_p else "6px"};'
            f'height:{"10px" if i==cur_p else "6px"};border-radius:50%;margin:0 4px;'
            f'background:{"#DC2626" if i==cur_p else "#2A2A2A"};transition:all 0.2s;"></span>'
            for i in range(pages_count)
        )
        st.markdown(f'<div style="text-align:center;padding:12px;">{dots}</div>', unsafe_allow_html=True)
    with n3:
        if st.button("Next", disabled=(end >= total), use_container_width=True):
            st.session_state.carousel_index = min(total - items_pp, start + items_pp)
            st.rerun()

    # ── Urgent People Who Need Help ───────────────────────────────────────────
    approved = st.session_state.get("approved_help_requests", [])
    if approved:
        st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
        st.markdown(
            '<div style="border-top:2px solid #DC2626;padding-top:24px;margin-bottom:20px;">'
            '<div style="display:flex;align-items:center;gap:12px;margin-bottom:6px;">'
            '<div class="pf" style="color:#FFFFFF;font-size:1.6rem;font-weight:700;letter-spacing:-0.5px;">'
            'Urgent — People Who Need Help</div>'
            '<div style="background:#DC2626;color:#FFFFFF;padding:2px 10px;border-radius:2px;'
            'font-size:0.65rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;">LIVE</div>'
            '</div>'
            '<div style="color:#444;font-size:0.72rem;letter-spacing:1px;text-transform:uppercase;'
            'margin-bottom:20px;">Verified community requests — approved for public visibility</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        cols_help = st.columns(min(len(approved), 3))
        for idx, req in enumerate(approved):
            trust_r = req.get("trust_score", {})
            chips_r = needs_chips(req.get("needs", []))

            # ── Contact / Phone ──────────────────────────────────────────────
            contact_email = req.get("contact_email") or ""
            contact_html = ""
            if contact_email:
                contact_html = (
                    f'<div style="display:flex;align-items:center;gap:6px;margin-top:8px;">'
                    f'<span style="color:#555;font-size:0.68rem;letter-spacing:0.5px;'
                    f'text-transform:uppercase;min-width:60px;">Contact</span>'
                    f'<span style="color:#AAAAAA;font-size:0.78rem;">{contact_email}</span>'
                    f'</div>'
                )

            # ── Bank / Account Number ────────────────────────────────────────
            bank_details = req.get("bank_details") or ""
            bank_html = ""
            if bank_details:
                bank_html = (
                    f'<div style="display:flex;align-items:flex-start;gap:6px;margin-top:6px;">'
                    f'<span style="color:#555;font-size:0.68rem;letter-spacing:0.5px;'
                    f'text-transform:uppercase;min-width:60px;padding-top:1px;">Account</span>'
                    f'<span style="color:#AAAAAA;font-size:0.78rem;font-family:monospace;'
                    f'background:#111;border:1px solid #2A2A2A;border-radius:2px;'
                    f'padding:2px 8px;">{bank_details}</span>'
                    f'</div>'
                )

            # ── Donation Link ────────────────────────────────────────────────
            donation_link = req.get("donation_link") or ""
            don_link_html = ""
            don_btn_html = ""
            if donation_link:
                don_link_html = (
                    f'<div style="display:flex;align-items:center;gap:6px;margin-top:6px;">'
                    f'<span style="color:#555;font-size:0.68rem;letter-spacing:0.5px;'
                    f'text-transform:uppercase;min-width:60px;">Donate</span>'
                    f'<a href="{donation_link}" target="_blank" '
                    f'style="color:#DC2626;font-size:0.76rem;word-break:break-all;'
                    f'text-decoration:underline;">{donation_link}</a>'
                    f'</div>'
                )
                don_btn_html = (
                    f'<a href="{donation_link}" target="_blank" '
                    f'style="display:inline-block;margin-top:14px;background:#DC2626;color:#FFFFFF;'
                    f'padding:6px 16px;border-radius:2px;text-decoration:none;font-size:0.72rem;'
                    f'font-weight:700;letter-spacing:0.5px;text-transform:uppercase;">Support Now →</a>'
                )

            with cols_help[idx % 3]:
                st.markdown(
                    f'<div style="background:#0F0F0F;border:1px solid #1A1A1A;border-top:3px solid #DC2626;'
                    f'border-radius:4px;padding:20px;margin-bottom:12px;">'
                    # ── Header row ──
                    f'<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;">'
                    f'<div>'
                    f'<div class="pf" style="color:#FFFFFF;font-size:1rem;font-weight:700;">{req["name"]}</div>'
                    f'<div style="color:#444;font-size:0.7rem;margin-top:3px;">'
                    f'📍 {req["region"]} &nbsp;·&nbsp; {req.get("created_at","")[:10]}</div>'
                    f'</div>'
                    f'<div style="background:#1A0000;border:1px solid #DC2626;color:#DC2626;padding:2px 8px;'
                    f'border-radius:2px;font-size:0.6rem;font-weight:700;letter-spacing:1.5px;'
                    f'text-transform:uppercase;">NEEDS HELP</div>'
                    f'</div>'
                    # ── Description ──
                    f'<div style="color:#777;font-size:0.8rem;line-height:1.6;margin-bottom:12px;">'
                    f'{req["description"][:240]}{"…" if len(req["description"]) > 240 else ""}'
                    f'</div>'
                    # ── Need chips ──
                    f'<div style="margin-bottom:12px;">{chips_r}</div>'
                    # ── Contact info block ──
                    f'<div style="border-top:1px solid #1E1E1E;padding-top:10px;margin-top:4px;">'
                    f'{contact_html}'
                    f'{bank_html}'
                    f'{don_link_html}'
                    f'</div>'
                    # ── Trust + CTA ──
                    f'<div style="display:flex;justify-content:space-between;align-items:center;margin-top:12px;">'
                    f'<div style="color:#333;font-size:0.68rem;letter-spacing:0.5px;">'
                    f'Trust: {trust_r.get("confidence","?")}</div>'
                    f'{don_btn_html}'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

    # ── Statistics ────────────────────────────────────────────────────────────
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    st.markdown(
        '<div class="pf" style="color:#FFFFFF;font-size:1.2rem;font-weight:700;'
        'margin-bottom:14px;letter-spacing:-0.3px;">Feed Statistics</div>',
        unsafe_allow_html=True,
    )
    high = sum(1 for c in feed if c.get("urgency") == "High")
    med  = sum(1 for c in feed if c.get("urgency") == "Medium")
    low  = sum(1 for c in feed if c.get("urgency") == "Low")

    s1, s2, s3, s4 = st.columns(4)
    for col, label, val, color in [
        (s1, "Total Crises",     total, "#FFFFFF"),
        (s2, "High Alert",       high,  "#DC2626"),
        (s3, "Medium Urgency",   med,   "#888888"),
        (s4, "Lower Urgency",    low,   "#444444"),
    ]:
        with col:
            st.markdown(
                f'<div style="background:#0F0F0F;border:1px solid #1A1A1A;border-radius:4px;'
                f'padding:18px;text-align:center;">'
                f'<div class="pf" style="color:{color};font-size:2rem;font-weight:700;">{val}</div>'
                f'<div style="color:#444444;font-size:0.65rem;letter-spacing:1.5px;'
                f'text-transform:uppercase;margin-top:4px;">{label}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 2 — Donor Hub
# ─────────────────────────────────────────────────────────────────────────────
_DONOR_PRESETS = ["Sudan", "Gaza", "Ukraine", "Haiti", "Syria", "Yemen",
                  "Somalia", "Ethiopia", "Pakistan", "Afghanistan", "Myanmar", "DRC"]


def render_donor_hub():
    section_header("Donor Hub", "AI-powered crisis analysis with verified donation links")

    # ── Free-text region input ─────────────────────────────────────────────
    st.markdown(
        '<div style="color:#555;font-size:0.7rem;letter-spacing:1px;'
        'text-transform:uppercase;margin-bottom:6px;">Search any region, country, or crisis</div>',
        unsafe_allow_html=True,
    )
    # Use a shadow key so preset buttons don't conflict with the text_input widget key
    preset_default = st.session_state.pop("_donor_region_preset", None)
    region_text = st.text_input(
        "Region",
        key="donor_region_text",
        value=preset_default if preset_default is not None else st.session_state.get("donor_region_text", ""),
        placeholder="e.g. Myanmar, Rohingya crisis, Sahel drought, DRC conflict...",
        label_visibility="collapsed",
    )

    # Quick-select preset buttons
    st.markdown(
        '<div style="color:#333;font-size:0.65rem;letter-spacing:1px;'
        'text-transform:uppercase;margin:10px 0 6px;">Or select a known region</div>',
        unsafe_allow_html=True,
    )
    preset_cols = st.columns(6)
    for i, r in enumerate(_DONOR_PRESETS[:12]):
        if preset_cols[i % 6].button(r, key=f"dp_{r}", use_container_width=True):
            st.session_state["_donor_region_preset"] = r
            st.rerun()

    final_region = st.session_state.get("donor_region_text", "").strip() or "Global"

    analyze = st.button("Analyze Region", type="primary")

    if analyze:
        if not final_region or final_region == "Global":
            st.warning("Enter a region or select one above before analyzing.")
        else:
            with st.spinner(f"AI analyzing '{final_region}'... (RAG + OpenAI)"):
                result = call_api("/api/rag/analyze", "POST", {"region": final_region}, timeout=90)
            st.session_state.donor_analysis = result

    result = st.session_state.get("donor_analysis")
    if result is None:
        st.markdown(
            '<div style="background:#0F0F0F;border:1px solid #1A1A1A;border-radius:4px;'
            'padding:48px;text-align:center;margin-top:20px;">'
            '<div class="pf" style="color:#FFFFFF;font-size:1.2rem;margin-bottom:8px;">Select a Region to Analyse</div>'
            '<div style="color:#444;font-size:0.8rem;max-width:460px;margin:0 auto;">'
            'Type any region or crisis name above (or use the quick-select buttons) '
            'then click <strong style="color:#FFFFFF;">Analyze Region</strong>.'
            '</div></div>',
            unsafe_allow_html=True,
        )
        return

    if "error" in result:
        st.error(result["error"])
        return

    analysis = result.get("analysis", "Analysis not available.")
    donation_info = result.get("donation_info", {})
    region_name = result.get("region", final_region)

    left, right = st.columns([3, 2])

    with left:
        st.markdown(
            f'<div style="background:#0F0F0F;border:1px solid #1A1A1A;border-left:3px solid #DC2626;'
            f'border-radius:4px;padding:6px 20px 20px;">'
            f'<div style="color:#444;font-size:0.65rem;letter-spacing:1.5px;'
            f'text-transform:uppercase;padding:16px 0 8px;">AI Analysis — {region_name}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(analysis)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown(
            '<div style="color:#555;font-size:0.65rem;letter-spacing:1.5px;'
            'text-transform:uppercase;margin-bottom:12px;">Verified Organizations</div>',
            unsafe_allow_html=True,
        )
        for org in donation_info.get("organizations", [])[:5]:
            st.markdown(
                f'<div style="background:#0F0F0F;border:1px solid #1A1A1A;border-radius:4px;'
                f'padding:14px;margin-bottom:8px;">'
                f'<div style="display:flex;justify-content:space-between;align-items:flex-start;">'
                f'<div>'
                f'<div style="color:#FFFFFF;font-size:0.88rem;font-weight:600;">{org.get("name","")}</div>'
                f'<div style="color:#444;font-size:0.72rem;margin-top:2px;">{org.get("type","")}</div>'
                f'</div>'
                f'<span style="background:#0A0A0A;border:1px solid #2A2A2A;color:#666;'
                f'padding:2px 8px;border-radius:2px;font-size:0.65rem;letter-spacing:0.5px;'
                f'white-space:nowrap;">{org.get("trust","Verified").replace("✅ ","").replace("⚠️ ","")}</span>'
                f'</div>'
                f'<a href="{org.get("url","#")}" target="_blank" style="display:inline-block;'
                f'margin-top:10px;background:#FFFFFF;color:#0A0A0A;padding:5px 14px;'
                f'border-radius:2px;text-decoration:none;font-size:0.72rem;font-weight:700;'
                f'letter-spacing:0.5px;text-transform:uppercase;">Donate</a>'
                f'</div>',
                unsafe_allow_html=True,
            )

        needs = donation_info.get("needs", [])
        if needs:
            st.markdown(
                '<div style="color:#555;font-size:0.65rem;letter-spacing:1.5px;'
                'text-transform:uppercase;margin:16px 0 10px;">Urgent Needs</div>',
                unsafe_allow_html=True,
            )
            for need in needs[:6]:
                st.markdown(
                    f'<div style="display:flex;align-items:flex-start;gap:8px;padding:7px 0;'
                    f'border-bottom:1px solid #1A1A1A;">'
                    f'<span style="color:#DC2626;margin-top:1px;font-size:0.8rem;">—</span>'
                    f'<span style="color:#AAAAAA;font-size:0.82rem;">{need}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 3 — Physical Aid Centers
# ─────────────────────────────────────────────────────────────────────────────
_CENTERS = {
    "United States": [
        {"name": "American Red Cross — Washington DC", "address": "430 17th Street NW, Washington, DC", "phone": "+1 (800) 733-2767", "hours": "Mon–Fri 9–5, Sat 10–3", "accepts": ["Food", "Clothing", "Hygiene Kits", "Cash"], "distance": "2.3 mi"},
        {"name": "UNICEF USA — New York", "address": "125 Maiden Lane, New York, NY 10038", "phone": "+1 (800) 367-5437", "hours": "Mon–Fri 9–6", "accepts": ["Medical Supplies", "Baby Food", "Cash"], "distance": "4.1 mi"},
        {"name": "World Vision — Federal Way, WA", "address": "34834 Weyerhaeuser Way S, Federal Way, WA", "phone": "+1 (888) 511-6548", "hours": "Mon–Fri 8–5", "accepts": ["Clothing", "Food", "School Supplies"], "distance": "7.8 mi"},
    ],
    "United Kingdom": [
        {"name": "British Red Cross — London", "address": "44 Moorfields, London EC2Y 9AL", "phone": "+44 344 871 1111", "hours": "Mon–Fri 9–5", "accepts": ["Clothing", "Medical Supplies", "Cash"], "distance": "1.2 mi"},
        {"name": "Oxfam Drop & Shop — Notting Hill", "address": "17 Notting Hill Gate, London W11", "phone": "+44 1865 472 602", "hours": "Mon–Sat 10–6", "accepts": ["Clothing", "Books", "Household Items"], "distance": "3.5 mi"},
    ],
    "Canada": [
        {"name": "Canadian Red Cross — Ottawa", "address": "170 Metcalfe Street, Ottawa ON", "phone": "+1 (613) 740-1900", "hours": "Mon–Fri 9–5", "accepts": ["Clothing", "Food", "Medical", "Cash"], "distance": "3.7 mi"},
    ],
    "Australia": [
        {"name": "Australian Red Cross — Sydney", "address": "159 Clarence Street, Sydney NSW 2000", "phone": "+61 1800 733 276", "hours": "Mon–Fri 9–5, Sat 9–1", "accepts": ["Clothing", "Food", "Hygiene", "Cash"], "distance": "2.1 mi"},
    ],
    "Germany": [
        {"name": "Deutsches Rotes Kreuz — Berlin", "address": "Carstennstrasse 58, 12205 Berlin", "phone": "+49 30 85404-0", "hours": "Mon–Fri 8–4", "accepts": ["Clothing", "Food", "Medical", "Cash"], "distance": "3.8 mi"},
    ],
    "France": [
        {"name": "Croix-Rouge Francaise — Paris", "address": "98 rue Didot, 75014 Paris", "phone": "+33 1 44 43 11 00", "hours": "Mon–Sat 9–6", "accepts": ["Clothing", "Food", "Hygiene", "Cash"], "distance": "2.9 mi"},
    ],
    "India": [
        {"name": "Indian Red Cross — New Delhi", "address": "1 Red Cross Road, New Delhi 110001", "phone": "+91 11 2371 6441", "hours": "Mon–Sat 9–5", "accepts": ["Medical", "Clothing", "Food", "Cash"], "distance": "5.0 mi"},
    ],
    "Other": [
        {"name": "International Red Cross / Red Crescent", "address": "Find your local chapter at redcross.org", "phone": "+1 (800) 733-2767", "hours": "Varies by location", "accepts": ["Clothing", "Food", "Medical", "Cash"], "distance": "Varies"},
    ],
}

_DONATE_WHAT = [
    ("Non-perishable Food", "Canned goods, dry foods, baby formula, energy bars"),
    ("Clothing & Warmth", "All sizes especially children's; blankets, coats"),
    ("Medical Supplies", "First aid kits, OTC medications — check with centre first"),
    ("Hygiene Kits", "Soap, toothbrush, feminine hygiene, hand sanitiser"),
    ("Educational Materials", "Books, notebooks, pens, school bags for children"),
    ("Monetary Donation", "Always the most flexible — organisations buy what is needed"),
]


def render_physical_aid():
    section_header("Physical Aid Centers", "Donation drop-off points near you")

    c1, c2 = st.columns(2)
    with c1:
        country = st.selectbox("Your Country", list(_CENTERS.keys()))
    with c2:
        crisis = st.selectbox("Supporting Region", ["Sudan", "Gaza", "Ukraine", "Haiti", "Syria", "Yemen", "Somalia", "Ethiopia"])

    centers = _CENTERS.get(country, _CENTERS["Other"])
    st.markdown(
        f'<div style="color:#333;font-size:0.7rem;letter-spacing:1px;text-transform:uppercase;'
        f'margin:12px 0 20px;border-bottom:1px solid #1A1A1A;padding-bottom:10px;">'
        f'{len(centers)} collection centres in {country} supporting {crisis} relief</div>',
        unsafe_allow_html=True,
    )

    for ctr in centers:
        chips = " ".join(
            f'<span style="background:#1A1A1A;border:1px solid #2A2A2A;color:#666;'
            f'padding:2px 8px;border-radius:2px;font-size:0.65rem;letter-spacing:0.5px;">{item}</span>'
            for item in ctr.get("accepts", [])
        )
        st.markdown(
                f'<div style="background:#0F0F0F;border:1px solid #1A1A1A;border-radius:4px;'
                f'padding:18px;margin-bottom:10px;">'
                f'<div style="color:#FFFFFF;font-weight:600;font-size:0.92rem;">{ctr["name"]}</div>'
                f'<div style="color:#444;font-size:0.76rem;margin-top:5px;">📍 {ctr["address"]}</div>'
                f'<div style="color:#444;font-size:0.76rem;">Tel: {ctr["phone"]}</div>'
                f'<div style="color:#444;font-size:0.76rem;">Hours: {ctr["hours"]}</div>'
                f'<div style="color:#444;font-size:0.76rem;">🕒 {ctr["distance"]} from you</div>'
                f'<div style="margin-top:10px;display:flex;gap:6px;flex-wrap:wrap;">{chips}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown(
        '<div class="pf" style="color:#FFFFFF;font-size:1.2rem;font-weight:700;margin-bottom:14px;">What Can I Donate?</div>',
        unsafe_allow_html=True,
    )
    cols3 = st.columns(3)
    for i, (title, desc) in enumerate(_DONATE_WHAT):
        with cols3[i % 3]:
            st.markdown(
                f'<div style="background:#0F0F0F;border:1px solid #1A1A1A;border-radius:4px;'
                f'padding:16px;margin-bottom:10px;">'
                f'<div style="color:#FFFFFF;font-size:0.85rem;font-weight:600;margin-bottom:5px;">{title}</div>'
                f'<div style="color:#444;font-size:0.75rem;line-height:1.5;">{desc}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 4 — Help Center
# ─────────────────────────────────────────────────────────────────────────────
def render_help_center():
    section_header("Help Center", "Request assistance or support others in crisis")

    tab_submit, tab_feed = st.tabs(["Submit a Request", "Public Help Feed"])

    with tab_submit:
        st.markdown(
            '<div style="background:#1A0000;border:1px solid #5A2A2A;border-radius:4px;'
            'padding:12px 16px;margin-bottom:20px;">'
            '<div style="color:#AAAAAA;font-size:0.78rem;line-height:1.5;">'
            'For emergencies call 911 / 999 / 112. This platform creates public visibility for '
            'requests. Submissions are AI-scored for trust level.'
            '</div></div>',
            unsafe_allow_html=True,
        )

        with st.form("help_form", clear_on_submit=False):
            r1c1, r1c2 = st.columns(2)
            with r1c1:
                name = st.text_input("Full Name *", placeholder="Your name / family name")
            with r1c2:
                region = st.selectbox(
                    "Region / Location *",
                    ["Sudan", "Gaza", "Ukraine", "Haiti", "Syria", "Yemen",
                     "Somalia", "Ethiopia", "Pakistan", "Afghanistan", "Other"],
                )
            description = st.text_area(
                "Describe Your Situation *",
                placeholder="What is happening? How many people are affected? Where are you? "
                            "Include as much detail as possible — more detail improves your trust score.",
                height=130,
            )
            needs_sel = st.multiselect(
                "What do you urgently need? *",
                ["Food", "Water", "Medical Aid", "Shelter", "Clothing",
                 "Financial Support", "Transportation", "Education", "Communication"],
                default=["Food", "Water"],
            )
            r2c1, r2c2 = st.columns(2)
            with r2c1:
                contact_email = st.text_input("Contact Email", placeholder="reach@you.com")
            with r2c2:
                has_docs = st.checkbox("I have supporting documents (strongly increases trust score)")
            r3c1, r3c2 = st.columns(2)
            with r3c1:
                donation_link = st.text_input("Donation Link (optional)", placeholder="https://paypal.me/yourlink")
            with r3c2:
                bank_details = st.text_input("Bank / Transfer Details (optional)", placeholder="For direct transfers")

            submitted = st.form_submit_button("Submit Help Request", use_container_width=True, type="primary")

        if submitted:
            if not name.strip() or not description.strip() or not needs_sel:
                st.error("Please fill in all required fields (*)")
            else:
                with st.spinner("Processing..."):
                    result = call_api("/api/help/submit", "POST", {
                        "name": name.strip(), "region": region,
                        "description": description.strip(), "needs": needs_sel,
                        "contact_email": contact_email.strip() or None,
                        "has_documents": has_docs,
                        "donation_link": donation_link.strip() or None,
                        "bank_details": bank_details.strip() or None,
                    })
                if "error" not in result and result.get("success"):
                    trust = result.get("trust_score", {})
                    st.success(f"Request submitted. Reference: #{result.get('id','')}")
                    st.markdown(
                        f'<div style="background:#0F0F0F;border:1px solid #1A1A1A;border-left:3px solid '
                        f'{"#DC2626" if trust.get("level")=="High" else "#555"};'
                        f'border-radius:4px;padding:16px;margin-top:10px;">'
                        f'<div style="color:#FFFFFF;font-size:0.9rem;font-weight:600;">'
                        f'{trust.get("badge","Submitted").replace("✅ ","").replace("⚠️ ","").replace("🔍 ","")}</div>'
                        f'<div style="color:#555;font-size:0.78rem;margin-top:4px;">'
                        f'AI Trust Score: {trust.get("confidence","?")} &nbsp;|&nbsp; '
                        f'Level: {trust.get("level","Unknown")}</div></div>',
                        unsafe_allow_html=True,
                    )
                    # Store pending request for admin approval
                    st.session_state.pending_approval = {
                        "name": name.strip(),
                        "region": region,
                        "description": description.strip(),
                        "needs": needs_sel,
                        "contact_email": contact_email.strip() or None,
                        "donation_link": donation_link.strip() or None,
                        "bank_details": bank_details.strip() or None,
                        "trust_score": trust,
                        "ref": result.get("id", ""),
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    }
                    st.session_state.help_requests = []
                else:
                    st.error(result.get("error", "Submission failed — please try again."))

        # ── Approval Panel ─────────────────────────────────────────────────────
        pending = st.session_state.get("pending_approval")
        if pending:
            st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
            st.markdown(
                '<div style="border-top:1px solid #2A2A2A;padding-top:20px;">'
                '<div style="color:#DC2626;font-size:0.68rem;font-weight:700;letter-spacing:2px;'
                'text-transform:uppercase;margin-bottom:12px;">⚠ Pending Approval — Publish to Crisis Feed?</div>'
                '</div>',
                unsafe_allow_html=True,
            )
            trust_p = pending.get("trust_score", {})
            chips_p = needs_chips(pending.get("needs", []))
            don_p = ""
            if pending.get("donation_link"):
                don_p = (
                    f'<a href="{pending["donation_link"]}" target="_blank" '
                    f'style="color:#DC2626;font-size:0.72rem;">🔗 Donation Link</a>'
                )
            st.markdown(
                f'<div style="background:#0F0F0F;border:1px solid #2A2A2A;border-left:3px solid #DC2626;'
                f'border-radius:4px;padding:18px;margin-bottom:14px;">'
                f'<div style="display:flex;justify-content:space-between;align-items:flex-start;">'
                f'<div>'
                f'<div style="color:#FFFFFF;font-weight:700;font-size:0.95rem;">{pending["name"]}</div>'
                f'<div style="color:#444;font-size:0.72rem;margin-top:3px;">📍 {pending["region"]} &nbsp;·&nbsp; {pending["created_at"]}</div>'
                f'</div>'
                f'<div style="background:#1A0000;border:1px solid #DC2626;color:#DC2626;padding:2px 10px;'
                f'border-radius:2px;font-size:0.65rem;font-weight:700;letter-spacing:1.5px;">AWAITING APPROVAL</div>'
                f'</div>'
                f'<div style="color:#777;font-size:0.8rem;margin:12px 0;line-height:1.6;">{pending["description"][:300]}</div>'
                f'<div style="margin-bottom:10px;">{chips_p}</div>'
                f'<div style="color:#444;font-size:0.72rem;">Trust Score: {trust_p.get("confidence","?")} &nbsp;|&nbsp; Level: {trust_p.get("level","Unknown")}</div>'
                f'{"<div style=margin-top:6px;>" + don_p + "</div>" if don_p else ""}'
                f'</div>',
                unsafe_allow_html=True,
            )
            col_approve, col_decline, _ = st.columns([1, 1, 3])
            with col_approve:
                if st.button("✅ Approve & Publish", type="primary", use_container_width=True, key="approve_btn"):
                    st.session_state.approved_help_requests.append(pending)
                    st.session_state.pending_approval = None
                    st.success("✅ Request approved and published to the Crisis Feed!")
                    st.rerun()
            with col_decline:
                if st.button("✕ Decline", use_container_width=True, key="decline_btn"):
                    st.session_state.pending_approval = None
                    st.info("Request declined and removed.")
                    st.rerun()

    with tab_feed:
        if st.button("Refresh Feed", use_container_width=False):
            st.session_state.help_requests = []

        if not st.session_state.help_requests:
            with st.spinner("Loading..."):
                result = call_api("/api/help/feed")
            if "error" not in result:
                st.session_state.help_requests = result.get("requests", [])
            else:
                st.error(result["error"])

        reqs = st.session_state.help_requests
        if not reqs:
            st.info("No help requests yet.")
            return

        st.markdown(
            f'<div style="color:#333;font-size:0.7rem;letter-spacing:1px;text-transform:uppercase;'
            f'margin-bottom:14px;border-bottom:1px solid #1A1A1A;padding-bottom:8px;">'
            f'{len(reqs)} active requests</div>',
            unsafe_allow_html=True,
        )

        for req in reqs:
            trust = req.get("trust_score", {})
            tc = "#DC2626" if trust.get("level") == "High" else ("#555" if trust.get("level") == "Medium" else "#333")
            chips = needs_chips(req.get("needs", []))
            don_btn = ""
            if req.get("donation_link"):
                don_btn = (
                    f'<a href="{req["donation_link"]}" target="_blank" '
                    f'style="background:#FFFFFF;color:#0A0A0A;padding:4px 12px;border-radius:2px;'
                    f'text-decoration:none;font-size:0.7rem;font-weight:700;letter-spacing:0.5px;'
                    f'text-transform:uppercase;">Donate</a>'
                )
            badge_text = trust.get("badge","").replace("✅ ","").replace("⚠️ ","").replace("🔍 ","")
            st.markdown(
                f'<div style="background:#0F0F0F;border:1px solid #1A1A1A;border-radius:4px;'
                f'padding:18px;margin-bottom:12px;border-left:3px solid {tc};">'
                f'<div style="display:flex;justify-content:space-between;'
                f'align-items:flex-start;margin-bottom:10px;">'
                f'<div>'
                f'<div class="pf" style="color:#FFFFFF;font-size:0.95rem;font-weight:700;">'
                f'{req.get("name","Anonymous")}</div>'
                f'<div style="color:#333;font-size:0.72rem;margin-top:2px;">'
                f'📍 {req.get("region","")} &nbsp;·&nbsp; {req.get("created_at","")[:10]}</div>'
                f'</div>'
                f'<div style="text-align:right;">'
                f'<div style="color:{tc};font-size:0.72rem;font-weight:600;">{badge_text}</div>'
                f'<div style="color:#333;font-size:0.68rem;">Score: {trust.get("confidence","?")}</div>'
                f'</div></div>'
                f'<div style="color:#777;font-size:0.8rem;line-height:1.6;margin-bottom:10px;">'
                f'{req.get("description","")[:320]}{"…" if len(req.get("description",""))>320 else ""}'
                f'</div>'
                f'<div style="margin-bottom:10px;">{chips}</div>'
                f'<div style="display:flex;gap:12px;align-items:center;">'
                f'<span style="color:#333;font-size:0.72rem;">{req.get("upvotes",0)} supporters</span>'
                f'{don_btn}'
                f'</div></div>',
                unsafe_allow_html=True,
            )


# ─────────────────────────────────────────────────────────────────────────────
# PAGE 5 — Crisis Blog
# ─────────────────────────────────────────────────────────────────────────────
_BLOG_PRESETS = ["Sudan", "Gaza", "Ukraine", "Haiti", "Syria", "Yemen",
                 "Somalia", "Ethiopia", "Pakistan", "Afghanistan", "Myanmar", "Libya"]


def render_blog():
    section_header("Crisis Blog", "AI-generated awareness articles — RAG-grounded, OpenAI-powered")

    st.markdown(
        '<div style="color:#555;font-size:0.7rem;letter-spacing:1px;'
        'text-transform:uppercase;margin-bottom:6px;">Search any region, country, or crisis topic</div>',
        unsafe_allow_html=True,
    )
    # Use a shadow key so preset buttons don't conflict with the text_input widget key
    blog_preset_default = st.session_state.pop("_blog_region_preset", None)
    blog_input = st.text_input(
        "Topic",
        key="blog_region_text",
        value=blog_preset_default if blog_preset_default is not None else st.session_state.get("blog_region_text", ""),
        placeholder="e.g. Rohingya crisis, Sahel famine, DRC displacement, North Korea sanctions...",
        label_visibility="collapsed",
    )

    st.markdown(
        '<div style="color:#333;font-size:0.65rem;letter-spacing:1px;'
        'text-transform:uppercase;margin:10px 0 6px;">Or select a known crisis region</div>',
        unsafe_allow_html=True,
    )
    bp_cols = st.columns(6)
    for i, r in enumerate(_BLOG_PRESETS[:12]):
        if bp_cols[i % 6].button(r, key=f"bp_{r}", use_container_width=True):
            st.session_state["_blog_region_preset"] = r
            st.rerun()

    final_topic = st.session_state.get("blog_region_text", "").strip()
    gen_btn = st.button("Generate Blog Post", type="primary")

    if gen_btn:
        if not final_topic:
            st.warning("Enter a region or crisis topic to write about.")
        else:
            with st.spinner(f"AI writing blog post on '{final_topic}'... (RAG-grounded, ~30s)"):
                result = call_api("/api/rag/blog", "POST", {"region": final_topic}, timeout=120)
            if "error" in result:
                st.error(result["error"])
            else:
                st.session_state.blog_content = result.get("blog", "")
                st.session_state.blog_region = final_topic

    if st.session_state.get("blog_content"):
        br = st.session_state.get("blog_region", "")
        now = datetime.now().strftime("%B %d, %Y")

        # Meta line
        st.markdown(
            f'<div style="display:flex;gap:12px;align-items:center;margin:20px 0 16px;flex-wrap:wrap;">'
            f'<span style="background:#1A0000;border:1px solid #DC2626;color:#DC2626;'
            f'padding:2px 10px;border-radius:2px;font-size:0.65rem;font-weight:700;letter-spacing:1.5px;">AI GENERATED</span>'
            f'<span style="background:#111;border:1px solid #2A2A2A;color:#888;'
            f'padding:2px 10px;border-radius:2px;font-size:0.65rem;letter-spacing:1px;">{br.upper()}</span>'
            f'<span style="background:#111;border:1px solid #2A2A2A;color:#888;'
            f'padding:2px 10px;border-radius:2px;font-size:0.65rem;letter-spacing:1px;">RAG-GROUNDED</span>'
            f'<span style="color:#333;font-size:0.7rem;">{now}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div style="background:#0D0D0D;border:1px solid #1A1A1A;border-top:3px solid #DC2626;'
            'border-radius:4px;padding:36px;">',
            unsafe_allow_html=True,
        )
        st.markdown(st.session_state.blog_content)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            '<div style="display:flex;gap:10px;margin-top:14px;">'
            '<span style="background:#1877F2;color:white;padding:6px 14px;border-radius:2px;'
            'font-size:0.72rem;font-weight:600;letter-spacing:0.5px;cursor:pointer;">Share on Facebook</span>'
            '<span style="background:#1DA1F2;color:white;padding:6px 14px;border-radius:2px;'
            'font-size:0.72rem;font-weight:600;letter-spacing:0.5px;cursor:pointer;">Share on Twitter</span>'
            '<span style="background:#0A66C2;color:white;padding:6px 14px;border-radius:2px;'
            'font-size:0.72rem;font-weight:600;letter-spacing:0.5px;cursor:pointer;">Share on LinkedIn</span>'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div style="background:#0F0F0F;border:1px solid #1A1A1A;border-radius:4px;'
            'padding:52px;text-align:center;margin-top:16px;">'
            '<div class="pf" style="color:#FFFFFF;font-size:1.2rem;margin-bottom:10px;">AI Blog Generator</div>'
            '<div style="color:#444;font-size:0.82rem;max-width:440px;margin:0 auto;line-height:1.7;">'
            'Type any region, conflict, or humanitarian crisis topic above, '
            'then click <strong style="color:#FFFFFF;">Generate Blog Post</strong> to create a '
            'RAG-grounded article with timeline, needs analysis, and action steps.'
            '</div></div>',
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    render_sidebar()
    render_header()

    page = st.session_state.page
    if page == "🌐 Crisis Feed":
        render_crisis_feed()
    elif page == "💰 Donor Hub":
        render_donor_hub()
    elif page == "🏥 Physical Aid":
        render_physical_aid()
    elif page == "🆘 Help Center":
        render_help_center()
    elif page == "📰 Crisis Blog":
        render_blog()
    else:
        render_crisis_feed()


if __name__ == "__main__":
    main()
