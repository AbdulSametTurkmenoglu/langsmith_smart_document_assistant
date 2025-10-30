import os
from glob import glob


def load_text_documents(data_dir: str = "data") -> list[str]:
    """'data/' klasöründeki tüm .txt dosyalarını okur."""
    text_files = glob(os.path.join(data_dir, "*.txt"))

    if not text_files:
        print(f"Uyarı: '{data_dir}' klasöründe .txt dosyası bulunamadı.")
        return []

    print(f"{len(text_files)} adet doküman bulundu: {text_files}")

    all_texts = []
    for file_path in text_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                all_texts.append(f.read())
        except Exception as e:
            print(f"Hata: {file_path} dosyası okunurken hata: {e}")

    return all_texts