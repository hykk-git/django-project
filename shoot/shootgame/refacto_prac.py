from django.db import models
import math
import random

class Invitation:
    when = models.IntegerField()

class Ticket:
    fee = models.IntegerField()

    def getFee(self):
        return self.fee
    
class Bag:
    amount = models.IntegerField()
    invitation = models.CharField()
    ticket =  models.ForeignKey(Ticket, on_delete=models.CASCADE)
    
    def __init__(self, amount=None, invitation=None):
        self.invitation = invitation
        self.amount = amount 

    def setTicket(self, ticket):
        self.ticket = ticket

    def hasInvitation(self):
        return self.invitation != None
    
    def minusAmount(self, amount):
        self.amount = amount

    def hold(self, ticket):
        if self.hasInvitation():
            self.setTicket(ticket)
            return
        else:
            self.minusAmount(self.ticket.getFee())
            self.setTicket(ticket)
            return self.ticket.getFee()

class Audience:
    bag = models.ForeignKey(Bag, on_delete=models.CASCADE)

    def __init__(self, bag):
        self.bag = bag
    
    def getBag(self):
        return self.bag

    def buy(self, ticket):
        fee = self.bag.hold(ticket)
        return fee
        
class TicketOffice:
    amount = models.IntegerField()
    tickets = models.ManyToManyField(Ticket, blank=True) 

    def __init__(self, amount, tickets):
        self.amount = amount
        if tickets:
            self.save()  
            self.tickets.add(*tickets)

    def minusAmount(self, amount):
        self.amount -= amount
    
    def plusAmount(self, amount):
        self.amount += amount
    
    def sellTicketTo(self, audience):
        self.plusAmount(audience)
    
class TicketSeller:
    ticketOffice = models.OneToOneField(TicketOffice, on_delete=models.CASCADE)

    def __init__(self, ticketoffice):
        self.ticketoffice = ticketoffice
    
    def sellTo(self, audience):
        self.ticketOffice.sellTicketTo(audience)

class Theater:
    ticketSeller = models.OneToOneField(TicketSeller, on_delete=models.CASCADE)
    
    def __init__(self, ticketSeller):
        self.ticketSeller = ticketSeller

    def enter(self, audience):
        self.ticketSeller.sellTo(audience)
        