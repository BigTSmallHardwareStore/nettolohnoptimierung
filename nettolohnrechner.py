import requests
from bs4 import BeautifulSoup


# class to get user input with relevant information and set default values
class UserData:
    year = 2022
    LZZ = 1
    RE4 = 0
    STKL = 1
    KVZ = 1.30
    PVZ = 0
    ZKF = 0
    kirchensteuersatz = 8
    min_hour = 20
    max_hour = 40

    def user_input(self):
        # self.year = int(input("Abrechnungsjahr (Default: 2022): ") or self.year)
        # self.LZZ = int(input("Leistungszeitraum (Default: Jahr): ") or self.LZZ)

        # checks, if Jahresbruttolohn not empty and not negative
        while True:
            self.RE4 = input("Jahresbruttolohn: ")
            if self.RE4 != '' and int(self.RE4) >= 0:
                self.RE4 = int(self.RE4)
                break

        # checks, if Steuerklasse is allowed for BMF interface
        while True:
            stkl = int(input("Steuerklasse (Default: 1): ") or self.STKL)
            if stkl in range(1, 6):
                self.STKL = stkl
                break

        # according to BMF 2 decimal places must be indicated and German comma have to be a dot
        while True:
            try:
                self.KVZ = format(float(input("Krankenkassenzusatzbeitrag (Default: 1,30): ") or self.KVZ), ".2f")
                break
            except ValueError:
                print("Bitte geb das Komma als . ein")

        self.PVZ = int(input("Pflegezusatzbeitrag (Default: 0 = Nein) / (1 = Ja): ") or self.PVZ)

        # according to BMF 1 decimal places must be indicated and German comma have to be a dot
        while True:
            try:
                self.ZKF = format(float(input("Kinderfreibetrag (Default: 0): ") or self.ZKF), ".1f")
                break
            except ValueError:
                print("Bitte geb das Komma als . ein")

        self.kirchensteuersatz = int(input("Kirchensteuersatz (Default: 8): ") or self.kirchensteuersatz)
        self.min_hour = int(input("Mindestwochenarbeitszeit (Default: 20): ") or self.min_hour)
        self.max_hour = int(input("Maximalwochenarbeitszeit (Default: 40): ") or self.max_hour)


# to calculate tax with BMF interface and social insurance tax
class GetTaxAndSocialInsurance:
    # TODO: Besonderheiten Sachsen fehlen
    # TODO: neue Bundesländer implementieren
    LSTLZZ = 0
    SOLZLZZ = 0
    lohnsteuer = 0.00
    soli = 0.00
    kirchensteuer = 0
    arbeitslosenversicherung = 0.00
    rentenversicherung = 0
    pflegeversicherung = 0
    krankenversicherung = 0.00
    RE4 = 0

    def __init__(self, class_obj):
        self.RE4 = class_obj.RE4

        self.get_tax_from_bmf(class_obj)
        self.calculate_kirchensteuer(class_obj)
        self.calculate_arbeitslosenversicherung()
        self.calculate_rentenversicherung()
        self.calculate_pflegeversicherung(class_obj)
        self.calculate_krankenversicherung()

    def get_tax_from_bmf(self, class_obj):
        base_url = "https://www.bmf-steuerrechner.de/interface/"
        re4 = self.RE4 * 100
        request_url = f"{base_url}{class_obj.year}Version1.xhtml?code={class_obj.year}eP&LZZ={class_obj.LZZ}" \
                      f"&RE4={re4}&STKL={class_obj.STKL}&KVZ={class_obj.KVZ}&PVZ={class_obj.PVZ}" \
                      f"&ZKF={class_obj.ZKF}"
        r = requests.get(request_url)

        self.LSTLZZ = BeautifulSoup(r.content, 'xml').find('ausgabe', {'name': "LSTLZZ"}).get('value')
        self.SOLZLZZ = BeautifulSoup(r.content, 'xml').find('ausgabe', {'name': "SOLZLZZ"}).get('value')

        # Inaccuracy because BMF interface rounds up
        self.lohnsteuer = round(float(self.LSTLZZ), 2) / 100
        self.soli = round(float(self.SOLZLZZ), 2) / 100

    def calculate_kirchensteuer(self, class_obj):
        kirchensteuersatz = class_obj.kirchensteuersatz / 100
        self.kirchensteuer = self.lohnsteuer * kirchensteuersatz
        # self.kirchensteuer = math.floor(float(self.kirchensteuer))
        self.kirchensteuer = round(self.kirchensteuer, 2)
        # TODO: Kappung der Kirchensteuer. In allen Bundesländern außer Bayern

    def calculate_arbeitslosenversicherung(self):
        beitragssatz_arbeitslosen = 0.024 / 2
        beitragsbemessungsgrenze_arbeitslosen_alt = 7_050 * 12
        if self.RE4 >= beitragsbemessungsgrenze_arbeitslosen_alt:
            self.arbeitslosenversicherung = beitragsbemessungsgrenze_arbeitslosen_alt * beitragssatz_arbeitslosen
        else:
            self.arbeitslosenversicherung = self.RE4 * beitragssatz_arbeitslosen
        # self.arbeitslosenversicherung = math.floor(float(self.arbeitslosenversicherung))
        self.arbeitslosenversicherung = round(self.arbeitslosenversicherung, 2)

    def calculate_rentenversicherung(self):
        beitragssatz_renten = 0.186 / 2
        beitragsbemessungsgrenze_renten_alt = 7_050 * 12
        if self.RE4 >= beitragsbemessungsgrenze_renten_alt:
            self.rentenversicherung = beitragsbemessungsgrenze_renten_alt * beitragssatz_renten
        else:
            self.rentenversicherung = self.RE4 * beitragssatz_renten
        self.rentenversicherung = round(self.rentenversicherung, 2)

    def calculate_pflegeversicherung(self, class_obj):
        # TODO: Altersabfrage einbauen
        beitragssatz_pflege = 0.0305
        if class_obj.PVZ == 0:
            beitragssatz_pflege = beitragssatz_pflege / 2
        else:
            beitragssatz_pflege = (beitragssatz_pflege / 2) + 0.0035
        beitragsbemessungsgrenze_pflege_alt = 58_050

        if self.RE4 >= beitragsbemessungsgrenze_pflege_alt:
            self.pflegeversicherung = beitragsbemessungsgrenze_pflege_alt * beitragssatz_pflege
        else:
            self.pflegeversicherung = self.RE4 * beitragssatz_pflege
        self.pflegeversicherung = round(self.pflegeversicherung, 2)

    def calculate_krankenversicherung(self):
        beitragssatz_kranken = 0.157 / 2
        beitragsbemessungsgrenze_kranken_alt = 58_050
        if self.RE4 >= beitragsbemessungsgrenze_kranken_alt:
            self.krankenversicherung = beitragsbemessungsgrenze_kranken_alt * beitragssatz_kranken
        else:
            self.krankenversicherung = self.RE4 * beitragssatz_kranken
        self.krankenversicherung = round(self.krankenversicherung, 2)


class NetSalary(GetTaxAndSocialInsurance):
    nettolohn = 0

    def __init__(self, class_obj):
        super().__init__(class_obj=class_obj)
        self.nettolohn = self.RE4 - self.lohnsteuer - self.soli - self.kirchensteuer - self.krankenversicherung - self.pflegeversicherung - self.arbeitslosenversicherung - self.rentenversicherung
        self.nettolohn = round(self.nettolohn, 2)
