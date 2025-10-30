import os
from dotenv import load_dotenv
from langsmith import Client

load_dotenv()

if "OPENAI_API_KEY" not in os.environ:
    raise EnvironmentError("OPENAI_API_KEY .env dosyasında bulunamadı")

if "LANGSMITH_API_KEY" not in os.environ:
    print("Uyarı: LANGSMITH_API_KEY bulunamadı. LangSmith izlemesi devre dışı.")
    langsmith_client = None
else:
    langsmith_client = Client()
    print(f"LangSmith izlemesi aktif. Proje: {os.environ.get('LANGSMITH_PROJECT', 'default')}")