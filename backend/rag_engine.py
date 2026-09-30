import os
import re
import logging
from typing import List, Tuple
from rank_bm25 import BM25Okapi
from config import DATA_DIR

logger = logging.getLogger(__name__)

class ClinicalRAGEngine:
    def __init__(self):
        self.chunks: List[str] = []
        self.chunk_sources: List[str] = []
        self.bm25: BM25Okapi = None
        self._load_documents()

    def _load_documents(self):
        doc_files = {
            "clinical_protocols.txt": "Clinical Protocol",
            "medication_guidelines.txt": "Medication Guidelines",
            "nursing_procedures.txt": "Nursing Procedures",
        }

        all_chunks = []
        all_sources = []

        for filename, source_label in doc_files.items():
            filepath = os.path.join(DATA_DIR, filename)
            if not os.path.exists(filepath):
                logger.warning(f"Document not found: {filepath}")
                continue
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            chunks = self._split_into_chunks(content, source_label)
            all_chunks.extend(chunks)
            all_sources.extend([source_label] * len(chunks))
            logger.info(f"Loaded {len(chunks)} chunks from {filename}")

        self.chunks = all_chunks
        self.chunk_sources = all_sources

        tokenized = [self._tokenize(c) for c in self.chunks]
        self.bm25 = BM25Okapi(tokenized)
        logger.info(f"RAG engine initialized with {len(self.chunks)} total chunks")

    def _split_into_chunks(self, text: str, source: str) -> List[str]:
        sections = re.split(r"={3,}", text)
        chunks = []
        for section in sections:
            section = section.strip()
            if not section:
                continue
            if len(section) <= 1200:
                chunks.append(section)
            else:
                paragraphs = section.split("\n\n")
                current = ""
                for para in paragraphs:
                    if len(current) + len(para) < 1200:
                        current += "\n\n" + para if current else para
                    else:
                        if current:
                            chunks.append(current.strip())
                        current = para
                if current:
                    chunks.append(current.strip())
        return [c for c in chunks if len(c) > 50]

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        return text.split()

    def search(self, query: str, top_k: int = 3) -> str:
        if not self.chunks or self.bm25 is None:
            return "Clinical knowledge base not available."

        tokenized_query = self._tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

        results: List[Tuple[float, str, str]] = [
            (scores[i], self.chunk_sources[i], self.chunks[i])
            for i in top_indices
            if scores[i] > 0
        ]

        if not results:
            return "No relevant clinical protocol or guideline found for this query."

        output_parts = []
        for score, source, chunk in results:
            output_parts.append(f"[Source: {source}]\n{chunk}")

        return "\n\n---\n\n".join(output_parts)


_rag_engine: ClinicalRAGEngine = None

def get_rag_engine() -> ClinicalRAGEngine:
    global _rag_engine
    if _rag_engine is None:
        _rag_engine = ClinicalRAGEngine()
    return _rag_engine
