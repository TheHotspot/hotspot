from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount

import hashlib

epoch = timezone.make_aware(timezone.datetime.fromtimestamp(0), timezone.utc) # set time_out to epoch to indicate user is still checked in; if time_out == epoch: timezone.is_aware(time_out) == False

def records(func):
    def inner(*args, **kwargs):
        if "records" in kwargs:
            records = kwargs.pop("records")
            if "sort_key" in kwargs:
                sort_key = kwargs.pop("sort_key")
                return func(*args, **kwargs).order_by(sort_key)[:records]
            else:
                return func(*args, **kwargs)[:records]
        else:
            return func(*args, **kwargs)
    return inner

class User(AbstractUser):
    telephone = models.CharField(max_length=20, blank=True, default="")

    # checkin/checkout
    def checkin(self, hotspot, time_in=timezone.now(), time_out=epoch):
        """
        checks this user into specified hotspot
        """
        newcheckin = CheckIn(user=self, hotspot=hotspot, time_in=time_in, time_out=time_out)
        newcheckin.save()
    def checkout(self, checkin=None, business=None, hotspot=None, time_out=timezone.now()):
        """
        Checks user out of a checkin, or if none specified checksout from all
        """
        if checkin:
            lastcheckins = [checkin]
        elif hotspot or business:
            lastcheckins = self.checkins(business=business, hotspot=hotspot).order_by('time_in')
        else:
            lastcheckins = self.checkins().order_by('time_in')

        for check_in in lastcheckins:
            check_in.checkout(time_out)

    # Returns QuerySet of <object>s that have been checked into in the past
    @records
    def checkins(self, business=None, hotspot=None):
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

    @records
    def hotspots_visited(self, business=None, hotspot=None):
        """
        Get all of the hotspots the user has visited, optionally filtering by business
        """
        filterargs = {}
        filterargs["checkin__user__id"] = self.id

        if business:
            filterargs["business__id"] = business.id
        if hotspot:
            filterargs["id"] = hotspot.id

        hotspots = Hotspot.objects.filter(**filterargs).distinct()
        return hotspots

    @records
    def businesses_visited(self, business=None):
        """
        Get all of the businesses whos hotspots the user has checked into
        """
        filterargs = {}
        filterargs["hotspot__checkin__user__id"] = self.id

        if business:
            filterargs["id"] = business.id

        businesses = Business.objects.filter(**filterargs).distinct()
        return businesses

    # Returns QuerySet of <object>s that are currently checked into
    @records
    def checkins_checkedin(self, business=None, hotspot=None):
        """
        returns checkins that havent been checked out
        """
        filterargs = {}
        filterargs["time_in__lt"] = timezone.now()
        filterargs["time_out"] = epoch

        checkins = self.checkins(business=business, hotspot=hotspot).filter(**filterargs)
        return checkins

    @records
    def hotspots_checkedin(self, business=None, hotspot=None):
        filterargs = {}
        filterargs["checkin__time_in__lt"] = timezone.now()
        filterargs["checkin__time_out"] = epoch

        hotspots = self.hotspots_visited(business=business, hotspot=hotspot).filter(**filterargs)
        return hotspots

    @records
    def businesses_checkedin(self, business=None):
        filterargs = {}
        filterargs["hotspot__checkin__time_in__lt"] = timezone.now()
        filterargs["hotspot__checkin__time_out"] = epoch

        businesses = self.businesses_visited(business=business).filter(**filterargs)
        return businesses

    # Gets Bool of state
    def is_checkedin(self, business=None, hotspot=None):
        """
        returns true if user is checked into business
        returns true if user is checked into hotspot
        returns true if user is checked into any hotspot
        returns true if user is checked into any business
        """
        for checkin in self.checkins_checkedin(business=business, hotspot=hotspot):
            if checkin.is_checkedin():
                return True
        return False

    # Formatters
    def checkins_recent(self, business=None, hotspot=None, records=3, sort_key='time_in'):
        return self.checkins(business=business, hotspot=hotspot, records=records)

