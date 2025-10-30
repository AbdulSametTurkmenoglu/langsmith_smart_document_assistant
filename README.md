# LangSmith ile Akıllı Doküman Asistanı (RAG)

Bu proje, LangChain, OpenAI ve ChromaDB kullanarak bir RAG (Retrieval-Augmented Generation) sistemi oluşturur ve tüm süreci izlemek, debug etmek ve değerlendirmek için **LangSmith**'i kullanır.

Asistan, `data/` klasöründeki metin dosyalarını okur, bunları vektörlere dönüştürür ve kullanıcı sorularını bu dokümanlara dayanarak cevaplar.

##  Özellikler

* **RAG Mimarisi:** Dokümanlardan bağlam (context) alarak cevap üreten sistem.
* **LangSmith Entegrasyonu:**
    * `@traceable` decorator'ları ile tüm adımlar (doküman yükleme, chain kurulumu, soru sorma) izlenir.
    * Token kullanımı, maliyet ve gecikme süreleri otomatik olarak takip edilir.
    * **Feedback Toplama:** Her soru-cevap çiftine `user_rating` (0 veya 1) ile puan verme ve bu puanları LangSmith arayüzünde görme.
* **Modüler Yapı:** Veri, konfigürasyon, prompt'lar ve ana mantık `src/` klasöründe ayrılmıştır.
* **İki Çalıştırma Modu:**
    1.  `run_demo.py`: Önceden tanımlanmış sorularla bir demo çalıştırır ve otomatik (simüle edilmiş) feedback gönderir.
    2.  `chat.py`: Asistanla interaktif sohbet etmenizi ve her cevaba manuel olarak (e/h) feedback vermenizi sağlar.


##  Kurulum

1.  **Depoyu Klonlama:**
    ```bash
    git clone [https://github.com/AbdulSametTurkmenoglu/lang_smith_akilli_dokuman_asistani.git](https://github.com/AbdulSametTurkmenoglu/lang_smith_akilli_dokuman_asistani.git)
    cd lang_smith_akilli_dokuman_asistani
    ```

2.  **Sanal Ortam (Önerilir):**
    ```bash
    python -m venv .venv
    # Windows: .\.venv\Scripts\activate
    # macOS/Linux: source .venv/bin/activate
    ```

3.  **Gerekli Kütüphaneleri Yükleme:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **.env Dosyasını Oluşturma:**
    `.env.example` dosyasını kopyalayıp `.env` olarak adlandırın ve içini kendi API anahtarlarınızla doldurun:
    ```bash
    # Windows
    copy .env.example .env
    
    # macOS / Linux
    cp .env.example .env
    ```
    `.env` dosyasının içeriği:
    ```
    OPENAI_API_KEY="sk-..."
    LANGSMITH_API_KEY="..."
    LANGSMITH_PROJECT="Akilli Dokuman Asistani" # LangSmith'te görünecek proje adı
    ```

##  Kullanım

İki farklı modda çalıştırabilirsiniz:

### 1. Demo Modu (`run_demo.py`)

Bu script, `data/` klasöründeki dokümanları yükler, `questions` listesindeki soruları sırayla sorar ve her cevap için otomatik olarak (simüle edilmiş) bir puanı (0 veya 1) LangSmith'e gönderir.

```bash
python run_demo.py
```
Bu modu çalıştırdıktan sonra LangSmith arayüzüne giderek projeniz altındaki "Ask Question" run'larını ve onlara bağlı "user_rating" skorlarını görebilirsiniz.

### 2. İnteraktif Sohbet Modu (`chat.py`)

Bu script, asistanla gerçek zamanlı sohbet etmenizi sağlar. Her cevaptan sonra size "Yardımcı oldu mu? (e/h)" diye sorar ve cevabınıza göre (1.0 veya 0.0) puanı LangSmith'e kaydeder.

```bash
python chat.py
```
```
 Asistan hazır. Sorularınızı sorabilirsiniz.
------------------------------------------------------------
 Soru: LangSmith nedir?
 Cevap: LangSmith, LangChain uygulamalarını izlemek ve debug etmek için kullanılan bir araçtır. Her chain çağrısı, token kullanımı ve hatalar LangSmith'te görülebilir.
  Süre: 1.23s
  3 kaynak kullanıldı
   Cevap yardımcı oldu mu? (e/h/enter=geç): e
   LangSmith Feedback eklendi (Puan: 1.0)
 Soru: 
```