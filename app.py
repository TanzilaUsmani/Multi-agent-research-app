"""
Streamlit UI for the Research Pipeline.

IMPORTANT: This file only adds a visual interface. It does not modify the
logic in research_pipeline.py in any way — run_research_pipline() is
imported and called exactly as written.
"""

import sys
import io
import time
import contextlib
from datetime import datetime

import streamlit as st

from pipeline import run_research_pipline


# ----------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Insight Forge · AI Research Pipeline",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------
# Global styling
# ----------------------------------------------------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background: radial-gradient(circle at 15% 0%, #1b1035 0%, #0d0b1e 45%, #060613 100%);
            color: #EDEBFF;
        }

        /* Hide default streamlit chrome */
        #MainMenu, footer, header {visibility: hidden;}

        /* ---------- Hero header ---------- */
        .hero {
            padding: 2.6rem 2.8rem;
            border-radius: 22px;
            background: linear-gradient(120deg, rgba(124,58,237,0.35), rgba(56,189,248,0.18));
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: 0 20px 60px rgba(88, 28, 235, 0.25);
            margin-bottom: 1.8rem;
            position: relative;
            overflow: hidden;
        }
        .hero::after{
            content:"";
            position:absolute; inset:0;
            background: radial-gradient(circle at 90% 10%, rgba(255,255,255,0.08), transparent 40%);
        }
        .hero h1{
            font-family: 'Sora', sans-serif;
            font-weight: 800;
            font-size: 2.4rem;
            margin: 0;
            background: linear-gradient(90deg, #C4B5FD, #7DD3FC 60%, #F0ABFC);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
        }
        .hero p{
            margin-top: 0.6rem;
            color: #C9C6E8;
            font-size: 1.02rem;
            max-width: 620px;
        }

        /* ---------- Step pills ---------- */
        .step-track{
            display:flex; gap: 0.6rem; margin: 1.4rem 0 0.4rem 0; flex-wrap: wrap;
        }
        .step-pill{
            padding: 0.45rem 1rem;
            border-radius: 999px;
            font-size: 0.82rem;
            font-weight: 600;
            border: 1px solid rgba(255,255,255,0.12);
            background: rgba(255,255,255,0.04);
            color: #A8A4CC;
            transition: all .3s ease;
        }
        .step-pill.active{
            background: linear-gradient(90deg,#7C3AED,#38BDF8);
            color: white;
            border-color: transparent;
            box-shadow: 0 6px 18px rgba(124,58,237,0.45);
        }
        .step-pill.done{
            background: rgba(52, 211, 153, 0.12);
            border-color: rgba(52,211,153,0.4);
            color: #6EE7B7;
        }

        /* ---------- Glass cards ---------- */
        .glass-card{
            background: rgba(255,255,255,0.045);
            border: 1px solid rgba(255,255,255,0.09);
            border-radius: 18px;
            padding: 1.6rem 1.7rem;
            backdrop-filter: blur(10px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.25);
            margin-bottom: 1.1rem;
        }
        .glass-card h4{
            font-family:'Sora', sans-serif;
            margin-top:0;
            color: #E4E1FF;
            font-size: 1.05rem;
        }
        .glass-card .badge{
            display:inline-block;
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            padding: 0.2rem 0.6rem;
            border-radius: 999px;
            background: rgba(124,58,237,0.22);
            color: #C4B5FD;
            margin-bottom: 0.7rem;
        }

        /* ---------- Sidebar ---------- */
        section[data-testid="stSidebar"]{
            background: linear-gradient(180deg, #120c26, #0a0818);
            border-right: 1px solid rgba(255,255,255,0.06);
        }

        /* ---------- Buttons ---------- */
        .stButton>button{
            background: linear-gradient(90deg, #7C3AED, #38BDF8);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.7rem 1.4rem;
            font-weight: 700;
            font-size: 0.95rem;
            box-shadow: 0 10px 25px rgba(124,58,237,0.35);
            transition: transform .15s ease;
        }
        .stButton>button:hover{
            transform: translateY(-2px);
        }

        /* ---------- Text input ---------- */
        .stTextInput>div>div>input{
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.14);
            color: #EDEBFF;
            border-radius: 12px;
            padding: 0.7rem 0.9rem;
        }

        /* ---------- Tabs ---------- */
        button[data-baseweb="tab"]{
            color: #A8A4CC;
            font-weight: 600;
        }
        button[data-baseweb="tab"][aria-selected="true"]{
            color: #F0ABFC;
        }

        /* ---------- Log console ---------- */
        .log-box{
            background: #08060f;
            border: 1px solid rgba(56,189,248,0.25);
            border-radius: 14px;
            padding: 1rem 1.2rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.82rem;
            color: #7DD3FC;
            max-height: 340px;
            overflow-y: auto;
            white-space: pre-wrap;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🔮 Insight Forge")
    st.caption("Multi-agent research pipeline")
    st.markdown("---")
    st.markdown(
        """
        **Pipeline stages**
        1. 🔎 Search Agent
        2. 📖 Reader Agent
        3. ✍️ Writer Chain
        4. 🧪 Critic Chain
        """
    )
    st.markdown("---")
    show_logs = st.toggle("Show live console logs", value=True)
    st.markdown("---")
    if "history" in st.session_state and st.session_state.history:
        st.markdown("### 🕘 Past topics")
        for h in reversed(st.session_state.history[-8:]):
            st.caption(f"• {h}")

if "history" not in st.session_state:
    st.session_state.history = []
if "state" not in st.session_state:
    st.session_state.state = None

# ----------------------------------------------------------------------
# Hero header
# ----------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>Insight Forge 🔮</h1>
        <p>Give it a topic — a search agent, a reader agent, a writer chain and a
        critic chain work together to hunt down, digest, draft and grade a
        research report, right in front of you.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# Input row
# ----------------------------------------------------------------------
col1, col2 = st.columns([4, 1])
with col1:
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. The impact of quantum computing on cryptography",
        label_visibility="collapsed",
    )
with col2:
    run_clicked = st.button("🚀 Run Pipeline", use_container_width=True)

step_placeholder = st.empty()
log_placeholder = st.empty()
results_placeholder = st.container()


def render_steps(active_index: int):
    """active_index: 0..3 currently running, 4 = all done, -1 = idle"""
    labels = ["🔎 Search", "📖 Read", "✍️ Write", "🧪 Critique"]
    pills = []
    for i, label in enumerate(labels):
        if active_index == -1:
            cls = ""
        elif i < active_index:
            cls = "done"
        elif i == active_index:
            cls = "active"
        else:
            cls = ""
        pills.append(f'<div class="step-pill {cls}">{label}</div>')
    step_placeholder.markdown(
        f'<div class="step-track">{"".join(pills)}</div>', unsafe_allow_html=True
    )


class _StreamTee(io.StringIO):
    """Tees prints to real stdout AND a live-updating Streamlit log box,
    while also letting us detect which pipeline step we're on."""

    def __init__(self, placeholder, step_callback):
        super().__init__()
        self._placeholder = placeholder
        self._buffer = ""
        self._step_callback = step_callback

    def write(self, s):
        super().write(s)
        sys.__stdout__.write(s)
        self._buffer += s

        if "Step 2" in s:
            self._step_callback(1)
        elif "Step 3" in s:
            self._step_callback(2)
        elif "Step 4" in s:
            self._step_callback(3)
        elif "step 1" in s:
            self._step_callback(0)

        self._placeholder.markdown(
            f'<div class="log-box">{self._buffer[-4000:]}</div>',
            unsafe_allow_html=True,
        )
        return len(s)

    def flush(self):
        pass


if run_clicked:
    if not topic or not topic.strip():
        st.warning("Please enter a research topic first ✍️")
    else:
        render_steps(0)
        tee = _StreamTee(log_placeholder if show_logs else st.empty(), render_steps)

        start = time.time()
        error = None
        state = None
        try:
            with contextlib.redirect_stdout(tee):
                state = run_research_pipline(topic.strip())
        except Exception as e:
            error = e

        elapsed = time.time() - start

        if error:
            render_steps(-1)
            st.error(f"The pipeline hit an error after {elapsed:.1f}s:\n\n**{error}**")
        else:
            render_steps(4)
            st.session_state.state = state
            st.session_state.history.append(topic.strip())
            st.success(f"Pipeline finished in {elapsed:.1f}s ✅")

# ----------------------------------------------------------------------
# Results
# ----------------------------------------------------------------------
state = st.session_state.state
if state:
    with results_placeholder:
        st.markdown("### 📦 Results")

        tab_search, tab_read, tab_report, tab_critic = st.tabs(
            ["🔎 Search Result", "📖 Scraped Content", "✍️ Report", "🧪 Feedback"]
        )

        with tab_search:
            st.markdown(
                f"""
                <div class="glass-card">
                    <span class="badge">Search Agent</span>
                    <h4>Raw findings</h4>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(state.get("Search_result", "_No search result._"))

        with tab_read:
            st.markdown(
                f"""
                <div class="glass-card">
                    <span class="badge">Reader Agent</span>
                    <h4>Deep-scraped content</h4>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(str(state.get("scraped_content", "_No scraped content._")))

        with tab_report:
            st.markdown(
                f"""
                <div class="glass-card">
                    <span class="badge">Writer Chain</span>
                    <h4>Draft report</h4>
                </div>
                """,
                unsafe_allow_html=True,
            )
            report_text = str(state.get("report", "_No report generated._"))
            st.markdown(report_text)
            st.download_button(
                "⬇️ Download report (.md)",
                data=report_text,
                file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown",
            )

        with tab_critic:
            st.markdown(
                f"""
                <div class="glass-card">
                    <span class="badge">Critic Chain</span>
                    <h4>Feedback & score</h4>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(str(state.get("Feedback", "_No feedback generated._")))
else:
    st.info("Enter a topic above and hit **Run Pipeline** to get started.")
