from django.test import TestCase, Client
from django.urls import reverse
from election.models import Voivodeship, District, Commune, Circuit, Candidate
from .test_data import TestData
from django.contrib.auth.models import User

def setUpModule():
    TestData().load()

class ViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="test1", password="test1", email="test1@test.tst")

    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_voivodeship(self):
        v = Voivodeship.objects.get(name="Mazowieckie")
        response = self.client.get(reverse('voivodeship', args=[v.no]))
        self.assertEqual(response.status_code, 200)

    def test_no_voivodeship(self):
        response = self.client.get(reverse('voivodeship', args=[17]))
        self.assertEqual(response.status_code, 404)

    def test_district(self):
        d = District.objects.get(name='Krosno')
        response = self.client.get(reverse('district', args=[d.voivodeship.no, d.no]))
        self.assertEqual(response.status_code, 200)

    def test_no_district(self):
        v = Voivodeship.objects.get(name='Podkarpackie')
        response = self.client.get(reverse('district', args=[v.no, 70]))
        self.assertEqual(response.status_code, 404)

    def test_commune(self):
        c = Commune.objects.get(name="Bircza")
        response = self.client.get(reverse('commune', args=[c.district.voivodeship.no, c.district.no, c.code]))
        self.assertEqual(response.status_code, 200)

    def test_no_commune(self):
        c = Commune.objects.get(name="Bircza")
        response = self.client.get(reverse('commune', args=[c.district.voivodeship.no, c.district.no, 70000]))
        self.assertEqual(response.status_code, 404)

    def test_search(self):
        response = self.client.get(reverse('search'), {'q': 'maz'})
        self.assertEquals(len(response.context['result']), 2)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        self.client.logout()

        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        circ = Circuit.objects.filter(address="Gminny Ośrodek Kultury, Sportu i Turystyki w Birczy")[0]
        cand = Candidate.objects.get(name=TestData.CANDIDATES[0])

        response = self.client.get(reverse('update', args=[circ.commune.district.voivodeship.no, circ.commune.district.no, circ.commune.code, circ.id, cand.id]))
        self.assertEqual(response.status_code, 302)

        self.assertTrue(self.client.login(username='test1', password='test1'))

        response = self.client.get(reverse('update', args=[circ.commune.district.voivodeship.no, circ.commune.district.no, circ.commune.code, circ.id, cand.id]))
        self.assertEqual(response.status_code, 200)


    def test_logout(self):
        self.client.logout()
        self.assertTrue(self.client.login(username='test1', password='test1'))
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)