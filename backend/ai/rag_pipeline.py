"""
LangChain RAG Pipeline for NeuroQuest
"""
from typing import List, Dict, Any, Optional
from langchain.chains import RetrievalQA
from langchain.llms import Anthropic
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os
from dotenv import load_dotenv
from nim_retriever import NIMClient

load_dotenv()


class RAGPipeline:
    """Retrieval-Augmented Generation pipeline for research paper synthesis."""

    def __init__(self):
        """Initialize the RAG pipeline."""
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.vector_store: Optional[FAISS] = None
        self.qa_chain: Optional[RetrievalQA] = None

        # Initialize LLM based on provider
        ai_provider = os.getenv("AI_PROVIDER", "nim").lower()

        if ai_provider == "nim":
            # Use NVIDIA NIM
            self.nim_client = NIMClient()
            self.llm = None  # NIM doesn't use LangChain LLM interface
            print("🚀 Using NVIDIA NIM for AI inference")
        elif ai_provider == "anthropic":
            # Use Anthropic Claude
            self.llm = Anthropic(
                anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
                model="claude-sonnet-4-20240514",
                temperature=0.7,
            )
            self.nim_client = None
            print("🤖 Using Anthropic Claude for AI inference")
        else:
            # Default to NIM
            self.nim_client = NIMClient()
            self.llm = None
            print("🚀 Using NVIDIA NIM for AI inference (default)")

    def create_vector_store(self, documents: List[Document]) -> FAISS:
        """
        Create a vector store from documents.

        Args:
            documents: List of documents to index

        Returns:
            FAISS vector store
        """
        # Split documents into chunks
        texts = self.text_splitter.split_documents(documents)

        # Create vector store
        vector_store = FAISS.from_documents(texts, self.embeddings)
        self.vector_store = vector_store

        return vector_store

    def load_vector_store(self, path: str) -> FAISS:
        """
        Load a vector store from disk.

        Args:
            path: Path to the vector store directory

        Returns:
            Loaded FAISS vector store
        """
        self.vector_store = FAISS.load_local(path, self.embeddings)
        return self.vector_store

    def save_vector_store(self, path: str):
        """
        Save the vector store to disk.

        Args:
            path: Path to save the vector store
        """
        if self.vector_store:
            self.vector_store.save_local(path)

    def create_qa_chain(self) -> RetrievalQA:
        """
        Create a QA chain for question answering.

        Returns:
            RetrievalQA chain
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Call create_vector_store first.")

        retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
        )

        return self.qa_chain

    def query(self, question: str, k: int = 5) -> Dict[str, Any]:
        """
        Query the RAG pipeline.

        Args:
            question: Question to ask
            k: Number of documents to retrieve

        Returns:
            Dictionary containing answer and source documents
        """
        if not self.qa_chain:
            self.create_qa_chain()

        result = self.qa_chain({"query": question})

        return {
            "answer": result["result"],
            "source_documents": result["source_documents"],
        }

    def add_documents(self, documents: List[Document]):
        """
        Add documents to the vector store.

        Args:
            documents: List of documents to add
        """
        if not self.vector_store:
            self.create_vector_store(documents)
        else:
            texts = self.text_splitter.split_documents(documents)
            self.vector_store.add_texts([doc.page_content for doc in texts])

    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """
        Perform similarity search on the vector store.

        Args:
            query: Search query
            k: Number of results to return

        Returns:
            List of similar documents
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized.")

        return self.vector_store.similarity_search(query, k=k)

    def synthesize_results(
        self,
        query: str,
        search_results: List[Dict[str, Any]],
        max_length: int = 500
    ) -> str:
        """
        Synthesize search results into a coherent summary.

        Args:
            query: Original search query
            search_results: List of search results
            max_length: Maximum length of the summary

        Returns:
            Synthesized summary
        """
        # Use NIM if available
        if self.nim_client:
            return self.nim_client.synthesize_results(query, search_results, max_length=max_length)

        # Fallback to LangChain RAG pipeline
        # Create documents from search results
        documents = []
        for result in search_results:
            doc = Document(
                page_content=f"{result['title']}\n\n{result['abstract']}",
                metadata={
                    "source": result["source"],
                    "url": result["url"],
                    "authors": result["authors"],
                }
            )
            documents.append(doc)

        # Create or update vector store
        if not self.vector_store:
            self.create_vector_store(documents)
        else:
            self.add_documents(documents)

        # Query for synthesis
        result = self.query(
            f"Synthesize a comprehensive summary of these research papers about: {query}. "
            f"Focus on key findings, methodologies, and implications. Keep it under {max_length} words."
        )

        return result["answer"]


# Example usage
if __name__ == "__main__":
    # Create sample documents
    sample_docs = [
        Document(
            page_content="This paper introduces a novel approach to machine learning using transformers.",
            metadata={"source": "arxiv", "title": "Novel Transformer Approach"}
        ),
        Document(
            page_content="We present a new method for natural language processing using attention mechanisms.",
            metadata={"source": "pubmed", "title": "Attention in NLP"}
        ),
    ]

    # Initialize pipeline
    pipeline = RAGPipeline()
    pipeline.create_vector_store(sample_docs)

    # Query
    result = pipeline.query("What are the key innovations in these papers?")
    print("Answer:", result["answer"])
    print("\nSources:")
    for doc in result["source_documents"]:
        print(f"- {doc.metadata.get('title', 'Unknown')}")
