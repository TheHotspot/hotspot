from django.db import models
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount

from django.utils import timezone
import hashlib

from django.contrib.auth.models import AbstractUser

epoch = timezone.datetime.fromtimestamp(0) # set time_out to epoch to indicate user is still checked in (use if time_out < time_in checked_in=True)

class User(AbstractUser):
    telephone = models.CharField(max_length=100, default="")

    def checkins(self, hotspot=None, business=None):
        """
        Get all of the user's checkins, optionally filtering by hotspot and business
        """
        filterargs = {}
        filterargs["user__id"] = self.id

        if hotspot:
            filterargs["hotspot__id"] = hotspot__id
        if business:
            filterargs["hotspot__business__id"] = business.id

        checkins = CheckIn.objects.filter(**filterargs)
        return checkins

    def hotspots_visited(self, business=None):
        """
        Get all of the hotspots the user has visited, optionally filtering by business
        """
        filterargs = {}
        filterargs["checkin__user__id"] = self.id

        if business:
            filterargs["checkin__hotspot__business__id"] = business.id

        hotspots = Hotspot.objects.filter(**filterargs)
        return hotspots

    def businesses_visited(self):
        """
        Get all of the businesses whos hotspots the user has checked into
        """
        filterargs = {}
        filterargs["hotspot__checkin__user__id"] = self.id

        businesses = Business.objects.filter(**filterargs)
        return businesses

    def checkin(self, hotspot, time_in=timezone.now(), time_out=epoch):
        """
        checks this user into specified hotspot
        """
        newcheckin = CheckIn(user=self, hotspot=hotspot, time_in=time_in, time_out=time_out)
        newcheckin.save()

    def checkout(self, checkin=None, time_out=timezone.now()):
        """
        Checks user out of a checkin, or if none specified, uses most recent checkin
        """
        if checkin:
            checkin.checkout(time_out)
        else:
            lastcheckin = self.checkins().order_by('time_in')[0]
            lastcheckin.checkout(time_out)

    def checkins_checkedin(self):
        """
        returns checkins that havent been checkedout (should only match current checkins)
        """
        filterargs = {}
        filterargs["time_in__lt"] = timezone.now()
        filterargs["time_out"] = epoch

        checkins = self.checkins().filter(**filterargs)
        return checkins

    def hotspots_checkedin(self):
        filterargs = {}
        filterargs["checkin__time_in__lt"] = timezone.now()
        filterargs["checkin__time_out"] = epoch

        hotspots = self.hotspots_visited().filter(**filterargs)
        return hotspots

    def businesses_checkedin(self):
        filterargs = {}
        filterargs["hotspot__checkin__time_in__lt"] = timezone.now()
        filterargs["hotspot__checkin__time_out"] = epoch

        businesses = self.businesses_visited().filter(**filterargs)
        return businesses


class Business(models.Model):
    """
    Businesses are linked many-to-many with User objects

    """
    name = models.CharField(max_length=100)
    user = models.ManyToManyField(User)
    logo = models.CharField(max_length=100)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

    def hotspots(self):
        """
        return all hotspots belonging to this business
        """
        filterargs = {}
        filterargs["business__id"] = self.id

        hotspots = Hotspot.objects.filter(**filterargs)
        return hotspots

    def checkins(self, hotspot=None, user=None):
        """
        return all checkins to hotspots belonging to this business, optionally filtering by hotspot and user
        """
        filterargs = {}
        filterargs["hotspot__business__id"] = self.id

        if user:
            filterargs["user__id"] = user.id
        if hotspot:
            filterargs["hotspot__id"] = hotspot.id

        checkins = CheckIn.objects.filter(**filterargs)
        return checkins

    def users_visited(self, hotspot=None, user=None):
        """
        return all users who have checked into hotspots belonging to this business
        """
        filterargs = {}
        filterargs["checkin__hotspot__business__id"] = self.id

        if hotspot:
            filterargs["checkin__hotspot__id"] = hotspot.id
        if user:
            filterargs["id"] = user.id

        users = User.objects.filter(**filterargs).distinct()
        return users

    def hotspots_visited(self, user=None):
        """
        return all hotspots that have been checked into, optionally filtering by user
        """
        filterargs = {}
        filterargs["business__id"] = self.id
        filterargs["checkin__hotspot__business__id"] = self.id

        if user:
            filterargs["checkin__user__id"] = user.id

        hotspots = Hotspot.objects.filter(**filterargs).distinct()
        return hotspots

    def checkins_checkedin(self, hotspot=None, user=None):
        """
        returns checkins that havent been checkedout (should only match current checkins), filter by user for >>>if business.checked_in(user):
        """
        filterargs = {}
        filterargs["time_in__lt"] = timezone.now()
        filterargs["time_out"] = epoch

        checkins = self.checkins(hotspot=hotspot, user=user).filter(**filterargs)
        return checkins

    def users_checkedin(self, hotspot=None, user=None):
        """
        returns currently checked in users, optionally filtering by hotspot and user
        """
        filterargs = {}
        filterargs["checkin__time_in__lt"] = timezone.now()
        filterargs["checkin__time_out"] = epoch

        users_checkedin = self.users_visited(hotspot=hotspot, user=user).filter(**filterargs)
        return users_checkedin



class Hotspot(models.Model):
    """
    Hotspots are linked many-to-one with businesses

    """
    name = models.CharField(max_length=100)
    business = models.ForeignKey(Business)
    LAT = models.FloatField()
    LNG = models.FloatField()
    description = models.CharField(max_length=1000)
    logo = models.CharField(max_length=100)

    def checkins(self, user=None):
        """
        return all checkins to this hotspot, optionally filtering by user
        """
        filterargs = {}
        filterargs["hotspot__id"] = self.id

        if user:
            filterargs["user__id"] = user.id

        checkins = CheckIn.objects.filter(**filterargs)
        return checkins

    def checkin(self, user, time_in=timezone.now(), time_out=epoch):
        """
        check into this hotspot with specified user
        """
        User.CheckIn(user=user, hotspot=self, time_in=time_in,time_out=time_out)

    def checkout(self, user, time_out=timezone.now()):
        """
        Checks user out of their most recent check-in at this hotspot
        """
        lastcheckin = CheckIn.objects.filter(user__id=user.id).order_by('time_in')[0]
        lastcheckin.checkout(time_out)

    def users_visited(self):
        """
        return all users who have checked into this hotspot
        """
        return User.objects.filter(checkin__hotspot__id=self.id)

    def users_checkedin(self):
        """
        returns checkins that havent been checked out (should only match currently checked in)
        """
        filterargs = {}
        filterargs["time_in__lt"] = timezone.now()
        filterargs["time_out"] = epoch

        checkins = self.checkins().filter(**filterargs)
        return checkins

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

class CheckIn(models.Model):
    """
    CheckIns are linked many-to-one with hotspots and many-to-one with users

    """
    user = models.ForeignKey(User)
    hotspot = models.ForeignKey(Hotspot)

    time_in = models.DateTimeField('time in', editable=True, default=timezone.now)
    time_out = models.DateTimeField('time out', editable=True, default=epoch)

    def checkout(self, time_out=timezone.now()):
        self.time_out = time_out
        self.save()

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.user.get_full_name()+" @ "+str(self.hotspot)
