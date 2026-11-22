"""Mapping form UI Kindred Care ke ontology ABK."""

AREA_TO_SIGN_CODES = {
    "communication": ["K1", "K2", "K3", "K4", "K5"],
    "hearing":       ["S1"],
    "vision":        ["S2"],
    "sensory":       ["S3", "S4"],
    "motor":         ["F1", "F2", "F3", "F5", "F6"],
    "seizure":       ["F4"],
    "learning":      ["B1", "B2", "B3", "B4", "B5"],
    "social":        ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9"],
}

RED_FLAG_SIGNS = ["K6", "P7", "F4"]

RED_FLAG_QUESTIONS = [
    {"code": "K6", "label": "Regresi perkembangan", "question": "Apakah anak pernah kehilangan kemampuan yang sudah dikuasai?"},
    {"code": "P7", "label": "Penarikan sosial / halusinasi", "question": "Apakah anak menarik diri drastis atau melihat/mendengar hal yang tidak nyata?"},
    {"code": "F4", "label": "Kejang", "question": "Apakah anak pernah kejang / kelojotan / hilang kesadaran sesaat?"},
]

DURATION_TO_MONTHS = {
    "recently": 1,
    "several_months": 6,
    "long_time": 24,
    "not_sure": 3,
}

SETTING_KEYS = ["home", "school", "with_other_children", "unfamiliar_places", "many_situations"]

# Mapping label sign untuk UI (bisa juga ambil dari ontology langsung)
SIGN_LABELS = {
    "K1": "Bicara terlambat / tidak keluar suara",
    "K2": "Artikulasi tidak jelas / gagap / suara serak",
    "K3": "Bahasa tubuh/mimik kaku / kontak mata minim",
    "K4": "Kesulitan memahami instruksi lisan",
    "K5": "Echolalia / suara tak terkontrol",
    "S1": "Tidak merespons suara / tidak menoleh jika dipanggil",
    "S2": "Gangguan penglihatan (menabrak, mendekatkan barang)",
    "S3": "Hiper/hiposensitif terhadap suara, tekstur, cahaya, sentuhan",
    "S4": "Kehilangan rasa (mati rasa) pada bagian tubuh",
    "F1": "Keterlambatan motorik (duduk/berjalan, kaku/lemas)",
    "F2": "Kelainan bentuk fisik nyata",
    "F3": "Gerakan repetitif tanpa tujuan",
    "F4": "Kejang / kelojotan / hilang kesadaran",
    "F5": "Sulit menelan / mengunyah / kontrol air liur lemah",
    "F6": "Kelemahan/kelumpuhan anggota gerak",
    "B1": "Sulit membaca / mengeja / menukar huruf mirip",
    "B2": "Tulisan sangat buruk / sulit memegang pensil",
    "B3": "Sulit memahami angka / matematika / waktu & uang",
    "B4": "Keterlambatan kecerdasan umum",
    "B5": "Mudah teralih / sulit fokus / sering lupa",
    "P1": "Hiperaktif (tak bisa diam, memotong pembicaraan)",
    "P2": "Sangat terikat rutinitas / marah jika ada perubahan",
    "P3": "Menolak perintah ekstrem / membangkang",
    "P4": "Agresif, merusak barang, melanggar aturan kronis",
    "P5": "Cemas berlebihan, takut berpisah",
    "P6": "Perilaku ritualistik berulang (cuci tangan, mengecek)",
    "P7": "Penarikan diri sosial drastis / halusinasi",
    "P8": "Masalah pola makan ekstrem",
    "P9": "Murung / mudah marah berkepanjangan, hilang minat",
    "K6": "Regresi: kehilangan kemampuan yang sudah dikuasai (RED FLAG)",
}