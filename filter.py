import os, django
from django.db.models import Sum, Min, Max, Count
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "www_zad2.settings")
django.setup()

from election.models import Candidate, District, Vote, Circuit, Voivodeship, Country

#Wypisz sumę głosów dla każdego kandydata w całym kraju (imię, nazwisko, liczba głosów)
# cands = Candidate.objects.annotate(sum_votes=Sum("vote__number")).order_by("-sum_votes")
#
# for i in cands:
#     print("{}: {}".format(i.name, i.sum_votes))

#Wypisz sumę głosów dla każdego kandydata w podziale na okręgi (numer okręgu, imię, nazwisko, liczba głosów)
# for d in District.objects.all():
#     cands = Candidate.objects.filter(vote__circuit__commune__district=d).annotate(sum_votes=Sum("vote__number"))
#     for c in cands:
#         print("{}: {} {}".format(d.name, c.name, c.sum_votes))


# ci = Circuit.objects.aggregate(entitled_sum=Sum("entitled"), cards_sum=Sum("cards"), votes_sum=Sum("votes"), valid_sum=Sum("valid"), invalid_sum=Sum("invalid"))
# print(ci)

#ci = Circuit.objects.filter(commune__district__voivodeship__no__exact=1).\
#    aggregate(entitled_sum=Sum("entitled"), cards_sum=Sum("cards"), votes_sum=Sum("votes"), valid_sum=Sum("valid"), invalid_sum=Sum("invalid"))
#print(ci)

# cands = Candidate.objects.filter(vote__circuit__commune__district__no=1).annotate(sum_votes=Sum("vote__number")).order_by("-sum_votes")
#
# for i in cands:
#     print("{}: {}".format(i.name, i.sum_votes))

c = Candidate.objects.filter(vote__circuit__id=15).annotate(votes=Sum("vote__number")).query
print(c)

