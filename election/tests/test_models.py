from django.test import TestCase
from election.models import Voivodeship, District, Commune, Circuit, Country
from .test_data import TestData

def setUpModule():
    TestData().load()

class ModelTestCase(TestCase):

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
            self.assertEquals(c.candidates.get(name=TestData.CANDIDATES[i]).votes, v)

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
            self.assertEquals(v.candidates.get(name=TestData.CANDIDATES[i]).votes, vv)

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
            self.assertEquals(d.candidates.get(name=TestData.CANDIDATES[i]).votes, v)

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
            self.assertEquals(c.candidates.get(name=TestData.CANDIDATES[i]).votes, v)

    def test_circuit(self):
        c = Circuit.objects.get(address="Odrzykoń - Dom Kultury")
        self.assertEquals(c.entitled, 2160)
        self.assertEquals(c.cards, 1112)
        self.assertEquals(c.votes, 1112)
        self.assertEquals(c.valid, 1092)
        self.assertEquals(c.invalid, 20)
        self.assertEquals(c.valid+c.invalid, c.votes)
        self.assertEquals(c.attendance, 51.48)

        votes = [13, 1, 84, 14, 209, 469, 79, 19, 181, 2, 13, 8]
        for i, v in enumerate(votes):
            self.assertEquals(c.candidates.get(name=TestData.CANDIDATES[i]).votes, v)
