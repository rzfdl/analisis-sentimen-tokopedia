const { createApp } = Vue;

createApp({
  data() {
    return {
      teks: "",
      loading: false,
      error: "",
      hasil: null,
      riwayat: [],
      contoh: [
        "telur sampai cepat, packing aman, rasanya enak, mantap",
        "telur busuk semua, sangat kecewa, tolong ganti",
        "barang sesuai pesanan tapi pengiriman agak lama dan kemasan sedikit penyok",
      ],
    };
  },
  methods: {
    kelasCss(nama) {
      return { Positif: "positive", Netral: "neutral", Negatif: "negative" }[nama] || "";
    },
    reset() {
      this.teks = "";
      this.hasil = null;
      this.error = "";
    },
    async analisis() {
      if (!this.teks.trim()) return;
      this.loading = true;
      this.error = "";
      try {
        const res = await fetch("/predict", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ teks: this.teks }),
        });
        const data = await res.json();
        if (!res.ok) {
          this.error = data.error || "Terjadi kesalahan pada server.";
          this.hasil = null;
        } else {
          this.hasil = data;
          this.riwayat.unshift({ teks: this.teks, label: data.label, label_id: data.label_id });
          this.riwayat = this.riwayat.slice(0, 8);
        }
      } catch (e) {
        this.error = "Tidak dapat terhubung ke server. Pastikan aplikasi (python app.py) sedang berjalan.";
        this.hasil = null;
      } finally {
        this.loading = false;
      }
    },
  },
}).mount("#app");
