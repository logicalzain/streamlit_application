# 🔥 DocuMind AI — Intelligent Document Analysis & AI Tools

> **A powerful, multi-feature AI web application built with Streamlit.**
> Upload any document, ask questions, summarize, translate, generate code, analyze sentiment & more — all powered by your own API key.

---

## 📸 Overview

**DocuMind AI** is a sleek, orange-and-black themed AI-powered web application that lets you:

- Upload **any type of document** (PDF, Word, Excel, PowerPoint, TXT, CSV, JSON, HTML, Markdown)
- **Ask questions** about your documents and get accurate, context-aware answers
- **Summarize** documents in multiple styles (concise, detailed, ELI5, academic)
- **Translate** text into 14+ languages
- **Generate code** in 14+ programming languages
- **Analyze sentiment** of any text
- **Extract key information** (facts, people, topics, action items) from documents
- **Compare two documents** side-by-side
- **Chat freely** with AI about any topic

All features work with **Google Gemini** (free!) or **OpenAI** — you choose.

---

## 🗂️ Project Structure

```
API_application/
├── app.py               # Main Streamlit application (UI + routing)
├── ai_tools.py          # AI feature functions (Q&A, summarize, translate, etc.)
├── file_processor.py    # File parsing for all supported formats
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables
└── README.md            # This documentation file
```

### File Descriptions

| File                | Purpose |
|---------------------|---------|
| `app.py`            | The main entry point. Contains the Streamlit UI, custom CSS theme (orange + black), sidebar configuration, all 8 feature tabs, and session state management. |
| `ai_tools.py`       | All AI-powered functions. Each feature (summarize, translate, etc.) has its own function that builds a prompt and calls the selected LLM provider. |
| `file_processor.py` | Handles reading and extracting text from 11+ file formats. Each format has a dedicated parser function. |
| `requirements.txt`  | Lists all Python packages needed to run the app. |
| `.env.example`      | Template for environment variables (optional — the app uses sidebar input). |

---

## 🚀 Installation & Setup

### Prerequisites

- **Python 3.10+** installed on your system
- **pip** (Python package manager)
- An API key from **Google AI Studio** (free) or **OpenAI**

### Step 1: Clone or Navigate to the Project

```bash
cd API_application
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Get Your API Key

#### Option A: Google Gemini (Recommended — FREE)

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key — you'll paste it in the app sidebar

#### Option B: OpenAI

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click **"Create new secret key"**
4. Copy the key — you'll paste it in the app sidebar
5. Note: OpenAI requires a paid account with credits

### Step 5: Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 🎨 Theme & Design

The application uses a custom **Orange (#FF6B00) + Black (#0A0A0A)** color scheme:

| Element          | Color / Style                                    |
|------------------|--------------------------------------------------|
| Background       | Deep black `#0A0A0A`                             |
| Cards/Panels     | Dark grey `#1A1A1A` with subtle borders          |
| Primary accent   | Vibrant orange `#FF6B00`                         |
| Buttons          | Orange gradient with glow hover effect           |
| Text (primary)   | Light grey `#F5F5F5`                             |
| Text (secondary) | Muted grey `#B0B0B0`                             |
| Active tabs      | Orange background with white text                |
| Input focus      | Orange border glow                               |
| Scrollbar        | Orange thumb on black track                      |

### Customizing Colors

To change the color scheme, edit the CSS variables at the top of `app.py` in the `CUSTOM_CSS` string:

```css
:root {
    --orange-primary: #FF6B00;    /* Change this to your primary color */
    --orange-light: #FF8C33;      /* Lighter variant */
    --orange-dark: #CC5500;       /* Darker variant */
    --black-primary: #0A0A0A;     /* Main background */
    --black-card: #1A1A1A;        /* Card backgrounds */
    --text-primary: #F5F5F5;      /* Main text color */
}
```

For example, to switch to **blue + dark**:
```css
--orange-primary: #2196F3;
--orange-light: #64B5F6;
--orange-dark: #1565C0;
```

---

## 📄 Supported File Formats

| Format     | Extensions         | Library Used     | What's Extracted                       |
|------------|--------------------|------------------|----------------------------------------|
| PDF        | `.pdf`             | PyPDF2           | All text from every page               |
| Word       | `.docx`            | python-docx      | Paragraphs + table content             |
| Excel      | `.xlsx`, `.xls`    | openpyxl         | All sheets with cell data              |
| CSV        | `.csv`             | Built-in csv     | All rows and columns                   |
| PowerPoint | `.pptx`            | python-pptx      | Text from all slides and shapes        |
| Plain Text | `.txt`             | Built-in         | Raw text content                       |
| Markdown   | `.md`              | Built-in         | Raw markdown content                   |
| JSON       | `.json`            | Built-in json    | Pretty-printed JSON                    |
| HTML       | `.html`, `.htm`    | BeautifulSoup    | Text only (scripts/styles stripped)    |

