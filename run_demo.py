import time
import random
import sys
from src.assistant import DocumentAssistant
from src.data_loader import load_text_documents
import src.config
import os

def main():
    """Demo çalıştır"""
    print(" LangSmith Demo - Doküman Asistanı Başlatılıyor\n")

    assistant = DocumentAssistant(collection_name="langsmith_demo_v2")

    try:
        sample_docs = load_text_documents(data_dir="data")
        if not sample_docs:
            print("Hata: Demo dokümanları yüklenemedi. 'data' klasörünü kontrol edin.")
            sys.exit(1)
        assistant.load_documents(sample_docs)
    except Exception as e:
        print(f"Hata: Dokümanlar yüklenemedi: {e}")
        return

    assistant.setup_chain()

    print("\n" + "=" * 60)
    print(" Sorular sormaya başlayalım!")
    print("=" * 60)

    questions = [
        "Python hangi yıl geliştirildi ve kim tarafından?",
        "Makine öğrenmesinin kaç türü var?",
        "LangSmith ne işe yarar?",
        "Python'un web geliştirme için kullanılan framework'leri neler?",
        "Kuantum bilgisayar nedir?"  # Doküman dışı test sorusu
    ]

    for i, question in enumerate(questions, 1):
        print(f"\n{'=' * 60}")
        print(f"Soru {i}/{len(questions)}")
        print(f"{'=' * 60}")

        try:
            result = assistant.ask(
                question,
                run_name=f"Demo Soru {i} - {question[:20]}"
            )

            run_id = result.get("run_id")
            if run_id:
                # Simüle edilmiş feedback (0 = kötü, 1 = iyi)
                score = 0.0
                comment = ""

                if question == "Kuantum bilgisayar nedir?":
                    if "Bu bilgi dokümanda yok" in result["answer"]:
                        score = 1.0  # Başarılı: Bilmediğini doğru söyledi
                        comment = "Doğru şekilde 'bilmiyorum' dedi."
                    else:
                        score = 0.0  # Başarısız: Cevap uydurdu
                        comment = "Bilmediği halde cevap uydurdu."
                elif "Bu bilgi dokümanda yok" in result["answer"]:
                    score = 0.0  # Başarısız: Bilmesi gereken bir şeyi bilemedi
                    comment = "Dokümanda olan bilgiyi bulamadı."
                else:
                    score = 1.0  # Başarılı: Cevap verdi
                    comment = "Cevap ilgili ve doğru görünüyor."

                print(f"   Simüle feedback: {'İyi' if score == 1.0 else 'Kötü'} ({score})")

                assistant.add_feedback(run_id=run_id, score=score, comment=comment)

        except Exception as e:
            print(f"Hata: Soru sorulurken hata oluştu: {e}")

        time.sleep(1)

    print("\n" + "=" * 60)
    print(" Demo tamamlandı!")
    print("=" * 60)
    print("\n LangSmith'te şunları görebilirsiniz:")
    print("   • 'Ask Question' run'ları ve bunlara eklenen 'user_rating' feedback'leri")
    print("   • 'Load Documents' ve 'Setup RAG Chain' tool/chain'leri")
    print(f"   • Proje: {os.environ.get('LANGSMITH_PROJECT', 'default')}")
    print("\n https://smith.langchain.com/ adresinden kontrol edin!")


if __name__ == "__main__":
    main()