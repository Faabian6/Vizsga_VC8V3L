from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class Bicikli(ABC):
    def __init__(self, bicikli_id, tipus, ar, allapot):
        self.bicikli_id = bicikli_id
        self.tipus = tipus
        self.ar = ar
        self.allapot = allapot

    @abstractmethod
    def get_bicikli_info(self):
        pass

class OrszagutiBicikli(Bicikli):
    def __init__(self, bicikli_id, ar, allapot):
        super().__init__(bicikli_id, "Országúti", ar, allapot)

    def get_bicikli_info(self):
        return f"Országúti bicikli #{self.bicikli_id}, Ár: {self.ar} Ft, Állapot: {self.allapot}"

class HegyiBicikli(Bicikli):
    def __init__(self, bicikli_id, ar, allapot):
        super().__init__(bicikli_id, "Hegyi", ar, allapot)

    def get_bicikli_info(self):
        return f"Hegyi bicikli #{self.bicikli_id}, Ár: {self.ar} Ft, Állapot: {self.allapot}"

class ElektromosBicikli(Bicikli):
    def __init__(self, bicikli_id, ar, allapot):
        super().__init__(bicikli_id, "Ebike", ar, allapot)

    def get_bicikli_info(self):
        return f"Ebike #{self.bicikli_id}, Ár: {self.ar} Ft, Állapot: {self.allapot}"

class Kolcsonzo:
    def __init__(self, nev):
        self.nev = nev
        self.biciklik = []
        self.kolcsonzesek = []

    def add_bicikli(self, bicikli):
        self.biciklik.append(bicikli)

    def remove_bicikli(self, bicikli_id):
        self.biciklik = [bicikli for bicikli in self.biciklik if bicikli.bicikli_id != bicikli_id]

    def list_biciklik(self):
        if not self.biciklik:
            print("Nincsenek biciklik a kölcsönzőben.")
        else:
            print("Elérhető biciklik:")
            for bicikli in self.biciklik:
                print(bicikli.get_bicikli_info())

    def kolcsonzes_foglalas(self, bicikli_id, kezdeti_idopont, vegdatum):
        bicikli = next((b for b in self.biciklik if b.bicikli_id == bicikli_id), None)
        jelenlegi_idopont = datetime.now()

        if bicikli and bicikli.allapot == "Elérhető" and kezdeti_idopont >= jelenlegi_idopont and vegdatum > kezdeti_idopont:
            kolcsonzes = Kolcsonzes(bicikli, self, kezdeti_idopont, vegdatum)
            self.kolcsonzesek.append(kolcsonzes)
            bicikli.allapot = "Kölcsönözve"
            print(f"A foglalás sikeres. Kezdeti időpont: {kezdeti_idopont}, Végdátum: {vegdatum}")
        elif bicikli and bicikli.allapot == "Kölcsönözve":
            print("A bicikli már ki van kölcsönözve.")
        elif bicikli:
            if bicikli.allapot != "Elérhető":
                print("A bicikli jelenleg nem elérhető.")
            elif kezdeti_idopont < jelenlegi_idopont:
                print("A kezdeti időpont nem lehet a múltban.")
            else:
                print("A végdátum nem megfelelő.")
        else:
            print("Hibás bicikli azonosító.")

    def kolcsonzes_lemondas(self, bicikli_id):
        kolcsonzes = next((k for k in self.kolcsonzesek if k.bicikli.bicikli_id == bicikli_id), None)
        if kolcsonzes and kolcsonzes.kezdeti_idopont >= datetime.now():
            kolcsonzes.befejezes()
            self.kolcsonzesek.remove(kolcsonzes)
            kolcsonzes.bicikli.allapot = "Elérhető"
            print(f"A kölcsönzés lemondva.")
        elif kolcsonzes:
            print("A kölcsönzés már nem lemondható, mert a kezdeti időpont lejárt.")
        else:
            print("Ez a bicikli még elérhető, kérem ellenőrizze listában.")

    def list_kolcsonzesek(self):
        for kolcsonzes in self.kolcsonzesek:
            print(f"{kolcsonzes.bicikli.get_bicikli_info()}, Kölcsönző: {self.nev}, Kezdeti időpont: {kolcsonzes.kezdeti_idopont}, Befejezési időpont: {kolcsonzes.vegdatum}")