class Business(models.Model):
    """
    Businesses are linked many-to-many with User objects

    """
    name = models.CharField(max_length=100)
    logo = models.CharField(max_length=100)
    admins = models.ManyToManyField(User)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

    # checkin/checkout
    def checkout(self, user, hotspot=None, time_out=timezone.now()):
        """
        Checks out user from all hotspots or hotspot in this business
        """
        for checkin in checkins_checkedin(user=user, hotspot=hotspot):
            checkin.checkout(time_out)
    def checkout_all(self, hotspot=None, time_out=timezone.now()):
        """
        Checks out all users from all hotspots or hotspot in this business
        """
        for checkin in checkins_checkedin(hotspot=hotspot):
            checkin.checkout(time_out)

    # Return QuerySet of child <Hotspot>s
    def hotspots(self):
        """
        return all hotspots belonging to this business
        """
        filterargs = {}
        filterargs["business__id"] = self.id

        hotspots = Hotspot.objects.filter(**filterargs)
        return hotspots

    # Return QuerySet of <object>s that have been checked into in the past
    @records
    def checkins(self, user=None, hotspot=None, records=0):
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
        if records:
            return checkins.order_by('time_in')[:records]
        return checkins

    @records
    def users_visited(self, user=None, hotspot=None):
        """
        return all users who have checked into hotspots belonging to this business
        """
        filterargs = {}
        filterargs["checkin__hotspot__business__id"] = self.id

        if user:
            filterargs["id"] = user.id
        if hotspot:
            filterargs["checkin__hotspot__id"] = hotspot.id

        users = User.objects.filter(**filterargs).distinct()
        return users

    @records
    def hotspots_visited(self, user=None, hotspot=None):
        """
        return all hotspots that have been checked into, optionally filtering by user
        """
        filterargs = {}
        filterargs["business__id"] = self.id
        filterargs["checkin__hotspot__business__id"] = self.id  # only matches hotspots that have been visited

        if user:
            filterargs["checkin__user__id"] = user.id
        if hotspot:
            filterargs["id"] = hotspot.id

        hotspots = Hotspot.objects.filter(**filterargs).distinct()
        return hotspots

    # Return QuerySet of <object>s that are currently checked into
    @records
    def checkins_checkedin(self, user=None, hotspot=None):
        """
        returns checkins that havent been checkedout (should only match current checkins), filter by user for >>>if business.checked_in(user):
        """
        filterargs = {}
        filterargs["time_in__lt"] = timezone.now()
        filterargs["time_out"] = epoch

        checkins = self.checkins(user=user, hotspot=hotspot).filter(**filterargs)
        return checkins

    @records
    def users_checkedin(self, user=None, hotspot=None):
        """
        returns users who are currently checked in to a hotspot belonging to this business, optionally filtering by hotspot and user
        """
        filterargs = {}
        filterargs["checkin__time_in__lt"] = timezone.now()
        filterargs["checkin__time_out"] = epoch

        users = self.users_visited(user=user, hotspot=hotspot).filter(**filterargs)
        return users

    @records
    def hotspots_checkedin(self, user=None, hotspot=None):
        """
        returns currently checked in users, optionally filtering by hotspot and user
        """
        filterargs = {}
        filterargs["checkin__time_in__lt"] = timezone.now()
        filterargs["checkin__time_out"] = epoch

        hotspots = self.hotspots_visited(user=user, hotspot=hotspot).filter(**filterargs)
        return hotspots

    # Retrun Bool of state
    def is_checkedin(self, user=None, hotspot=None):
        """
        returns true if any user is checked into any hotspot
        returns true if any user is checked into hotspot
        returns true if user is checked into any hotspot
        returns true if user is checked into hotspot
        """
        for checkin in self.checkins_checkedin(user=user, hotspot=hotspot):
            if checkin.is_checkedin():
                return True
        return False

    # Formatters
    def checkins_recent(self, user=None, records=3):
        return self.checkins(user=user, records=records)

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

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

    # setters
    def checkin(self, user, time_in=timezone.now(), time_out=epoch):
        """
        check into this hotspot with specified user
        """
        User.CheckIn(user=user, hotspot=self, time_in=time_in,time_out=time_out)
    def checkout(self, user, time_out=timezone.now()):
        """
        Checks out user from this hotspot
        """
        for checkin in checkins_checkedin(user=user):
            checkin.checkout(time_out)
    def checkout_all(self, time_out=timezone.now()):
        """
        Checks out all users from this hotspot
        """
        for checkin in checkins_checkedin():
            checkin.checkout(time_out)

    # Gets QuerySet of <object>s that have been checked into this hotspot in the past
    @records
    def checkins(self, user=None, records=0):
        """
        return all checkins to this hotspot, optionally filtering by user
        """
        filterargs = {}

        if user:
            filterargs["user__id"] = user.id

        checkins = self.checkin_set.filter(**filterargs)
        if records:
            return checkins.order_by('time_in')[:records]
        return checkins

    @records
    def users_visited(self, user=None):
        """
        return all users who have checked into hotspots belonging to this business
        """
        filterargs = {}
        filterargs["checkin__hotspot__id"] = self.id

        if user:
            filterargs["id"] = user.id

        users = User.objects.filter(**filterargs).distinct()
        return users

    # Gets QuerySet of <object>s that are currently checked into this hotspot
    @records
    def checkins_checkedin(self, user=None):
        """
        returns checkins that havent been checkedout (should only match current checkins), filter by user for >>>if business.checked_in(user):
        """
        filterargs = {}
        filterargs["time_in__lt"] = timezone.now()
        filterargs["time_out"] = epoch

        checkins = self.checkins(user=user).filter(**filterargs)
        return checkins

    @records
    def users_checkedin(self, user=None):
        """
        returns users who are currently checked in to a hotspot belonging to this business, optionally filtering by hotspot and user
        """
        filterargs = {}
        filterargs["checkin__time_in__lt"] = timezone.now()
        filterargs["checkin__time_out"] = epoch

        users = self.users_visited(user=user).filter(**filterargs)
        return users

    # Retrun Bool of state
    def is_checkedin(self, user=None):
        """
        """
        for checkin in self.checkins_checkedin(user=user):
            if checkin.is_checkedin():
                return True
        return False

    # Formatters
    def checkins_recent(self, user=None, records=3, sort_key='time_in'):
        return self.checkins(user=user, records=records)

class CheckIn(models.Model):
    """
    CheckIns are linked many-to-one with :model:`api.hotspot` and many-to-one with :model:`api.User`

    """
    user = models.ForeignKey(User)
    hotspot = models.ForeignKey(Hotspot)
    time_in = models.DateTimeField('time in', editable=True, default=timezone.now)
    time_out = models.DateTimeField('time out', editable=True, default=epoch)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.user.get_full_name()+" @ "+str(self.hotspot)

    # setters
    def checkout(self, time_out=timezone.now()):
        self.time_out = time_out
        self.save()

    def length(self):
        """
        returns length of time user spent checked in (timedelta)
        """
        if self.is_checkedin():
            return timezone.now()-self.time_in
        else:
            return self.time_out-self.time_in

    # status
    def is_checkedin(self):
        """
        returns true if checkin hasnt been checked out
        """
        if self.time_in < timezone.now() and self.time_out == epoch:
            return True
        else:
            return False
