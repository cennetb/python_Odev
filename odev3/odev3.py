class Personel:
    def __init__(self, adı, departmanı, çalışma_yılı, maaşı):
        self.adı = adı
        self.departmanı = departmanı
        self.çalışma_yılı = çalışma_yılı
        self.maaşı = maaşı


class Firma:
    def __init__(self):
        self.personel_listesi = []

    def personel_ekle(self, personel):
        self.personel_listesi.append(personel)

    def personel_listele(self):
        for personel in self.personel_listesi:
            print("Adı:", personel.adı)
            print("Departmanı:", personel.departmanı)
            print("Çalışma Yılı:", personel.çalışma_yılı)
            print("Maaşı:", personel.maaşı)
            print("-------------------")

    def maaş_zammı(self, personel, zam_oranı):
        personel.maaşı *= (1 + zam_oranı / 100)

    def personel_çıkart(self, personel):
        self.personel_listesi.remove(personel)


# Örnek personeller oluşturuyoruz
personel1 = Personel("Sena", "Mühendis", 3, 20000)
personel2 = Personel("Mehmet", "Mimar", 1, 4500)

# Firma oluşturuyoruz
firma = Firma()

# Personelleri firmaya ekliyoruz
firma.personel_ekle(personel1)
firma.personel_ekle(personel2)

# Personel listesini görüntülüyoruz
print("Firmanın Personel Listesi:")
firma.personel_listele()

# Personellere zam yapıyoruz
firma.maaş_zammı(personel1, 10)

# Personel listesini tekrar görüntülüyoruz
print("\nZam Sonrası Personel Listesi:")
firma.personel_listele()

# Bir personeli çıkarıyoruz
firma.personel_çıkart(personel2)

# Personel listesini son kez görüntülüyoruz
print("\nPersonel Çıkarıldıktan Sonraki Liste:")
firma.personel_listele()