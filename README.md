IntervueAI

IntervueAI is a lightweight interview-practice and candidate-evaluation toolkit. It combines a web UI, RAG-backed question/answering, resume analysis, and basic proctoring to help candidates prepare for interviews and let reviewers inspect results.

Key features
- Interview practice with live prompts and recording support
- Retrieval-augmented generation (RAG) for contextual answers
- Resume analyzer and resume history viewer
- Basic proctoring and live view for monitored sessions
- Persisted vectorstore (Chroma) for document embeddings

Quick start
1. Create and activate a Python environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the app (Streamlit or app entry):

```powershell
streamlit run app.py
# or: python app.py
```

Project layout (important files)
- `app.py` — application entry
- `build_vectorstore.py` — build or rebuild the vectorstore
- `scripts/strip_comments.py` — utility used to strip comments and create backups
- `src/` — application source (models, pages, utils)
- `vectorstore/chroma_db/` — Chroma DB files and SQLite store

Contributions
Feel free to open issues or add PRs. If you run heavy data operations, keep backups of `vectorstore/` and `uploads/`.

