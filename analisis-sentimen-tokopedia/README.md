# Analisis Sentimen Ulasan Produk Makanan & Minuman Tokopedia

Aplikasi web untuk mengklasifikasikan ulasan produk menjadi **Positif**, **Netral**, atau **Negatif**.
Dibuat sebagai lanjutan **Tugas Besar Machine Learning** (Part 1: rancangan ide CRISP-DM, Part 2: preprocessing,
tuning, dan analisis model, Part 3: aplikasi).

- **Pembuat:** Rizki Fadillah (202343501889 -X7L)
- **Mata kuliah:** Machine Learning
- **Dataset:** Tokopedia Product Reviews 2025 (Kaggle), kategori Makanan & Minuman
- **Model:** pipeline TF-IDF (unigram + bigram) + Logistic Regression, dilatih di Google Colab

## Teknologi

| Lapisan | Teknologi |
|---|---|
| Frontend (User Interface) | HTML, CSS, Vue.js 3 (via CDN) |
| Backend / API | Python, Flask |
| Model | scikit-learn (disimpan dengan joblib di folder `model/`) |

## Struktur folder

```
.
├── app.py                 # server Flask + endpoint /predict
├── preprocessing.py       # fungsi pembersihan teks (sama dengan saat pelatihan)
├── model/
│   └── model_sentimen_final.pkl   # model hasil Google Colab
├── templates/index.html   # halaman utama (Vue.js)
├── static/                # style.css dan app.js
├── requirements.txt
└── README.md
```

## Cara menjalankan

1. Pastikan Python 3.9+ terpasang.
2. (Disarankan) buat virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   source .venv/bin/activate     # macOS/Linux
   ```
3. Pasang dependensi:
   ```
   pip install -r requirements.txt
   ```
   `requirements.txt` memakai scikit-learn 1.6.1, yaitu versi yang dipakai di Google Colab saat model dilatih.
   Versi yang sama diperlukan agar model dapat dimuat dengan benar.
4. Jalankan aplikasi:
   ```
   python app.py
   ```
5. Buka **http://127.0.0.1:5000** di browser, tulis ulasan, lalu klik **Analisis Sentimen**.

## API

`POST /predict`

```json
{ "teks": "telur sampai cepat, packing aman, rasanya enak, mantap" }
```

Respons:

```json
{
  "label": "positive",
  "label_id": "Positif",
  "probabilitas": { "Negatif": 0.05, "Netral": 0.05, "Positif": 0.90 },
  "teks_bersih": "telur sampai cepat packing aman rasanya enak mantap"
}
```

`GET /health` menampilkan status dan nama file model yang dimuat.

## Catatan model

- Data latih sangat tidak seimbang (ulasan positif sekitar 96,6%), sehingga dilakukan undersampling pada data latih.
- Label dibuat dari rating (1-2 negatif, 3 netral, 4-5 positif), bukan anotasi manual.
- Macro F1 pada data uji masih sekitar 0,48 dan kelas **netral** paling sulit diprediksi.
  Aplikasi ini adalah prototipe pembelajaran, bukan sistem produksi.
