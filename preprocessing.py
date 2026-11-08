"""Preprocessing teks ulasan.

Fungsi `bersihkan` HARUS sama dengan yang dipakai saat melatih model di Google Colab
(Tugas Besar ML Part 2, USE_STEMMING = False), supaya hasil prediksi konsisten.
"""
import re

NORMAL = {"gak": "tidak", "ga": "tidak", "nggak": "tidak", "ngga": "tidak", "tdk": "tidak", "gk": "tidak",
          "yg": "yang", "dgn": "dengan", "dg": "dengan", "utk": "untuk", "krn": "karena", "karna": "karena",
          "sdh": "sudah", "udah": "sudah", "udh": "sudah", "blm": "belum", "jg": "juga", "bgt": "banget",
          "tp": "tapi", "brg": "barang", "dr": "dari", "bs": "bisa", "trs": "terus", "sy": "saya",
          "lbh": "lebih", "cepet": "cepat", "bgus": "bagus", "mantul": "mantap", "mantab": "mantap",
          "recomended": "rekomendasi", "rekomen": "rekomendasi", "oke": "ok", "makasih": "terimakasih"}

STOP = set("yang dan di ke dari ini itu untuk dengan pada adalah juga atau saya aku ada akan sudah "
           "oleh karena sebagai dalam nya sih deh dong kok ya".split())
# Kata negasi/penentu sentimen tidak boleh dibuang agar makna tidak hilang
JANGAN_DIBUANG = {"tidak", "bukan", "belum", "kurang", "jangan", "tanpa", "sangat", "banget"}
STOP -= JANGAN_DIBUANG


def bersihkan(teks: str) -> str:
    teks = re.sub(r"http\S+", " ", str(teks).lower())      # huruf kecil + hapus URL
    teks = re.sub(r"[^a-z\s]", " ", teks)                  # hapus angka, emoji, tanda baca
    teks = re.sub(r"(.)\1{2,}", r"\1\1", teks)             # "bagusssss" -> "baguss"
    kata = [NORMAL.get(k, k) for k in teks.split()]        # normalisasi kata tidak baku
    kata = [k for k in kata if k not in STOP and len(k) > 1]
    return " ".join(kata)
