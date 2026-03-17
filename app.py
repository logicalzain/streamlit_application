"""
DocuMind AI - Intelligent Document Analysis & AI Tools
Main Streamlit Application
"""

import streamlit as st
from file_processor import extract_text_from_file, get_supported_extensions, get_file_icon
from ai_tools import (
    ask_documents, summarize_text, translate_text,
    generate_code, analyze_sentiment, extract_key_info,
    compare_documents, general_chat, call_llm, test_api_key,
    list_gemini_models,
)

# ---------------------------------------------------------------------------
# Page config & custom CSS (Orange + Black theme)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="DocuMind AI",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
/* ---------- Global ---------- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --orange-primary: #FF6B00;
    --orange-light: #FF8C33;
    --orange-dark: #CC5500;
    --orange-glow: rgba(255, 107, 0, 0.3);
    --black-primary: #0A0A0A;
    --black-secondary: #141414;
    --black-card: #1A1A1A;
    --black-lighter: #242424;
    --text-primary: #F5F5F5;
    --text-secondary: #B0B0B0;
    --text-muted: #808080;
}

.stApp {
    background-color: var(--black-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background-color: var(--black-secondary) !important;
    border-right: 1px solid var(--orange-dark) !important;
}
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--orange-primary) !important;
}

/* ---------- Headers ---------- */
h1, h2, h3 { color: var(--orange-primary) !important; }

/* ---------- Buttons ---------- */
.stButton > button {
    background: linear-gradient(135deg, var(--orange-primary), var(--orange-dark)) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.5rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, var(--orange-light), var(--orange-primary)) !important;
    box-shadow: 0 0 20px var(--orange-glow) !important;
    transform: translateY(-1px) !important;
}

/* ---------- Inputs ---------- */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background-color: var(--black-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid #333 !important;
    border-radius: 8px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--orange-primary) !important;
    box-shadow: 0 0 10px var(--orange-glow) !important;
}

/* ---------- File uploader ---------- */
.stFileUploader {
    border: 2px dashed var(--orange-dark) !important;
    border-radius: 12px !important;
    background-color: var(--black-card) !important;
}

/* ---------- Tabs ---------- */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: var(--black-secondary) !important;
    border-radius: 10px !important;
    padding: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    color: var(--text-secondary) !important;
    background-color: transparent !important;
}
.stTabs [aria-selected="true"] {
    background-color: var(--orange-primary) !important;
    color: white !important;
}

/* ---------- Expander ---------- */
.streamlit-expanderHeader {
    background-color: var(--black-card) !important;
    color: var(--orange-primary) !important;
    border-radius: 8px !important;
}

/* ---------- Metric cards ---------- */
div[data-testid="stMetric"] {
    background-color: var(--black-card) !important;
    border: 1px solid #333 !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}
div[data-testid="stMetric"] label { color: var(--text-secondary) !important; }
div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: var(--orange-primary) !important; }

/* ---------- Chat messages ---------- */
.stChatMessage {
    background-color: var(--black-card) !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 12px !important;
}

/* ---------- Success / Info / Warning boxes ---------- */
.stSuccess { background-color: rgba(255,107,0,0.1) !important; border-left-color: var(--orange-primary) !important; }
.stInfo    { background-color: rgba(255,107,0,0.05) !important; border-left-color: var(--orange-light) !important; }

/* ---------- Scrollbar ---------- */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: var(--black-primary); }
::-webkit-scrollbar-thumb { background: var(--orange-dark); border-radius: 4px; }

/* ---------- Hero banner ---------- */
.hero-banner {
    background: linear-gradient(135deg, var(--black-secondary), var(--black-card));
    border: 1px solid var(--orange-dark);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    margin-bottom: 2rem;
}
.hero-banner h1 { font-size: 2.2rem !important; margin-bottom: 0.5rem; }
.hero-banner p  { color: var(--text-secondary); font-size: 1.1rem; }

/* ---------- Feature card ---------- */
.feature-card {
    background: var(--black-card);
    border: 1px solid #333;
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
    height: 100%;
}
.feature-card:hover {
    border-color: var(--orange-primary);
    box-shadow: 0 0 20px var(--orange-glow);
}
.feature-card h3 { color: var(--orange-primary) !important; margin: 0.5rem 0; }
.feature-card p  { color: var(--text-secondary); font-size: 0.9rem; }

/* ---------- Divider ---------- */
.orange-divider {
    height: 2px;
    background: linear-gradient(to right, transparent, var(--orange-primary), transparent);
    margin: 1.5rem 0;
    border: none;
}

