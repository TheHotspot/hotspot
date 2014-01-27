"""
Hotspot API v1.0  
Nick Sweeting 2014
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount

import hashlib
import random

from functools import wraps

epoch = timezone.make_aware(timezone.datetime.fromtimestamp(0), timezone.utc) # set time_out to epoch to indicate user is still checked in; if time_out == epoch: timezone.is_aware(time_out) == False

#@sortable allows you to limit queries to the first records=# when sorted with sort_key=''
def sortable(func):
    """
    Takes any QuerySet-returning-function, orders output by sort_key='', truncates to first records=#
    e.g. User.objects.get(id=1).checkins(records=3, sort_key='time_in')
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "records" in kwargs:
            records = kwargs.pop("records")
            if "sort_key" in kwargs:
                sort_key = kwargs.pop("sort_key")
            else:
                sort_key = False
        else:
            records = False
        if records:
            if sort_key:
                return func(*args, **kwargs).order_by(sort_key)[:records]
            else:
                return func(*args, **kwargs)[:records]
        else:
            return func(*args, **kwargs)
    return wrapper

class User(AbstractUser):
    """
    User(id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, telephone)

    :class:`.User` extends :class:`.AbstractUser` .
    """

    telephone = models.CharField(max_length=20, blank=True, default="")
    """ Field: Telephone Number. Defaults to None."""

    def checkin(self, hotspot, time_in=timezone.now(), time_out=epoch):
        """
        checkin(self, hotspot, time_in=timezone.now(), time_out=epoch)
        Checks the user into :class:`.Hotspot` at time_in= :class:`timezone.now()`, setting time_out to the unix epoch (indicating user is still checked in)
        """
        newcheckin = CheckIn(user=self, hotspot=hotspot, time_in=time_in, time_out=time_out)
        newcheckin.save()

    def checkout(self, checkin=None, business=None, hotspot=None, time_out=timezone.now()):
        """
        checkout(self, checkin=None, business=None, hotspot=None, time_out=timezone.now())
        Checks user out of checkin= :class:`.CheckIn` at time_out= :class:`timezone.now()`
            if checkin=None, checks out from all checkins where business= :class:`.Business` and/or hotspot= :class:`.Hotspot`
        """
        if checkin:
            lastcheckins = [checkin]
        elif hotspot or business:
            lastcheckins = self.checkins(business=business, hotspot=hotspot).order_by('time_in')
        else:
            lastcheckins = self.checkins().order_by('time_in')

        for check_in in lastcheckins:
            check_in.checkout(time_out)

    """ Returns QuerySet of <object>s that have been checked into in the past """
    @sortable
    def checkins(self, business=None, hotspot=None):
        """
        checkins(self, business=None, hotspot=None, records=0, sort_key="")
        Returns QuerySet of :class:`.CheckIn` objects where checkin__hotspot= :class:`.Hotspot` and hotspot__business= :class:`.Business`
        """
        filterargs = {}
        filterargs["user__id"] = self.id

        if hotspot:
            filterargs["hotspot__id"] = hotspot__id
        if business:
            filterargs["hotspot__business__id"] = business.id

        checkins = CheckIn.objects.filter(**filterargs)
        return checkins

    @sortable
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

    @sortable
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
    @sortable
    def checkins_checkedin(self, business=None, hotspot=None):
        """
        returns checkins that havent been checked out
        """
        filterargs = {}
        filterargs["time_in__lt"] = timezone.now()
        filterargs["time_out"] = epoch

        checkins = self.checkins(business=business, hotspot=hotspot).filter(**filterargs)
        return checkins

    @sortable
    def hotspots_checkedin(self, business=None, hotspot=None):
        filterargs = {}
        filterargs["checkin__time_in__lt"] = timezone.now()
        filterargs["checkin__time_out"] = epoch

        hotspots = self.hotspots_visited(business=business, hotspot=hotspot).filter(**filterargs)
        return hotspots

    @sortable
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
    admins = models.ManyToManyField(User)

    nickname = models.CharField(max_length=40, blank=True, default="")
    logo = models.CharField(max_length=200, blank=True, default="")
    website = models.CharField(max_length=200, blank=True, default="")

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
    @sortable
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

    @sortable
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

    @sortable
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
    @sortable
    def checkins_checkedin(self, user=None, hotspot=None):
        """
        returns checkins that havent been checkedout (should only match current checkins), filter by user for >>>if business.checked_in(user):
        """
        filterargs = {}
        filterargs["time_in__lt"] = timezone.now()
        filterargs["time_out"] = epoch

        checkins = self.checkins(user=user, hotspot=hotspot).filter(**filterargs)
        return checkins

    @sortable
    def users_checkedin(self, user=None, hotspot=None):
        """
        returns users who are currently checked in to a hotspot belonging to this business, optionally filtering by hotspot and user
        """
        filterargs = {}
        filterargs["checkin__time_in__lt"] = timezone.now()
        filterargs["checkin__time_out"] = epoch

        users = self.users_visited(user=user, hotspot=hotspot).filter(**filterargs)
        return users

    @sortable
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
    business = models.ForeignKey(Business, blank=True)
    LAT = models.FloatField(blank=True)
    LNG = models.FloatField(blank=True)
    address = models.CharField(max_length=500, blank=True, default="")

    nickname = models.CharField(max_length=40, blank=True, default="")
    capacity = models.IntegerField(blank=True, default=0)

    description = models.CharField(max_length=2000, blank=True, default="")
    website = models.CharField(max_length=200, blank=True, default="")
    logo = models.CharField(max_length=200, blank=True, default="")
    telephone = models.CharField(max_length=25, blank=True, default="")

    # songkick venue id
    #songkick_venue_id = models.IntegerField(blank=True, default=0)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

    def score(self):
        """
        Returns the number of people checked in (number to display on maps)
        """
        
        # Legit Version
        #return checkins_checkedin().count()
        # "augmented" results
        return self.checkins_checkedin().count()*2+random.randint(5,20)


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
    @sortable
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

    @sortable
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

    def admins(self):
        """
        Returns the users in control of this hotspot
        """
        return self.business.admins.all()

    # Gets QuerySet of <object>s that are currently checked into this hotspot
    @sortable
    def checkins_checkedin(self, user=None):
        """
        returns checkins that havent been checkedout (should only match current checkins), filter by user for >>>if business.checked_in(user):
        """
        filterargs = {}
        filterargs["time_in__lt"] = timezone.now()
        filterargs["time_out"] = epoch

        checkins = self.checkins(user=user).filter(**filterargs)
        return checkins

    @sortable
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

    # Scanners
    @staticmethod
    @sortable
    def search_by_radius(lat, lng, radius=10):
        """
        Find all hotspots within a given radius (limited to 50km)
        """

        find_by_radius_sql = \
        '''SELECT api_hotspot.id, api_hotspot.LAT, api_hotspot.LNG, 
        ( 3959 * acos(cos(radians( %(ILAT)s ) ) * cos( radians( LAT )) * cos(radians( LNG ) - radians( %(ILNG)s )) + sin(radians( %(ILAT)s )) * sin(radians( LAT )))) AS distance FROM api_hotspot
        HAVING distance < %(IRAD)s
        ORDER BY distance'''


        ids = [x.id for x in Hotspot.objects.raw(find_by_radius_sql, {"ILAT":lat,"ILNG":lng,"IRAD":radius})]
        return Hotspot.objects.filter(id__in=ids)

