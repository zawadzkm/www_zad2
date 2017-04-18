from django.test import TestCase
from election.forms import VoteForm


class FormTestCase(TestCase):

    def test_vote(self):
        form_data = {'number': 50}
        form = VoteForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_no_vote(self):
        form_data = {'number': -1}
        form = VoteForm(data=form_data)
        self.assertFalse(form.is_valid())
