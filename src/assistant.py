import time
from datetime import datetime
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.globals import get_run_id
from langsmith import traceable

from .config import langsmith_client
from .prompts import RAG_TEMPLATE


class DocumentAssistant:
    def __init__(self, collection_name="demo_docs"):
        """Doküman asistanını başlat"""
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None
        self.chain = None
        self.retriever = None
        self.template = RAG_TEMPLATE
        self.collection_name = collection_name

    @traceable(
        run_type="tool",
        name="Load Documents",
        tags=["setup", "document-loading"]
    )
    def load_documents(self, texts: list[str]):
        """Dokümanları yükle ve vektör store'a ekle"""
        print(f"{len(texts)} doküman yükleniyor...")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

        all_documents = []
        for i, text in enumerate(texts):
            chunks = text_splitter.split_text(text)
            for j, chunk in enumerate(chunks):
                doc = Document(
                    page_content=chunk,
                    metadata={
                        "doc_id": i,
                        "chunk_id": j,
                        "timestamp": datetime.now().isoformat()
                    }
                )
                all_documents.append(doc)

        print(f"  {len(all_documents)} chunk oluşturuldu")

        self.vectorstore = Chroma.from_documents(
            documents=all_documents,
            embedding=self.embeddings,
            collection_name=self.collection_name
        )

        print(" Vektör store hazır!")
        return len(all_documents)

    def format_docs(self, docs):
        """Dokümanları formatla"""
        return "\n\n".join(doc.page_content for doc in docs)

    @traceable(
        run_type="chain",
        name="Setup RAG Chain",
        tags=["setup", "chain-config"]
    )
    def setup_chain(self):
        """RAG chain'i kur (LCEL kullanarak)"""
        if not self.vectorstore:
            raise ValueError("Önce dokümanları yükleyin!")

        self.retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": 3}
        )
        prompt = ChatPromptTemplate.from_template(self.template)

        self.chain = (
                {
                    "context": self.retriever | self.format_docs,
                    "question": RunnablePassthrough()
                }
                | prompt
                | self.llm
                | StrOutputParser()
        )
        print("  RAG Chain kuruldu!")

    @traceable(
        run_type="chain",
        name="Ask Question",
        tags=["query", "main-flow"],
        metadata={"version": "1.0"}
    )
    def ask(self, question: str, run_name: str = None):
        if not self.chain or not self.retriever:
            raise ValueError("Önce setup_chain() çağrılmalı!")

        start_time = time.time()
        print(f"\n Soru: {question}")

        source_docs = self.retriever.invoke(
            question,
            config={"run_name": f"Retrieval for: {question[:30]}..."}
        )

        answer = self.chain.invoke(
            question,
            config={
                "metadata": {
                    "question_length": len(question),
                    "timestamp": datetime.now().isoformat(),
                    "user_type": "demo"
                },
                "tags": ["production", "v1"],
                "run_name": run_name or f"Query: {question[:30]}..."
            }
        )

        current_run_id = get_run_id()
        elapsed_time = time.time() - start_time

        print(f" Cevap: {answer}")
        print(f"  Süre: {elapsed_time:.2f}s")
        print(f"  {len(source_docs)} kaynak kullanıldı")

        return {
            "answer": answer,
            "source_documents": source_docs,
            "elapsed_time": elapsed_time,
            "run_id": str(current_run_id) if current_run_id else None
        }

    @traceable(
        run_type="tool",
        name="Collect Feedback"
    )
    def add_feedback(self, run_id: str, score: float, comment: str = ""):
        """Kullanıcı feedback'i ekle (0.0 = kötü, 1.0 = iyi)"""
        if not langsmith_client:
            print("   Feedback (LangSmith kapalı):", "Puan:", score, "Yorum:", comment)
            return

        if not run_id:
            print("Hata: Geçerli bir run_id olmadan feedback eklenemez.")
            return

        try:
            langsmith_client.create_feedback(
                run_id=run_id,
                key="user_rating",
                score=score,
                comment=comment
            )
            print(f"   LangSmith Feedback eklendi (Run ID: {run_id}, Puan: {score})")
        except Exception as e:
            print(f"Hata: LangSmith'e feedback eklenirken sorun oluştu: {e}")