### Adding New File Format Support

To add support for a new format, edit `file_processor.py`:

1. Add a new `_extract_xxx()` function:
```python
def _extract_xxx(raw_bytes: bytes) -> str:
    # Your parsing logic here
    return extracted_text
```

2. Add the extension check in `extract_text_from_file()`:
```python
elif filename.endswith(".xxx"):
    return _extract_xxx(raw_bytes)
```

3. Add the extension to `get_supported_extensions()`:
```python
return ["pdf", "txt", ..., "xxx"]
```

---

## 🛠️ Features in Detail

### 1. 📄 Document Q&A

**What it does:** Upload one or more documents, then ask questions. The AI reads your documents and answers based on their content.

**How to use:**
1. Upload files in the sidebar
2. Go to the **"Document Q&A"** tab
3. Type your question in the chat input
4. The AI will answer based on your documents
5. Continue asking — it keeps chat history

**How it works internally:**
- All document texts are concatenated
- The full text (up to 50,000 characters) is sent as context to the LLM
- The LLM is instructed to answer ONLY from the document content
- Chat history is maintained in `st.session_state["doc_chat_history"]`

---

### 2. 📝 Text Summarizer

**What it does:** Summarize uploaded documents or pasted text in 4 different styles.

**Summary Styles:**

| Style      | Description                                        |
|------------|----------------------------------------------------|
| Concise    | Brief summary in 3-5 bullet points                |
| Detailed   | Comprehensive summary with headings                |
| ELI5       | Explained like you're 5 — simple language          |
| Academic   | Formal abstract with key findings and conclusions  |

**How to use:**
1. Choose source: uploaded documents or paste text
2. Select a summary style
3. Click **"Summarize"**

---

### 3. 🌐 Text Translator

**What it does:** Translate document content or pasted text into 14+ languages.

**Supported Languages:** Urdu, Hindi, Arabic, Spanish, French, German, Chinese, Japanese, Korean, Portuguese, Russian, Italian, Turkish, Dutch

**How to use:**
1. Choose source: uploaded documents or paste text
2. Select the target language
3. Click **"Translate"**

**Adding More Languages:**
Edit the `languages` list in `app.py` (inside the `tab_translate` section):
```python
languages = ["Urdu", "Hindi", ..., "Your New Language"]
```

---

### 4. 💻 Code Generator

**What it does:** Describe what you want in plain English, and the AI generates working code.

**Supported Languages:** Python, JavaScript, TypeScript, Java, C++, C#, Go, Rust, PHP, Ruby, Swift, Kotlin, SQL, HTML/CSS

**How to use:**
1. Select the programming language
2. Describe what you want the code to do
3. Click **"Generate Code"**

**Example prompts:**
- "Create a REST API with Flask that has CRUD operations for a todo app"
- "Write a function to merge two sorted arrays efficiently"
- "Build a responsive navigation bar with dropdown menus"

---

### 5. 🎭 Sentiment Analysis

**What it does:** Analyzes the emotional tone of text and provides:
- Overall sentiment (Positive / Negative / Neutral / Mixed)
- Confidence level
- Key emotional tones detected
- Brief explanation

**How to use:**
1. Choose source or paste text (reviews, tweets, articles, etc.)
2. Click **"Analyze Sentiment"**

---

### 6. 🔍 Key Information Extractor

**What it does:** Automatically extracts structured information from text:
- Key facts and figures (numbers, dates, statistics)
- People and organizations mentioned
- Main topics discussed
- Action items and decisions
- Important quotes

**How to use:**
1. Choose source (documents or paste text)
2. Click **"Extract Key Info"**

---

### 7. ⚖️ Document Comparison

**What it does:** Compares two uploaded documents and identifies:
- **Similarities** — common themes and shared information
- **Differences** — contrasting points and unique information
- **Summary** — how the documents relate to each other

**How to use:**
1. Upload at least 2 documents
2. Select Document 1 and Document 2 from dropdowns
3. Click **"Compare"**

---

### 8. 💬 General AI Chat

**What it does:** A free-form AI chatbot — no documents needed. Ask anything.

**How to use:**
1. Go to the **"AI Chat"** tab
2. Type any message
3. Get intelligent responses
4. Full conversation history is maintained

