from django.db import models
from django.contrib.auth.models import User

class Faction(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Profile(models.Model):

    LEADER = 'Leader'
    CONSULTANT = 'Consultant'
    
    roles = (
    (LEADER, "Leader"),
    (CONSULTANT, "Consultant"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    faction = models.ForeignKey(Faction, on_delete=models.SET_NULL, null=True, blank=True)
    factionRole = models.CharField(max_length=30, null=True, blank=True, choices=roles)
    updated = models.DateTimeField(auto_now_add=True, null=False)
    isSaler = models.BooleanField(default=False)

    def __str__(self):
        return self.user.last_name  + " " + self.user.first_name
     
class Channel(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

