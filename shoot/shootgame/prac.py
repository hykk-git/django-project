from django.db import models
import math
import random

class Movie:
    Screening = models.ForeignKey(Screening, on_delete=models.CASCADE)
    def __init__(self):
        pass

class Reservation:
    customer = 
class Screening:
    sequence = models.IntegerField()
    whenScreend = models.DateTimeField()

    movie = Movie.objects.create()
    def __init__(self, movie, sequence, whenScreened):
        self.movie = movie
        self.sequence = sequence
        self.whenScreend = whenScreened

    def getStartTime(self):
        return self.whenScreend
    
    def isSequence(self, sequence):
        self.sequence = sequence

    def getMovieFee(self):
        return self.movie.getFee()
    
    def reserve(self, customer, autienceCount):
        return Reservation.object.create(customer, 
                                         calculateFee(audienceCount),
                                         audienceCount)