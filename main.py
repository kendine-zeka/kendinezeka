from flask import Flask, request, jsonify
import json
import difflib
import os
import random

app = Flask(__name__)

DOSYA_ADI = "veri.json"

ozel_cevaplar = {
    "zaman": ["Zaman hızlı geçiyor değil mi knk?", "Valla zaman uçuyo knk."],
    "göz": ["Gözler yalan söylemez.", "Gözlerinden belli knk."],
    "gitmek": ["Gitmek bazen kalmaktan iyidir.", "Gidene dur denmez knk."],
    "güzellik": ["Güzellik detayda gizlidir.", "İç güzellik önemli knk."],
    "koşmak": ["Koşarsan yakalarsın.", "Koş da yakala knk."],
    "yemek": ["Acıktım la.", "Karnım zil çalıyor knk."],
    "nasılsın": ["İyiyim knk sen?", "Kötüyüm knk sen?"],
}

rastgele_sorular = [
    "Bugün hava güzel değil mi?",
    "Sence yapay zeka dünyayı ele geçirir mi?",
    "Gece mi gündüz mü seversin?",
    "Çay mı kahve mi knk?",
    "Hayat nasıl gidiyo?"
]

# Önceki verileri yükle
if os.path.exists(DOSYA_ADI):
    with open(DOSYA_ADI, "r", encoding="utf-8") as f:
        ozel_cevaplar.update(json.load(f))

def en_yakin_kelime(kelime, sozluk):
    eslesen = difflib.get_close_matches(kelime, sozluk.keys(), n=1, cutoff=0.7)
    return eslesen[0] if eslesen else None

@app.route("/", methods=["POST"])
def cevap_ver():
    data = request.get_json()
    mesaj = data.get("mesaj", "").lower()

    if mesaj.startswith("::"):
        yeni_soru = mesaj[2:].strip()
        if yeni_soru:
            rastgele_sorular.append(yeni_soru)
            return jsonify({"cevap": "Yeni rastgele soru eklendi knk."})

    elif mesaj.startswith(":"):
        return jsonify({"cevap": random.choice(rastgele_sorular)})

    else:
        cevaplar = []
        for kelime in mesaj.split():
            if kelime in ozel_cevaplar:
                cevaplar.append(random.choice(ozel_cevaplar[kelime]))
            else:
                yakin = en_yakin_kelime(kelime, ozel_cevaplar)
                if yakin:
                    cevaplar.append(random.choice(ozel_cevaplar[yakin]))
        if not cevaplar:
            return jsonify({"cevap": "Bunu pek anlayamadım knk."})
        return jsonify({"cevap": " ".join(cevaplar)})

if __name__ == "__main__":
    app.run()
