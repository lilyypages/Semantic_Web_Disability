# Kindred Care — Ontology-Based Knowledge System for Parents of Children with Special Needs

> Sistem pengetahuan berbasis ontology untuk membantu orang tua anak berkebutuhan khusus memahami kondisi, asesmen, terapi, dan dukungan yang relevan — bukan pengganti diagnosis klinis.

---

## 📖 Latar Belakang

Orang tua anak berkebutuhan khusus sering menghadapi kebingungan: memahami kondisi anak, mencari informasi terpercaya, memahami hasil pemeriksaan, menentukan profesional yang tepat, hingga mencari informasi terapi dan pendidikan. Informasi tersebar di berbagai sumber dan sulit dihubungkan satu sama lain.

**Kindred Care** menjawab masalah ini dengan membangun **ontology-based knowledge system** yang menyatukan pengetahuan dari berbagai bidang (perkembangan anak, asesmen, profesional, terapi, pendidikan, dukungan keluarga) ke dalam satu knowledge base. Dengan **ontology reasoning**, sistem dapat memahami keterkaitan antarpengetahuan dan menghubungkan pertanyaan orang tua dengan informasi yang relevan — terstruktur, terhubung, dan berdasarkan sumber tervalidasi ahli.

**Disclaimer:** Sistem ini bersifat **edukatif**. Tidak dapat mendiagnosis, menyingkirkan, atau merekomendasikan terapi untuk anak tertentu. Untuk kekhawatiran serius, konsultasikan ke profesional.

---

## 🎯 Dua Modul Utama

Sistem ini punya **dua modul** yang saling melengkapi:

### 1. 📚 Knowledge Library — *"Saya ingin belajar tentang suatu topik"*

Modul untuk **menjelajahi pengetahuan** secara mandiri. Orang tua bisa browse kategori, kondisi, tanda, asesmen, profesional, terapi, pendidikan, dan dukungan. Setiap halaman kondisi menampilkan 10 area pengetahuan terstruktur yang terhubung ke ontology.

**Cocok untuk:**
- Orang tua yang sudah tahu topik yang ingin dipelajari
- Mencari informasi umum tentang kondisi tertentu
- Memahami istilah (asesmen, profesional, terapi)
- Belajar sebelum/ sesudah konsultasi dengan profesional

**Alur:** `index.html` → `library.html` → `condition.html`

**Teknologi:** Static HTML + CSS. Konten bisa di-generate dari ontology (via SPARQL) atau diisi manual dari sumber tervalidasi.

---

### 2. 🔍 Guided Exploration — *"Saya ingin memahami apa yang saya amati pada anak"*

Modul **tanya-jawab terpandu** untuk orang tua yang belum tahu harus mulai dari mana. Sistem memandu dengan pertanyaan bertahap, lalu menjalankan **ontology reasoning** untuk menemukan topik/kondisi yang relevan berdasarkan tanda-tanda yang dipilih.

**Cocok untuk:**
- Orang tua yang bingung harus mencari apa
- Ingin memahami apakah yang diamati termasuk tanda yang perlu diperhatikan
- Mencari tahu profesional/asesmen apa yang relevan

**Alur:** `index.html` → `profile.html` → `basics.html` → `questions.html` → `results.html`

**Teknologi:** Flask + `owlready2` + HermiT reasoner + `scikit-fuzzy`.

**Yang terjadi di balik layar:**
1. User memilih area concern (komunikasi, pendengaran, dll.)
2. Sistem menampilkan **checklist tanda spesifik** (Sign K1–P9) dari ontology
3. User mencentang tanda yang diamati + durasi + lokasi pengamatan
4. Flask membuat `ChildCase` sementara di ontology
5. HermiT reasoner menginferensi class turunan (`SuspectedASD`, `SuspectedADHDCombined`, `RedFlagCase`, dll.)
6. Query `hasCoreSign` / `hasSupportingSign` untuk menemukan kondisi terkait
7. Fuzzy system menghitung skor urgensi (0–100)
8. Hasil ditampilkan di `results.html` dengan **evidence** (kenapa topik muncul) dan **rekomendasi** (asesmen, profesional, terapi)

**Fitur khusus:**
- **Red flag detection** — tanda regresi (K6), halusinasi/penarikan sosial (P7), dan kejang (F4) otomatis memicu peringatan rujukan segera
- **Evidence transparency** — setiap topik yang muncul disertai alasan (sign mana yang match)
- **Tidak ada diagnosis** — sistem hanya menampilkan topik untuk dieksplorasi lebih lanjut

---

## 🏗️ Arsitektur
