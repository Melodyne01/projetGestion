from django.db import models
from django.core.validators import MinValueValidator
from users.models import Faction, Profile, Channel, Customer
from django import forms


class Request(models.Model):
    
    PENDING = 'Pending'
    PROPOSED = 'Proposed'
    RESOURCE_NEEDED = 'Resource needed'
    INTERVIEW = 'Interview'
    WON = 'Won'
    NO_GOAL = 'No goal'
    LOST = 'Lost'

    ONE = 1
    TWO = 2
    TREE = 3
    FOUR = 4
    
    STATUS = (
    (PENDING, "Pending"),
    (PROPOSED, "Proposed"),
    (RESOURCE_NEEDED, "Resource needed"),
    (INTERVIEW, "Interview"),
    (WON, "Won"),
    (NO_GOAL, "No goal"),
    (LOST, "Lost"),
    )

    Priority = (
        (ONE, 1),
        (TWO, 2),
        (TREE, 3),
        (FOUR, 4),
    )

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    channel = models.ForeignKey(Channel, on_delete=models.SET_NULL, null=True, blank=True)
    reference = models.CharField(max_length=30, null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    level = models.CharField(max_length=10, null=True, blank=True)
    priority = models.IntegerField(choices=Priority, null=True, blank=True)
    durationMonths = models.IntegerField(validators=[MinValueValidator(1)],  null=True, blank=True)
    sales = models.CharField(max_length=20, null=True, blank=True)
    faction = models.ForeignKey(Faction, on_delete=models.SET_NULL, null=True, blank=True)
    consultant = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=15, null=True, blank=True, choices=STATUS)
    internalComments = models.TextField(null=True, blank=True)
    clientComment = models.TextField(null=True, blank=True)
    started = models.DateField(null=True, blank=True)
    dateProposed = models.DateField(null=True, blank=True)
    ended = models.DateField(null=True, blank=True)
    uptaded = models.DateField(null=True, blank=True)
    created = models.DateField(auto_now_add=True, null=False)
    #Field in form
    pdf = models.FileField(upload_to='pdf', null=True, blank=True)
    class Meta:
        ordering = ['ended']

    def __unicode__(self):
        return self.reference

