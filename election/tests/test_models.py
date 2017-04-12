import os, sys, pandas, django, time
from django.test import TestCase
from election.models import Voivodeship, District, Commune, Circuit, Candidate, Vote, Country

class ModelTestCase(TestCase):

    CANDIDATES = ["Dariusz Maciej GRABOWSKI", "Piotr IKONOWICZ", "Jarosław KALINOWSKI", "Janusz KORWIN-MIKKE",
                  "Marian KRZAKLEWSKI", "Aleksander KWAŚNIEWSKI", "Andrzej LEPPER", "Jan ŁOPUSZAŃSKI",
                  "Andrzej Marian OLECHOWSKI", "Bogdan PAWŁOWSKI", "Lech WAŁĘSA", "Tadeusz Adam WILECKI"]

    def setUp(self):
        df = pandas.read_csv("C:\\zawadzkm\\www\\www_zad2\\data\\test_data.csv", sep=";")

        cands = {}

        for n in (ModelTestCase.CANDIDATES):
            cand = Candidate.objects.get_or_create(name=n)
            cands[n] = cand

        gr = df[["Uprawnieni", "Wydanekarty", "Oddane", "Wazne", "Niewazne"]].sum()

        p = Country.objects.get_or_create(name="Polska", entitled=gr["Uprawnieni"], cards=gr["Wydanekarty"],
                                          votes=gr["Oddane"], valid=gr["Wazne"], invalid=gr["Niewazne"])

        for i, row in df.iterrows():
            gr = df[df["Nrwoj"] == row["Nrwoj"]][["Uprawnieni", "Wydanekarty", "Oddane", "Wazne", "Niewazne"]].sum()
            v = Voivodeship.objects.get_or_create(country=p[0], no=row["Nrwoj"], name=row["Wojewodztwo"],
                                                      entitled=gr["Uprawnieni"], cards=gr["Wydanekarty"],
                                                      votes=gr["Oddane"], valid=gr["Wazne"], invalid=gr["Niewazne"])

            gr = df[df["Nrokr"] == row["Nrokr"]][["Uprawnieni", "Wydanekarty", "Oddane", "Wazne", "Niewazne"]].sum()
            d = District.objects.get_or_create(voivodeship=v[0], no=row["Nrokr"], name=row["Okreg"],
                                                   entitled=gr["Uprawnieni"], cards=gr["Wydanekarty"], votes=gr["Oddane"],
                                                   valid=gr["Wazne"], invalid=gr["Niewazne"])

            gr = df[df["Kodgminy"] == row["Kodgminy"]][
                    ["Uprawnieni", "Wydanekarty", "Oddane", "Wazne", "Niewazne"]].sum()
            c = Commune.objects.get_or_create(district=d[0], name=row["Gmina"], code=row["Kodgminy"],
                                                  entitled=gr["Uprawnieni"], cards=gr["Wydanekarty"], votes=gr["Oddane"],
                                                  valid=gr["Wazne"], invalid=gr["Niewazne"])

            cc = Circuit.objects.create(commune=c[0], no=row["Nrobw"], address=row["Adres"], entitled=row["Uprawnieni"],
                                        cards=row["Wydanekarty"], votes=row["Oddane"], valid=row["Wazne"],
                                        invalid=row["Niewazne"])

            objs = [
                Vote(candidate=cands[n][0], circuit=cc, number=row[n]
                     ) for n in ModelTestCase.CANDIDATES
            ]
            Vote.objects.bulk_create(objs)

    def test_country(self):
        c = Country.objects.get(name="Polska")
        self.assertEquals(c.entitled, 69662)
        self.assertEquals(c.cards, 40208)
        self.assertEquals(c.votes, 40189)
        self.assertEquals(c.valid, 39670)
        self.assertEquals(c.invalid, 519)
        self.assertEquals(c.valid+c.invalid, c.votes)
        self.assertEquals(c.attendance, 57.69)

        votes = [226, 72, 3261, 507, 6703, 20743, 1353, 320, 5916, 57, 435, 77]
        for i, v in enumerate(votes):
            self.assertEquals(c.candidates.get(name=ModelTestCase.CANDIDATES[i]).votes, v)

    def test_voivodeship(self):
        v = Voivodeship.objects.get(name="Mazowieckie")
        self.assertEquals(v.entitled, 48746)
        self.assertEquals(v.cards, 28882)
        self.assertEquals(v.votes, 28878)
        self.assertEquals(v.valid, 28551)
        self.assertEquals(v.invalid, 327)
        self.assertEquals(v.valid+v.invalid, v.votes)
        self.assertEquals(v.attendance, 59.24)

        votes = [137, 58, 2244, 400, 4271, 15658, 795, 240, 4378, 47, 274, 49]
        for i, vv in enumerate(votes):
            self.assertEquals(v.candidates.get(name=ModelTestCase.CANDIDATES[i]).votes, vv)

    def test_district(self):
        d = District.objects.get(name="Krosno")
        self.assertEquals(d.entitled, 15925)
        self.assertEquals(d.cards, 8647)
        self.assertEquals(d.votes, 8636)
        self.assertEquals(d.valid, 8495)
        self.assertEquals(d.invalid, 141)
        self.assertEquals(d.valid+d.invalid, d.votes)
        self.assertEquals(d.attendance, 54.23)

        votes = [62, 9, 799, 94, 1723, 3998, 423, 67, 1186, 9, 102, 23]
        for i, v in enumerate(votes):
            self.assertEquals(d.candidates.get(name=ModelTestCase.CANDIDATES[i]).votes, v)

    def test_commune(self):
        c = Commune.objects.get(name="Bircza")
        self.assertEquals(c.entitled, 4991)
        self.assertEquals(c.cards, 2679)
        self.assertEquals(c.votes, 2675)
        self.assertEquals(c.valid, 2624)
        self.assertEquals(c.invalid, 51)
        self.assertEquals(c.valid+c.invalid, c.votes)
        self.assertEquals(c.attendance, 53.6)

        votes = [27, 5, 218, 13, 709, 1087, 135, 13, 352, 1, 59, 5]
        for i, v in enumerate(votes):
            self.assertEquals(c.candidates.get(name=ModelTestCase.CANDIDATES[i]).votes, v)

    def test_circuit(self):
        c = Circuit.objects.get(address="Odrzykoń - Dom Kultury")
        self.assertEquals(c.entitled, 2160)
        self.assertEquals(c.cards, 1112)
        self.assertEquals(c.votes, 1112)
        self.assertEquals(c.valid, 1092)
        self.assertEquals(c.invalid, 20)
        self.assertEquals(c.valid+c.invalid, c.votes)
        self.assertEquals(c.attendance, 51.48)

        votes = [13, 1, 84, 14, 209, 469, 79, 19, 181,2, 13, 8]
        for i, v in enumerate(votes):
            self.assertEquals(c.candidates.get(name=ModelTestCase.CANDIDATES[i]).votes, v)

