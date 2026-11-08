"""Aplikasi web analisis sentimen ulasan produk Tokopedia (Flask + Vue.js).

Menjalankan: python app.py  ->  buka http://127.0.0.1:5000
"""
import os

import joblib
import numpy as np
from flask import Flask, jsonify, render_template, request

from preprocessing import bersihkan

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KANDIDAT_MODEL = [
    os.environ.get("MODEL_PATH"),
    os.path.join(BASE_DIR, "model", "model_sentimen_final.pkl"),
    os.path.join(BASE_DIR, "model", "model_sentimen_final.pth"),
]
LABEL_ID = {"negative": "Negatif", "neutral": "Netral", "positive": "Positif"}
MAKS_KARAKTER = 2000

app = Flask(__name__)


def muat_model():
    """Memuat model hasil pelatihan di Google Colab (pipeline TF-IDF + classifier)."""
    for path in KANDIDAT_MODEL:
        if path and os.path.exists(path):
            return joblib.load(path), path
    return None, None


model, model_path = muat_model()


def hitung_probabilitas(teks_bersih):
    """Probabilitas tiap kelas. Jika model tidak punya predict_proba (mis. LinearSVC), pakai softmax."""
    if hasattr(model, "predict_proba"):
        p = model.predict_proba([teks_bersih])[0]
    else:
        skor = np.atleast_2d(model.decision_function([teks_bersih]))[0]
        e = np.exp(skor - skor.max())
        p = e / e.sum()
    return {str(k): float(v) for k, v in zip(model.classes_, p)}


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify({"status": "ok" if model is not None else "model belum dimuat",
                    "model_file": os.path.basename(model_path) if model_path else None})


@app.post("/predict")
def predict():
    if model is None:
        return jsonify({"error": "Model belum ditemukan. Letakkan model_sentimen_final.pkl di folder model/."}), 503

    data = request.get_json(silent=True) or {}
    teks = str(data.get("teks", "")).strip()
    if not teks:
        return jsonify({"error": "Teks ulasan tidak boleh kosong."}), 400
    if len(teks) > MAKS_KARAKTER:
        return jsonify({"error": f"Teks terlalu panjang (maksimal {MAKS_KARAKTER} karakter)."}), 400

    bersih = bersihkan(teks)
    if not bersih:
        return jsonify({"error": "Teks tidak mengandung kata yang dapat dianalisis. Coba tulis ulasan yang lebih jelas."}), 422

    label = str(model.predict([bersih])[0])
    probabilitas = hitung_probabilitas(bersih)
    return jsonify({
        "label": label,
        "label_id": LABEL_ID.get(label, label),
        "probabilitas": {LABEL_ID.get(k, k): round(v, 4) for k, v in probabilitas.items()},
        "teks_bersih": bersih,
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
