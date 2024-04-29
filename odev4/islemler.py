import sqlite3

def metinleri_veritabanina_yukle(metin1, metin2):
    baglanti = sqlite3.connect('metinler.db')
    imlec = baglanti.cursor()
    imlec.execute('''CREATE TABLE IF NOT EXISTS metinler
                      (id INTEGER PRIMARY KEY, metin TEXT)''')
    imlec.execute("INSERT INTO metinler (metin) VALUES (?)", (metin1,))
    imlec.execute("INSERT INTO metinler (metin) VALUES (?)", (metin2,))
    baglanti.commit()
    baglanti.close()

def metinleri_veritabanindan_temizle():
    baglanti = sqlite3.connect('metinler.db')
    imlec = baglanti.cursor()
    imlec.execute("DELETE FROM metinler")
    baglanti.commit()
    baglanti.close()

def kosinus_benzerlik(metin1, metin2):
    kelimeler1 = metin1.lower().split()
    kelimeler2 = metin2.lower().split()
    kelimeler = set(kelimeler1).union(set(kelimeler2))

    sayim1 = {kelime: kelimeler1.count(kelime) for kelime in kelimeler}
    sayim2 = {kelime: kelimeler2.count(kelime) for kelime in kelimeler}

    skaler_carpim = sum(sayim1[kelime] * sayim2[kelime] for kelime in kelimeler)
    vektor1_buyuklugu = sum(sayim1[kelime] ** 2 for kelime in kelimeler) ** 0.5
    vektor2_buyuklugu = sum(sayim2[kelime] ** 2 for kelime in kelimeler) ** 0.5

    return skaler_carpim / (vektor1_buyuklugu * vektor2_buyuklugu)