class CheckIn(models.Model):
    """
    CheckIns are linked many-to-one with model:`Hotspot` and many-to-one with model:`User`

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

    
    # Returns QuerySet of <object>s that are currently checked into
    @staticmethod
    @sortable
    def checkins_checkedin(business=None, hotspot=None):
        """
        returns checkins that havent been checked out
        """
        filterargs = {}
        filterargs["time_in__lt"] = timezone.now()
        filterargs["time_out"] = epoch

        checkins = CheckIn.objects.filter(**filterargs)
        return checkins


from django.db import transaction
from django.db.models import get_models, Model
from django.contrib.contenttypes.generic import GenericForeignKey

@transaction.commit_on_success
def merge_objects(primary_object, alias_objects=[], keep_old=False):
    """
    Use this function to merge model objects (i.e. Users, Organizations, Polls,
    etc.) and migrate all of the related fields from the alias objects to the
    primary object.
    
    Usage:
    from django.contrib.auth.models import User
    primary_user = User.objects.get(email='good_email@example.com')
    duplicate_user = User.objects.get(email='good_email+duplicate@example.com')
    merge_model_objects(primary_user, duplicate_user)
    """
    if not isinstance(alias_objects, list):
        alias_objects = [alias_objects]
    
    # check that all aliases are the same class as primary one and that
    # they are subclass of model
    primary_class = primary_object.__class__
    
    if not issubclass(primary_class, Model):
        raise TypeError('Only django.db.models.Model subclasses can be merged')
    
    for alias_object in alias_objects:
        if not isinstance(alias_object, primary_class):
            raise TypeError('Only models of same class can be merged')
    
    # Get a list of all GenericForeignKeys in all models
    # TODO: this is a bit of a hack, since the generics framework should provide a similar
    # method to the ForeignKey field for accessing the generic related fields.
    generic_fields = []
    for model in get_models():
        for field_name, field in filter(lambda x: isinstance(x[1], GenericForeignKey), model.__dict__.iteritems()):
            generic_fields.append(field)
            
    local_fields = set([field.attname for field in primary_object._meta.local_fields])
    
    # Loop through all alias objects and migrate their data to the primary object.
    for alias_object in alias_objects:
        # Migrate all foreign key references from alias object to primary object.
        for related_object in alias_object._meta.get_all_related_objects():
            # The variable name on the alias_object model.
            alias_varname = related_object.get_accessor_name()
            # The variable name on the related model.
            obj_varname = related_object.field.name
            related_objects = getattr(alias_object, alias_varname)
            for obj in related_objects.all():
                setattr(obj, obj_varname, primary_object)
                obj.save()

        # Migrate all many to many references from alias object to primary object.
        for related_many_object in alias_object._meta.get_all_related_many_to_many_objects():
            alias_varname = related_many_object.get_accessor_name()
            obj_varname = related_many_object.field.name
            
            if alias_varname is not None:
                # standard case
                related_many_objects = getattr(alias_object, alias_varname).all()
            else:
                # special case, symmetrical relation, no reverse accessor
                related_many_objects = getattr(alias_object, obj_varname).all()
            for obj in related_many_objects.all():
                getattr(obj, obj_varname).remove(alias_object)
                getattr(obj, obj_varname).add(primary_object)

        # Migrate all generic foreign key references from alias object to primary object.
        for field in generic_fields:
            filter_kwargs = {}
            filter_kwargs[field.fk_field] = alias_object._get_pk_val()
            filter_kwargs[field.ct_field] = field.get_content_type(alias_object)
            for generic_related_object in field.model.objects.filter(**filter_kwargs):
                setattr(generic_related_object, field.name, primary_object)
                generic_related_object.save()
                
        # Try to fill all missing values in primary object by values of duplicates
        filled_up = set()
        for field_name in local_fields:
            val = getattr(alias_object, field_name)+getattr(primary_object, field_name)     # !!! this breaks any int field like LAT and LNG, because it adds them together
            if val not in [None, '']:
                # TODO: MAKE THIS APPEND NEW FIELD, NOT OVERWRITE IT
                setattr(primary_object, field_name, val)
                filled_up.add(field_name)
        local_fields -= filled_up
            
        if not keep_old:
            alias_object.delete()
    primary_object.save()
    return primary_object
