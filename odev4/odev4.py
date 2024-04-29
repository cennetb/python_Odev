import sqlite3
from islemler import metinleri_veritabanindan_temizle
from islemler import metinleri_veritabanina_yukle
from islemler import kosinus_benzerlik


metin1 = input("İlk metni giriniz: ")
metin2 = input("İkinci metni giriniz: ")

metinleri_veritabanindan_temizle()

metinleri_veritabanina_yukle(metin1, metin2)

baglanti = sqlite3.connect('metinler.db')
imlec = baglanti.cursor()
imlec.execute("SELECT metin FROM metinler")
metinler = imlec.fetchall()
baglanti.close()

benzerlik_orani = kosinus_benzerlik(metinler[0][0], metinler[1][0])

print(f"Metinler arasındaki Kosinus benzerlik katsayısı: {benzerlik_orani}")

with open('benzerlik durumu.txt', 'w') as dosya:
    dosya.write(f"Metinler arasındaki benzerlik katsayısı: {benzerlik_orani}")
