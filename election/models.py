from django.db import models


class Candidate(models.Model):
    name = models.CharField(max_length=100)


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)
    entitled = models.PositiveIntegerField()
    cards = models.PositiveIntegerField()
    votes = models.PositiveIntegerField()
    valid = models.PositiveIntegerField()
    invalid = models.PositiveIntegerField()


class Voivodeship(models.Model):
    no = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='subareas')
    entitled = models.PositiveIntegerField()
    cards = models.PositiveIntegerField()
    votes = models.PositiveIntegerField()
    valid = models.PositiveIntegerField()
    invalid = models.PositiveIntegerField()


class District(models.Model):
    no = models.PositiveIntegerField(unique=True)
    voivodeship = models.ForeignKey(Voivodeship, on_delete=models.CASCADE, related_name='subareas')
    name = models.CharField(max_length=50)
    entitled = models.PositiveIntegerField()
    cards = models.PositiveIntegerField()
    votes = models.PositiveIntegerField()
    valid = models.PositiveIntegerField()
    invalid = models.PositiveIntegerField()


class Commune(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='subareas')
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=5, unique=True)
    entitled = models.PositiveIntegerField()
    cards = models.PositiveIntegerField()
    votes = models.PositiveIntegerField()
    valid = models.PositiveIntegerField()
    invalid = models.PositiveIntegerField()


class Circuit(models.Model):
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name='subareas')
    address = models.CharField(max_length=300)
    entitled = models.PositiveIntegerField()
    cards = models.PositiveIntegerField()
    votes = models.PositiveIntegerField()
    valid = models.PositiveIntegerField()
    invalid = models.PositiveIntegerField()


class Vote(models.Model):
    number = models.PositiveIntegerField()
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('candidate', 'circuit')