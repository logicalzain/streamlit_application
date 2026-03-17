"""
AI Tools Module
Provides AI-powered features using Google Gemini or OpenAI APIs.
Features: Document Q&A, Summarization, Translation, Code Generation, Sentiment Analysis
"""

import time
from google import genai
from openai import OpenAI


# ---------------------------------------------------------------------------
# Provider wrappers
# ---------------------------------------------------------------------------

def _call_gemini(api_key: str, prompt: str, model_name: str = "gemini-2.0-flash") -> str:
    """Send a prompt to Google Gemini using the new google-genai SDK."""
    client = genai.Client(api_key=api_key)

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            return response.text
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower() or "rate" in error_msg.lower():
                if attempt < 2:
                    time.sleep(5 * (attempt + 1))
                    continue
                raise RuntimeError(
                    f"Rate limit reached for model '{model_name}'. "
                    f"Try: 1) Wait 30-60 seconds and try again, "
                    f"2) Switch to a different model, "
                    f"3) Check your quota at https://aistudio.google.com/apikey"
                ) from e
            raise


def _call_openai(api_key: str, prompt: str, model_name: str = "gpt-4o-mini") -> str:
    """Send a prompt to OpenAI and return the response text."""
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def call_llm(provider: str, api_key: str, prompt: str, model_name: str | None = None) -> str:
    """Unified LLM caller that routes to the right provider."""
    if provider == "Google Gemini":
        return _call_gemini(api_key, prompt, model_name or "gemini-2.0-flash")
    elif provider == "OpenAI":
        return _call_openai(api_key, prompt, model_name or "gpt-4o-mini")
    else:
        raise ValueError(f"Unknown provider: {provider}")


def test_api_key(provider: str, api_key: str, model_name: str) -> str:
    """Test if the API key works. Returns 'ok' or an error message."""
    try:
        result = call_llm(provider, api_key, "Say 'hello' in one word.", model_name)
        if result and len(result.strip()) > 0:
            return "ok"
        return "Empty response from API"
    except Exception as e:
        return str(e)


def list_gemini_models(api_key: str) -> list[str]:
    """Fetch all available Gemini model names from the API."""
    try:
        client = genai.Client(api_key=api_key)
        models = []
        for model in client.models.list():
            name = model.name
            # API returns "models/gemini-2.0-flash" -> we want "gemini-2.0-flash"
            if name.startswith("models/"):
                name = name[len("models/"):]
            # Only include generateContent-capable models
            if hasattr(model, "supported_actions"):
                if "generateContent" not in (model.supported_actions or []):
                    continue
            models.append(name)
        # Sort: newest/best first (2.5 > 2.0 > 1.5), flash before pro
        models.sort(reverse=True)
        return models if models else _default_gemini_models()
    except Exception:
        return _default_gemini_models()


def _default_gemini_models() -> list[str]:
    """Fallback model list if API listing fails."""
    return [
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
    ]


# ---------------------------------------------------------------------------
# High-level AI features
# ---------------------------------------------------------------------------

def ask_documents(provider: str, api_key: str, documents_text: str, question: str, model: str | None = None) -> str:
    """Answer a question based on the provided document text."""
    prompt = f"""You are a helpful AI assistant. Answer the user's question based ONLY on the
provided document content. If the answer is not in the documents, say so clearly.

=== DOCUMENT CONTENT ===
{documents_text[:50000]}
=== END DOCUMENT CONTENT ===

User Question: {question}

Provide a clear, detailed, and well-structured answer:"""
    return call_llm(provider, api_key, prompt, model)


def summarize_text(provider: str, api_key: str, text: str, style: str = "concise", model: str | None = None) -> str:
    """Summarize the given text in the requested style."""
    style_instructions = {
        "concise": "Provide a brief summary in 3-5 bullet points.",
        "detailed": "Provide a comprehensive summary covering all key points, organized with headings.",
        "eli5": "Explain the content as if explaining to a 5-year-old. Use simple language.",
        "academic": "Provide an academic-style abstract with key findings and conclusions.",
    }
    instruction = style_instructions.get(style, style_instructions["concise"])
    prompt = f"""Summarize the following text.
{instruction}

Text:
{text[:50000]}

Summary:"""
    return call_llm(provider, api_key, prompt, model)


def translate_text(provider: str, api_key: str, text: str, target_language: str, model: str | None = None) -> str:
    """Translate text to the target language."""
    prompt = f"""Translate the following text to {target_language}.
Preserve the original formatting and meaning as closely as possible.

Text:
{text[:30000]}

Translation:"""
    return call_llm(provider, api_key, prompt, model)


def generate_code(provider: str, api_key: str, description: str, language: str = "Python", model: str | None = None) -> str:
    """Generate code based on a description."""
    prompt = f"""Generate {language} code for the following requirement.
Include comments explaining the code. Provide clean, production-ready code.

Requirement: {description}

Code:"""
    return call_llm(provider, api_key, prompt, model)


def analyze_sentiment(provider: str, api_key: str, text: str, model: str | None = None) -> str:
    """Analyze the sentiment of the given text."""
    prompt = f"""Analyze the sentiment of the following text. Provide:
1. Overall sentiment (Positive / Negative / Neutral / Mixed)
2. Confidence level (High / Medium / Low)
3. Key emotional tones detected
4. Brief explanation

Text:
{text[:20000]}

Sentiment Analysis:"""
    return call_llm(provider, api_key, prompt, model)


def extract_key_info(provider: str, api_key: str, text: str, model: str | None = None) -> str:
    """Extract key information, entities, and facts from text."""
    prompt = f"""Extract all key information from the following text. Organize into:
1. **Key Facts & Figures** - important numbers, dates, statistics
2. **People & Organizations** - names mentioned and their roles
3. **Main Topics** - primary subjects discussed
4. **Action Items / Decisions** - if any
5. **Important Quotes** - notable statements

Text:
{text[:40000]}

Extracted Information:"""
    return call_llm(provider, api_key, prompt, model)


def compare_documents(provider: str, api_key: str, doc1_text: str, doc2_text: str, model: str | None = None) -> str:
    """Compare two documents and highlight similarities and differences."""
    prompt = f"""Compare the following two documents. Provide:
1. **Similarities** - common themes, shared information
2. **Differences** - contrasting points, unique information in each
3. **Summary** - brief overview of how they relate

=== DOCUMENT 1 ===
{doc1_text[:25000]}

=== DOCUMENT 2 ===
{doc2_text[:25000]}

Comparison:"""
    return call_llm(provider, api_key, prompt, model)


def general_chat(provider: str, api_key: str, message: str, chat_history: list | None = None, model: str | None = None) -> str:
    """General AI chat without document context."""
    history_text = ""
    if chat_history:
        for msg in chat_history[-10:]:
            role = msg["role"].capitalize()
            history_text += f"{role}: {msg['content']}\n"

    history_block = ""
    if history_text:
        history_block = "Previous conversation:\n" + history_text

    prompt = f"""You are a helpful AI assistant. Respond to the user's message thoughtfully.

{history_block}

User: {message}

Answer:"""
    return call_llm(provider, api_key, prompt, model)
