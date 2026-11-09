# Multi-Agent Student Study Assistant

A Python and Streamlit study tool that turns selectable-text textbook PDFs into retrieved, source-linked passages, revision notes, and flashcards. It also provides basic repeated-term analysis for pasted past-paper text.

## Features

- Extracts text and page numbers from PDFs with PyMuPDF.
- Splits text into overlapping chunks and ranks relevant chunks locally.
- Uses separate PDF, retrieval, notes, flashcard, exam analysis, and quality auditor agent classes.
- Works in local fallback mode without an LLM key; Groq can optionally generate the study materials.
- Shows retrieved textbook passages and page numbers alongside generated material.
- Downloads notes as Markdown and flashcards as CSV.
- Keeps uploaded PDFs in memory/temp storage for processing; it does not persist an uploaded book in the repository.

## Run locally

Requires Python 3.10 or newer.

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Optional: add your Groq key to .env
streamlit run web_app.py
```

Alternatively run `python app.py`. To use Groq, set `GROQ_API_KEY` in `.env` or your environment. Never commit `.env`. Without a key, local retrieval and fallback outputs still work.

## How it works

1. `PDFAgent` extracts page text and `chunk_pages` splits it while keeping source/page metadata.
2. `RetrievalAgent` ranks chunks using a lightweight local term-frequency/inverse-document-frequency-style score.
3. `NotesAgent` or `FlashcardAgent` builds output from retrieved excerpts. With Groq configured, it asks the model to format the output using those excerpts; otherwise it uses a simple local fallback.
4. `QualityAuditor` reports the pages used or asks the configured model for a grounding review. This is a review aid, not proof that output is correct.
5. `ExamAnalysisAgent` identifies repeated terms in text pasted by the user. It does not infer chapter weightage from official exam datasets.

## Files and folders

| Path | Purpose |
| --- | --- |
| `web_app.py` | Streamlit interface and session state for PDF upload, tasks, citations, and downloads. |
| `app.py` | Convenience command-line entry point that starts Streamlit. |
| `config.py` | Paths, chunk/retrieval settings, and optional Groq configuration. |
| `agents/pdf_agent.py` | Coordinates PDF extraction and chunking. |
| `agents/retrieval_agent.py` | Agent wrapper around passage search. |
| `agents/notes_agent.py` | Produces revision notes from retrieved excerpts. |
| `agents/flashcard_agent.py` | Produces question/answer cards from retrieved excerpts. |
| `agents/exam_analysis_agent.py` | Counts recurring terms in pasted past-paper text. |
| `agents/quality_auditor.py` | Provides a transparent source-page check or optional LLM review. |
| `modules/pdf_loader.py` | Extracts text with page metadata using PyMuPDF. |
| `modules/chunker.py` | Splits pages into overlapping chunks. |
| `modules/retriever.py` | Local lexical ranking for query-to-chunk retrieval. |
| `modules/llm_client.py` | Optional Groq chat completion wrapper. |
| `modules/csv_writer.py` | Serializes flashcards to CSV. |
| `modules/markdown_writer.py` | Saves Markdown notes to disk when used by scripts. |
| `requirements.txt` | Python package dependencies. |
| `.env.example` | Template for optional Groq configuration. Copy to `.env`. |
| `.gitignore` | Keeps secrets, environments, caches, and local data out of Git. |
| `data/books/` | Reserved for user-managed source books; uploads are not saved here by the app. |
| `outputs/` | Reserved for exported artifacts if using the file-writer helpers. |

## Current limits and next improvements

- Search is lexical, not a neural embedding/FAISS index. This keeps the starter project light and easy to run; adding vector embeddings and a persistent FAISS index would be a useful next iteration.
- Scanned PDFs need OCR before upload; the app currently detects files with no selectable text and explains this.
- Past-paper trend analysis only works on text pasted into the app. Add curated papers and normalize question concepts before making exam-weightage claims.
- The local flashcard fallback is intentionally simple. Use the optional LLM mode for better question variety, then verify answers against the cited textbook pages.
- The quality auditor is not an independent fact-checking guarantee. Human review remains important.

## CV wording

**Multi-Agent Student Study Assistant | Python, Streamlit, PyMuPDF, Groq**

- Built a modular study assistant that extracts page-aware content from textbook PDFs, chunks it with overlap, and retrieves relevant passages for study tasks.
- Designed specialized agents for PDF ingestion, retrieval, note and flashcard generation, past-paper term analysis, and output review.
- Added optional Groq generation, source-page visibility, and Markdown/CSV downloads, with local fallback behavior when no API key is configured.

Only claim the technologies and features you have personally run and can explain. In particular, this implementation currently uses lexical retrieval rather than FAISS/vector embeddings.
