# EduGenie — Google Gemini Powered Learning Assistant

SmartBridge internship project. Flat modular architecture: five independent
Python modules, one central FastAPI app, Jinja2 + static frontend.

## Structure (matches Epic 1 architecture)

```
EduGenie/
├── main.py                  # Central FastAPI app — routing and backend integration
├── qna.py                   # Q&A module — Gemini 1.5 Pro
├── explanation_module.py    # Explanation module — LaMini-Flan-T5-783M (local, CPU)
├── quiz_module.py           # Quiz generation — Gemini 1.5 Pro
├── summary_module.py        # Summarization — Gemini 1.5 Pro
├── learning_path.py         # Personalized learning recommendations — Gemini 1.5 Pro
├── templates/
│   └── index.html           # dropdown + textarea + submit + result
├── static/
│   └── style.css
├── requirements.txt
└── .env.example
```

## Why these models (Epic 1)

- **Gemini 1.5 Pro** (Q&A, Summary, Quiz, Learning Path) — chosen for its
  reasoning, contextual understanding, and structured response generation
  via cloud API.
- **LaMini-Flan-T5-783M** (Explanation only) — a lightweight,
  instruction-tuned, CPU-compatible local model. Runs offline, keeps
  simple concept explanations fast and cloud-independent.

## Module functions (Epic 2)

- `qna.py` → `answer_question_with_gemini(question)` — wraps Gemini 1.5 Pro,
  catches exceptions and returns an inline error string on failure.
- `explanation_module.py` → `explain_topic(topic)` — loads
  `AutoTokenizer`/`AutoModelForSeq2SeqLM` for LaMini-Flan-T5-783M once at
  import time, generates with `temperature=0.7, top_k=50, top_p=0.95,
  do_sample=True`.
- `quiz_module.py` → `generate_quiz(text)` — prompts Gemini for 3 MCQs as
  JSON, strips Markdown code fences via `clean_json_block()`, then
  `json.loads()`s the result. Returns `[{"error": "..."}]` on failure
  instead of raising.
- `summary_module.py` → `summarize_text(text)` — single Gemini call,
  same try/except error-string pattern.
- `learning_path.py` → `get_learning_recommendations(topic)` — builds a
  beginner/intermediate/advanced prompt, checks `response.text` then
  `response.parts[0].text` as a fallback, prints the raw response and
  full traceback for debugging.

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then fill in GEMINI_API_KEY
uvicorn main:app --reload
```

Visit `http://localhost:8000`. Endpoints (Epic 2, Backend API story):

- `GET  /qa?question=...` — Q&A, returns `{"answer": ...}`
- `POST /explain/` — body `{"topic": "..."}` → `{"topic", "explanation"}`
- `POST /summarize/` — body `{"text": "..."}` → `{"summary": ...}`
- `POST /quiz` — body `{"text": "..."}` → `{"quiz": [...]}` (logs the
  generated quiz server-side for debugging)
- `GET  /learn/recommendations?topic=...` — → `{"topic", "recommendation"}`

Each POST endpoint validates its required field and returns a 400 with
`{"error": "..."}` if missing, rather than raising.

## Notes

- `explanation_module.py` downloads `MBZUAI/LaMini-Flan-T5-783M` on first
  run and caches it in memory for the life of the process — first request
  will be slow (larger download than the 248M variant), subsequent ones
  are fast.
- No database — every request is stateless, matching the flow diagram
  (no persistence layer shown).
- Quiz generation expects Gemini to return clean JSON; if it wraps the
  JSON in prose, `json.loads` will raise — worth a try/except with a
  retry during testing (Epic 4, Story 2).
