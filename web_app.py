"""Streamlit interface for the multi-agent study assistant."""
import streamlit as st
from agents.pdf_agent import PDFAgent
from agents.retrieval_agent import RetrievalAgent
from agents.notes_agent import NotesAgent
from agents.flashcard_agent import FlashcardAgent
from agents.exam_analysis_agent import ExamAnalysisAgent
from agents.quality_auditor import QualityAuditor
from modules.csv_writer import to_csv
from config import GROQ_API_KEY

st.set_page_config(page_title="Study Assistant", page_icon="📚", layout="wide")
st.title("📚 Multi-Agent Student Study Assistant")
st.caption("Turn textbook PDFs into source-grounded revision notes and flashcards.")
if "chunks" not in st.session_state:
    st.session_state.chunks = []

with st.sidebar:
    st.header("1. Add learning material")
    uploaded = st.file_uploader("Textbook PDF", type=["pdf"])
    if uploaded and st.button("Process textbook", type="primary"):
        try:
            import tempfile
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp:
                temp.write(uploaded.getvalue())
                temp_path = temp.name
            chunks, pages = PDFAgent().process(temp_path)
            st.session_state.chunks = chunks
            st.session_state.book_name = uploaded.name
            st.success(f"Indexed {pages} pages into {len(chunks)} passages.")
        except Exception as exc:
            st.error(str(exc))
    st.caption("Scanned/image-only PDFs need OCR. No uploaded file is saved by this demo.")
    st.caption("LLM mode: " + ("Groq enabled" if GROQ_API_KEY else "local mode (add GROQ_API_KEY for AI generation)"))

if st.session_state.chunks:
    st.success(f"Ready: {st.session_state.get('book_name', 'Textbook')} · {len(st.session_state.chunks)} passages")
    task = st.radio("Choose a study task", ["Ask a question", "Make revision notes", "Create flashcards"], horizontal=True)
    topic = st.text_input("Question or topic", placeholder="For example: explain photosynthesis")
    if st.button("Generate", disabled=not topic):
        passages = RetrievalAgent(st.session_state.chunks).retrieve(topic)
        st.session_state.last_passages = passages
        if not passages:
            st.warning("No matching passages found. Try different wording.")
        elif task == "Create flashcards":
            cards = FlashcardAgent().run(topic, passages)
            st.session_state.cards = cards
            for i, card in enumerate(cards, 1):
                with st.expander(f"Card {i}: {card['question']}"):
                    st.write(card["answer"])
                    st.caption(card["source"])
            st.download_button("Download flashcards CSV", to_csv(cards), "flashcards.csv", "text/csv")
        else:
            content = NotesAgent().run(topic, passages)
            st.markdown(content)
            audit = QualityAuditor().review(content, passages)
            st.info(f"Quality check — {audit['status']}: {audit['notes']}")
            st.download_button("Download notes", content, "study-notes.md", "text/markdown")
        with st.expander("Retrieved textbook passages"):
            for p in passages:
                st.markdown(f"**{p['source']} · page {p['page']}**\n\n{p['text']}")
else:
    st.info("Upload a selectable-text PDF in the sidebar to begin.")

st.divider()
st.subheader("Past-paper trend analysis")
paper = st.text_area("Paste past-paper text", height=130, placeholder="Paste extracted questions from past papers...")
if st.button("Analyze past paper", disabled=not paper.strip()):
    st.markdown(ExamAnalysisAgent().run(paper, st.session_state.chunks))
