import sys
from src.assistant import DocumentAssistant
from src.data_loader import load_text_documents
import src.config


def main():
    print(" Akıllı Doküman Asistanı Başlatılıyor...")
    print(" Çıkmak için 'exit' veya 'quit' yazın.\n")

    assistant = DocumentAssistant(collection_name="langsmith_interactive_chat")

    try:
        docs = load_text_documents(data_dir="data")
        if not docs:
            print("Hata: 'data' klasöründe yüklenecek doküman bulunamadı.")
            sys.exit(1)
        print("Dokümanlar yükleniyor...")
        assistant.load_documents(docs)
    except Exception as e:
        print(f"Hata: Dokümanlar yüklenemedi: {e}")
        sys.exit(1)

    assistant.setup_chain()

    print("\n Asistan hazır. Sorularınızı sorabilirsiniz.")
    print("-" * 60)

    while True:
        try:
            question = input(" Soru: ")
            if question.lower() in ['exit', 'quit', 'çıkış']:
                print("Görüşmek üzere!")
                break

            if not question.strip():
                continue

            result = assistant.ask(question, run_name="Interactive Chat Query")

            if result.get("run_id"):
                feedback_input = input("   Cevap yardımcı oldu mu? (e/h/enter=geç): ").lower()
                if feedback_input == 'e':
                    assistant.add_feedback(result["run_id"], 1.0, "Kullanıcı cevabı beğendi.")
                elif feedback_input == 'h':
                    comment = input("   Neden beğenmediniz? (Opsiyonel): ")
                    assistant.add_feedback(result["run_id"], 0.0, f"Kullanıcı beğenmedi: {comment}")

        except KeyboardInterrupt:
            print("\nÇıkılıyor...")
            break
        except Exception as e:
            print(f"Hata: {e}")


if __name__ == "__main__":
    main()