---

## ⚙️ Configuration & Customization

### Changing the AI Provider

The app supports two providers:

| Provider       | Cost    | Models Available                              | Best For               |
|----------------|---------|-----------------------------------------------|------------------------|
| Google Gemini  | Free    | gemini-2.0-flash, gemini-2.0-flash-lite, gemini-1.5-flash, gemini-1.5-pro | Most users (free tier) |
| OpenAI         | Paid    | gpt-4o-mini, gpt-4o, gpt-3.5-turbo         | Premium quality        |

Select the provider and model in the sidebar.

### Adjusting Text Limits

In `ai_tools.py`, each function truncates input text to prevent hitting token limits:

```python
# In ask_documents():
{documents_text[:50000]}    # 50K character limit for document Q&A

# In summarize_text():
{text[:50000]}              # 50K for summarization

# In translate_text():
{text[:30000]}              # 30K for translation

# In analyze_sentiment():
{text[:20000]}              # 20K for sentiment analysis
```

To increase these limits (if your model supports it), change the slice values.

### Adding a New AI Feature

1. **Add the function in `ai_tools.py`:**
```python
def my_new_feature(provider, api_key, text, model=None):
    prompt = f"""Your prompt here...
    Text: {text}
    """
    return call_llm(provider, api_key, prompt, model)
```

2. **Add a new tab in `app.py`:**
```python
# Add to the tabs list:
tab_qa, tab_summary, ..., tab_new = st.tabs([..., "🆕 New Feature"])

# Add the tab content:
with tab_new:
    st.markdown("### 🆕 My New Feature")
    # ... your UI code ...
```

3. **Import the function at the top of `app.py`.**

### Adding a New AI Provider

1. **Add the API call function in `ai_tools.py`:**
```python
def _call_my_provider(api_key, prompt, model_name="default-model"):
    # Your API call logic
    return response_text
```

2. **Update the `call_llm` router:**
```python
elif provider == "My Provider":
    return _call_my_provider(api_key, prompt, model_name or "default-model")
```

3. **Add it to the sidebar dropdown in `app.py`:**
```python
provider = st.selectbox("AI Provider", ["Google Gemini", "OpenAI", "My Provider"])
```

---

## 🔒 Security Notes

- **API keys are never stored on disk** — they only exist in the browser session
- **Keys are entered via password input** — they're masked in the UI
- **No data is sent anywhere** except to the AI provider you selected
- **All processing happens locally** — your files are parsed on your machine
- **Session state is cleared** when you close the browser tab

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'xxx'"
```bash
pip install -r requirements.txt
```

### "Error processing file..."
- Make sure the file is not corrupted
- Check if the file format is supported (see table above)
- For password-protected files, remove the password first

### "API Error: 429 Too Many Requests"
- You've hit the rate limit — wait a minute and try again
- Google Gemini free tier: 15 requests/minute, 1,500 requests/day
- Consider upgrading to a paid plan for higher limits

### "API Error: Invalid API Key"
- Double-check your API key in the sidebar
- Make sure you selected the correct provider
- Regenerate the key if needed

### App is slow
- Large files take longer to process — try smaller files first
- Use `gemini-2.0-flash` or `gpt-4o-mini` for faster responses
- Close other browser tabs to free memory

---

## 📦 Dependencies

| Package              | Version    | Purpose                              |
|----------------------|------------|--------------------------------------|
| streamlit            | >= 1.30.0  | Web application framework            |
| google-generativeai  | >= 0.8.0   | Google Gemini API client             |
| openai               | >= 1.12.0  | OpenAI API client                    |
| PyPDF2               | >= 3.0.0   | PDF text extraction                  |
| python-docx          | >= 1.1.0   | Word document parsing                |
| openpyxl             | >= 3.1.0   | Excel file parsing                   |
| python-pptx          | >= 0.6.23  | PowerPoint parsing                   |
| beautifulsoup4       | >= 4.12.0  | HTML text extraction                 |

---

## 📝 Quick Start (TL;DR)

```bash
# 1. Go to the folder
cd API_application

# 2. Install everything
pip install -r requirements.txt

# 3. Run it
streamlit run app.py

# 4. In the browser:
#    - Paste your Google Gemini API key in the sidebar
#    - Upload files
#    - Ask questions!
```

---

## 🤝 Credits

- Built with [Streamlit](https://streamlit.io/)
- AI powered by [Google Gemini](https://ai.google.dev/) and [OpenAI](https://openai.com/)
- Part of the **AI ka Chilla** assignments series

---

**Made with 🔥 by DocuMind AI**
