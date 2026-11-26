# Tool-Using Research Agent

A small **agentic AI** project built with **Python + LangGraph**.

The agent answers questions by choosing and calling tools:

| Tool | Purpose |
|------|---------|
| `calculator` | Safe arithmetic (`+ - * /`) |
| `get_current_time` | Current UTC timestamp |
| `search_notes` | Search a local company knowledge file |

It also includes a **tiny evaluation harness** that checks tool selection and answer content.

---

## Why this project

Practice for AI engineering roles focused on:

- Tool-calling agents (beyond a plain chatbot)
- Multi-step agent workflows with LangGraph
- Basic **LLM evaluation** (expected tool + expected answer text)
- Clean Python structure, env-based config, and Git hygiene

---

## Setup

```bash
git clone https://github.com/vinayadabala05/agentic-research-assistant.git
cd agentic-research-assistant

python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
```

Add an API key to `.env`:

**Option A — Groq (free tier)**  
1. Create a key at https://console.groq.com  
2. Set:
```env
GROQ_API_KEY=your_key
LLM_PROVIDER=groq
```

**Option B — OpenAI**
```env
OPENAI_API_KEY=your_key
LLM_PROVIDER=openai
```

---

## Run the agent

```bash
python main.py "What is 12 * 8?"
python main.py "How many days for a refund?"
python main.py "What is the current UTC time?"
```

Or interactive:

```bash
python main.py
```

Example output:

```text
Question: What is 12 * 8?

Tools used: calculator
Answer: 96
```

---

## Run evaluations

```bash
python evals/run_evals.py
```

This runs 8 cases from `evals/cases.json` and reports pass/fail for:

- Whether the expected tool was used
- Whether the final answer contains the expected text

---

## Project layout

```text
agentic-research-assistant/
├── agent/
│   ├── graph.py      # LangGraph agent + tool routing
│   ├── tools.py      # calculator, time, search_notes
│   └── prompts.py    # system prompt
├── data/
│   └── notes.txt     # demo company knowledge
├── evals/
│   ├── cases.json    # evaluation dataset
│   └── run_evals.py  # automated pass/fail runner
├── main.py
├── requirements.txt
└── README.md
```

---

## What I learned

- Wiring tools into a LangGraph agent loop
- Logging which tools were called for a request
- Writing a small ground-truth eval set and checking agent behaviour
- Keeping secrets out of git with `.env` + `.gitignore`

---

## Author

**Vinay Adabala**  
GitHub: [vinayadabala05](https://github.com/vinayadabala05)  
LinkedIn: [vinay-adabala05](https://www.linkedin.com/in/vinay-adabala05/)
