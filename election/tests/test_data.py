import pandas, pkg_resources
from election.models import Voivodeship, District, Commune, Circuit, Candidate, Vote, Country

class TestData():

    CANDIDATES = ["Dariusz Maciej GRABOWSKI", "Piotr IKONOWICZ", "Jarosław KALINOWSKI", "Janusz KORWIN-MIKKE",
                  "Marian KRZAKLEWSKI", "Aleksander KWAŚNIEWSKI", "Andrzej LEPPER", "Jan ŁOPUSZAŃSKI",
                  "Andrzej Marian OLECHOWSKI", "Bogdan PAWŁOWSKI", "Lech WAŁĘSA", "Tadeusz Adam WILECKI"]


    def load(self):
        df = pandas.read_csv(pkg_resources.resource_filename('data', 'test_data.csv'), sep=";")

        cands = {}

        for n in TestData.CANDIDATES:
            cands[n] = Candidate.objects.get_or_create(name=n)

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
                     ) for n in TestData.CANDIDATES
            ]
            Vote.objects.bulk_create(objs)