class Kolcsonzes:
    def __init__(self, bicikli, kolcsonzo, kezdeti_idopont, vegdatum):
        self.bicikli = bicikli
        self.kolcsonzo = kolcsonzo
        self.kezdeti_idopont = kezdeti_idopont
        self.vegdatum = vegdatum
        # A kölcsönzés lejárati dátuma a kezdeti időponthoz hozzáadott időszak lesz
        #self.kolcsonzes_lejarat = kezdeti_idopont + timedelta(days=(vegdatum - kezdeti_idopont).days)

    def befejezes(self):
        befejezesi_idopont = datetime.now()
        kozos_idotartam = befejezesi_idopont - self.kezdeti_idopont
        koltseg = kozos_idotartam.total_seconds() // 3600 * self.bicikli.ar
        print(f"A kölcsönzés véget ért. Költség: {koltseg} Ft.")


def main():
    kolcsonzo = Kolcsonzo("BikeRent")

    # Biciklik létrehozása és hozzáadása a kölcsönzőhöz
    orszag1 = OrszagutiBicikli(1, 1000, "Elérhető")
    orszag2 = OrszagutiBicikli(2, 1000, "Elérhető")
    hegy1 = HegyiBicikli(3, 1550, "Elérhető")
    hegy2 = HegyiBicikli(4, 1550, "Elérhető")
    ebike1 = ElektromosBicikli(5, 3600, "Elérhető")
    ebike2 = ElektromosBicikli(6, 3600, "Elérhető")

    kolcsonzo.add_bicikli(orszag1)
    kolcsonzo.add_bicikli(orszag2)
    kolcsonzo.add_bicikli(hegy1)
    kolcsonzo.add_bicikli(hegy2)
    kolcsonzo.add_bicikli(ebike1)
    kolcsonzo.add_bicikli(ebike2)

    # Kölcsönzések létrehozása
    kezdeti_idopont1 = datetime.now() + timedelta(days=1)
    vegdatum1 = kezdeti_idopont1 + timedelta(days=5)
    kezdeti_idopont2 = datetime.now() + timedelta(days=4)
    vegdatum2 = kezdeti_idopont2 + timedelta(days=8)

    kolcsonzo.kolcsonzes_foglalas(1, kezdeti_idopont1, vegdatum1 )
    kolcsonzo.kolcsonzes_foglalas(5, kezdeti_idopont2, vegdatum2)

    kolcsonzo.list_kolcsonzesek()

    while True:
        print("\nVálassz műveletet:")
        print("1. Biciklik listázása")
        print("2. Kölcsönzés foglalása")
        print("3. Kölcsönzés lemondása")
        print("4. Kölcsönzések listázása")
        print("5. Kilépés")

        valasztas = input("Adja meg a választott művelet számát: ")

        if valasztas == "1":
            kolcsonzo.list_biciklik()
        elif valasztas == "2":
            bicikli_id = input("Adja meg a kölcsönözni kívánt bicikli azonosítóját: ")
            kezdeti_idopont = input("Adja meg a kezdeti időpontot (YYYY-MM-DD): ")
            kezdeti_idopont = datetime.strptime(kezdeti_idopont, "%Y-%m-%d")
            vegdatum = input("Adja meg a befejezési időpontot (YYYY-MM-DD): ")
            vegdatum = datetime.strptime(vegdatum, "%Y-%m-%d")
            kolcsonzo.kolcsonzes_foglalas(int(bicikli_id), kezdeti_idopont, vegdatum)
        elif valasztas == "3":
            bicikli_id = input("Adja meg a lemondani kívánt kölcsönzés bicikli azonosítóját: ")
            kolcsonzo.kolcsonzes_lemondas(int(bicikli_id))
        elif valasztas == "4":
            kolcsonzo.list_kolcsonzesek()
        elif valasztas == "5":
            print("Köszönjük, hogy használta a BikeRent rendszert. Viszlát!")
            break
        else:
            print("Érvénytelen választás. Kérem, válasszon újra.")

if __name__ == "__main__":
    main()