/* ---------- Status badge ---------- */
.status-badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
}
.status-connected { background: rgba(255,107,0,0.2); color: var(--orange-primary); }
.status-disconnected { background: rgba(255,50,50,0.2); color: #ff5555; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Session state defaults
# ---------------------------------------------------------------------------
DEFAULTS = {
    "api_key": "",
    "provider": "Google Gemini",
    "documents": {},          # filename -> extracted text
    "chat_history": [],
    "doc_chat_history": [],
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ---------------------------------------------------------------------------
# Sidebar — API configuration
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:1rem 0;">
        <h1 style="color:#FF6B00 !important; font-size:1.8rem;">🔥 DocuMind AI</h1>
        <p style="color:#B0B0B0; font-size:0.85rem;">Intelligent Document Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="orange-divider"></div>', unsafe_allow_html=True)

    # --- Provider & key ---
    st.markdown("### ⚙️ API Configuration")
    provider = st.selectbox("AI Provider", ["Google Gemini", "OpenAI"], key="sel_provider")
    st.session_state["provider"] = provider

    help_text = (
        "Get your free API key from Google AI Studio"
        if provider == "Google Gemini"
        else "Get your API key from platform.openai.com"
    )
    api_key = st.text_input("🔑 API Key", type="password", help=help_text, key="inp_api_key")
    st.session_state["api_key"] = api_key

    # Model selection — dynamically fetch from API when key is available
    if provider == "Google Gemini":
        if api_key:
            if "gemini_models" not in st.session_state:
                with st.spinner("Fetching available models..."):
                    st.session_state["gemini_models"] = list_gemini_models(api_key)
            model_options = st.session_state["gemini_models"]
            if st.button("🔄 Refresh Models", key="btn_refresh_models"):
                st.session_state["gemini_models"] = list_gemini_models(api_key)
                st.rerun()
        else:
            model_options = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]
    else:
        model_options = ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
    selected_model = st.selectbox("🤖 Model", model_options, key="sel_model")

    # Connection status
    if api_key:
        st.markdown('<span class="status-badge status-connected">● Connected</span>', unsafe_allow_html=True)
        if st.button("🧪 Test API Key", key="btn_test_key"):
            with st.spinner("Testing API key..."):
                result = test_api_key(provider, api_key, selected_model)
                if result == "ok":
                    st.success("API key is working!")
                else:
                    st.error(f"API key test failed: {result}")
    else:
        st.markdown('<span class="status-badge status-disconnected">● No API Key</span>', unsafe_allow_html=True)

    st.markdown('<div class="orange-divider"></div>', unsafe_allow_html=True)

    # --- File upload ---
    st.markdown("### 📁 Upload Documents")
    exts = get_supported_extensions()
    uploaded_files = st.file_uploader(
        "Drag & drop files here",
        accept_multiple_files=True,
        type=exts,
        key="file_uploader",
    )

    if uploaded_files:
        new_docs = {}
        for f in uploaded_files:
            if f.name not in st.session_state["documents"]:
                with st.spinner(f"Processing {f.name}..."):
                    try:
                        text = extract_text_from_file(f)
                        new_docs[f.name] = text
                    except Exception as e:
                        st.error(f"Error processing {f.name}: {e}")
            else:
                new_docs[f.name] = st.session_state["documents"][f.name]
        st.session_state["documents"] = new_docs

    # Show loaded documents
    if st.session_state["documents"]:
        st.markdown("#### Loaded Documents")
        for fname in st.session_state["documents"]:
            icon = get_file_icon(fname)
            chars = len(st.session_state["documents"][fname])
            st.markdown(f"{icon} **{fname}** — {chars:,} chars")
    else:
        st.info("No documents uploaded yet.")

    st.markdown('<div class="orange-divider"></div>', unsafe_allow_html=True)

    # Quick actions
    if st.button("🗑️ Clear All Documents"):
        st.session_state["documents"] = {}
        st.rerun()
    if st.button("💬 Clear Chat History"):
        st.session_state["chat_history"] = []
        st.session_state["doc_chat_history"] = []
        st.rerun()

    st.markdown('<div class="orange-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align:center;color:#666;font-size:0.75rem;">Built with ❤️ using Streamlit & AI</p>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Helper: verify API key before any LLM call
# ---------------------------------------------------------------------------
def require_api_key() -> bool:
    if not st.session_state["api_key"]:
        st.warning("⚠️ Please enter your API key in the sidebar to use this feature.")
        return False
    return True


def get_all_documents_text() -> str:
    """Concatenate all loaded document texts."""
    parts = []
    for fname, text in st.session_state["documents"].items():
        parts.append(f"=== {fname} ===\n{text}")
    return "\n\n".join(parts)


# ---------------------------------------------------------------------------
# Main content area
# ---------------------------------------------------------------------------

# Hero banner
st.markdown("""
<div class="hero-banner">
    <h1>🔥 DocuMind AI</h1>
    <p>Upload documents, ask questions, summarize, translate, generate code & more — powered by AI</p>
</div>
""", unsafe_allow_html=True)

# Tabs for different tools
tab_qa, tab_summary, tab_translate, tab_code, tab_sentiment, tab_extract, tab_compare, tab_chat = st.tabs([
    "📄 Document Q&A",
    "📝 Summarizer",
    "🌐 Translator",
    "💻 Code Generator",
    "🎭 Sentiment",
    "🔍 Key Info Extractor",
    "⚖️ Compare Docs",
    "💬 AI Chat",
])

# ===== TAB 1: Document Q&A =====
with tab_qa:
    st.markdown("### 📄 Ask Questions About Your Documents")
    if not st.session_state["documents"]:
        st.info("👈 Upload one or more documents in the sidebar to get started.")
    else:
        st.success(f"**{len(st.session_state['documents'])}** document(s) loaded and ready.")

        # Document preview
        with st.expander("📖 Preview loaded documents"):
            for fname, text in st.session_state["documents"].items():
                st.markdown(f"**{get_file_icon(fname)} {fname}**")
                st.text_area(f"Content of {fname}", text[:3000] + ("..." if len(text) > 3000 else ""), height=150, key=f"prev_{fname}", disabled=True)

        # Chat-style Q&A
        for msg in st.session_state["doc_chat_history"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        question = st.chat_input("Ask a question about your documents...", key="doc_qa_input")
        if question:
            if not require_api_key():
                st.stop()
            st.session_state["doc_chat_history"].append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.markdown(question)

            with st.chat_message("assistant"):
                with st.spinner("Analyzing documents..."):
                    try:
                        docs_text = get_all_documents_text()
                        answer = ask_documents(
                            st.session_state["provider"],
                            st.session_state["api_key"],
                            docs_text, question, selected_model,
                        )
                        st.markdown(answer)
                        st.session_state["doc_chat_history"].append({"role": "assistant", "content": answer})
                    except Exception as e:
                        st.error(f"Error: {e}")

# ===== TAB 2: Summarizer =====
with tab_summary:
    st.markdown("### 📝 Text Summarizer")
    sum_source = st.radio("Source", ["Uploaded Documents", "Paste Text"], horizontal=True, key="sum_src")
    sum_style = st.selectbox("Summary Style", ["concise", "detailed", "eli5", "academic"], key="sum_style")

    if sum_source == "Paste Text":
        sum_text = st.text_area("Paste your text here", height=200, key="sum_paste")
    else:
        sum_text = get_all_documents_text()
        if sum_text:
            st.success(f"Using text from {len(st.session_state['documents'])} document(s).")
        else:
            st.info("Upload documents in the sidebar first.")

    if st.button("✨ Summarize", key="btn_summarize"):
        if not require_api_key():
            st.stop()
        if not sum_text.strip():
            st.warning("No text to summarize.")
        else:
            with st.spinner("Generating summary..."):
                try:
                    result = summarize_text(st.session_state["provider"], st.session_state["api_key"], sum_text, sum_style, selected_model)
                    st.markdown("---")
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Error: {e}")

# ===== TAB 3: Translator =====
with tab_translate:
    st.markdown("### 🌐 Text Translator")
    tr_source = st.radio("Source", ["Uploaded Documents", "Paste Text"], horizontal=True, key="tr_src")
    languages = ["Urdu", "Hindi", "Arabic", "Spanish", "French", "German", "Chinese", "Japanese", "Korean", "Portuguese", "Russian", "Italian", "Turkish", "Dutch"]
    target_lang = st.selectbox("Target Language", languages, key="tr_lang")

    if tr_source == "Paste Text":
        tr_text = st.text_area("Paste your text here", height=200, key="tr_paste")
    else:
        tr_text = get_all_documents_text()
        if tr_text:
            st.success(f"Using text from {len(st.session_state['documents'])} document(s).")
        else:
            st.info("Upload documents in the sidebar first.")

    if st.button("🌐 Translate", key="btn_translate"):
        if not require_api_key():
            st.stop()
        if not tr_text.strip():
            st.warning("No text to translate.")
        else:
            with st.spinner(f"Translating to {target_lang}..."):
                try:
                    result = translate_text(st.session_state["provider"], st.session_state["api_key"], tr_text, target_lang, selected_model)
                    st.markdown("---")
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Error: {e}")

# ===== TAB 4: Code Generator =====
with tab_code:
    st.markdown("### 💻 AI Code Generator")
    code_lang = st.selectbox("Programming Language", [
        "Python", "JavaScript", "TypeScript", "Java", "C++", "C#",
        "Go", "Rust", "PHP", "Ruby", "Swift", "Kotlin", "SQL", "HTML/CSS",
    ], key="code_lang")
    code_desc = st.text_area("Describe what you want the code to do", height=150, key="code_desc",
                             placeholder="e.g., Create a function that reads a CSV file and generates a bar chart...")

    if st.button("🚀 Generate Code", key="btn_code"):
        if not require_api_key():
            st.stop()
        if not code_desc.strip():
            st.warning("Please describe what you want.")
        else:
            with st.spinner("Generating code..."):
                try:
                    result = generate_code(st.session_state["provider"], st.session_state["api_key"], code_desc, code_lang, selected_model)
                    st.markdown("---")
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Error: {e}")

# ===== TAB 5: Sentiment Analysis =====
with tab_sentiment:
    st.markdown("### 🎭 Sentiment Analysis")
    sent_source = st.radio("Source", ["Uploaded Documents", "Paste Text"], horizontal=True, key="sent_src")

    if sent_source == "Paste Text":
        sent_text = st.text_area("Paste your text here", height=200, key="sent_paste",
                                 placeholder="Enter a review, tweet, article, or any text...")
    else:
        sent_text = get_all_documents_text()
        if sent_text:
            st.success(f"Using text from {len(st.session_state['documents'])} document(s).")
        else:
            st.info("Upload documents in the sidebar first.")

    if st.button("🔍 Analyze Sentiment", key="btn_sentiment"):
        if not require_api_key():
            st.stop()
        if not sent_text.strip():
            st.warning("No text to analyze.")
        else:
            with st.spinner("Analyzing sentiment..."):
                try:
                    result = analyze_sentiment(st.session_state["provider"], st.session_state["api_key"], sent_text, selected_model)
                    st.markdown("---")
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Error: {e}")

# ===== TAB 6: Key Info Extractor =====
with tab_extract:
    st.markdown("### 🔍 Key Information Extractor")
    ext_source = st.radio("Source", ["Uploaded Documents", "Paste Text"], horizontal=True, key="ext_src")

    if ext_source == "Paste Text":
        ext_text = st.text_area("Paste your text here", height=200, key="ext_paste")
    else:
        ext_text = get_all_documents_text()
        if ext_text:
            st.success(f"Using text from {len(st.session_state['documents'])} document(s).")
        else:
            st.info("Upload documents in the sidebar first.")

    if st.button("🔍 Extract Key Info", key="btn_extract"):
        if not require_api_key():
            st.stop()
        if not ext_text.strip():
            st.warning("No text to analyze.")
        else:
            with st.spinner("Extracting key information..."):
                try:
                    result = extract_key_info(st.session_state["provider"], st.session_state["api_key"], ext_text, selected_model)
                    st.markdown("---")
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Error: {e}")

# ===== TAB 7: Compare Documents =====
with tab_compare:
    st.markdown("### ⚖️ Document Comparison")
    doc_names = list(st.session_state["documents"].keys())

    if len(doc_names) < 2:
        st.info("Upload at least **2 documents** to use the comparison feature.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            doc1_name = st.selectbox("Document 1", doc_names, key="cmp_doc1")
        with col2:
            remaining = [d for d in doc_names if d != doc1_name]
            doc2_name = st.selectbox("Document 2", remaining, key="cmp_doc2")

        if st.button("⚖️ Compare", key="btn_compare"):
            if not require_api_key():
                st.stop()
            with st.spinner("Comparing documents..."):
                try:
                    result = compare_documents(
                        st.session_state["provider"],
                        st.session_state["api_key"],
                        st.session_state["documents"][doc1_name],
                        st.session_state["documents"][doc2_name],
                        selected_model,
                    )
                    st.markdown("---")
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Error: {e}")

# ===== TAB 8: General AI Chat =====
with tab_chat:
    st.markdown("### 💬 General AI Chat")
    st.caption("Chat with AI about anything — no documents required.")

    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_msg = st.chat_input("Type your message...", key="chat_input")
    if user_msg:
        if not require_api_key():
            st.stop()
        st.session_state["chat_history"].append({"role": "user", "content": user_msg})
        with st.chat_message("user"):
            st.markdown(user_msg)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    answer = general_chat(
                        st.session_state["provider"],
                        st.session_state["api_key"],
                        user_msg,
                        st.session_state["chat_history"],
                        selected_model,
                    )
                    st.markdown(answer)
                    st.session_state["chat_history"].append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Error: {e}")

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown('<div class="orange-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; padding:1rem; color:#666;">
    <p>🔥 <strong style="color:#FF6B00;">DocuMind AI</strong> — Your Intelligent Document Assistant</p>
    <p style="font-size:0.8rem;">Supports PDF, DOCX, XLSX, CSV, TXT, PPTX, JSON, HTML, Markdown & more</p>
</div>
""", unsafe_allow_html=True)
