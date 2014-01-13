from django.db import models
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
import hashlib

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')

    def __unicode__(self):
        return "{}'s profile".format(self.user.username)

    class Meta:
        db_table = 'user_profile'

    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False

    def profile_image_url(self):
        fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')

        if len(fb_uid):
            return "http://graph.facebook.com/{}/picture?width=40&height=40".format(fb_uid[0].uid)

        return "http://www.gravatar.com/avatar/{}?s=40".format(hashlib.md5(self.user.email).hexdigest())

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class Business(models.Model):
    name = models.CharField(max_length=100)

    user = models.ManyToManyField(User)
    logo = models.CharField(max_length=100)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

class Hotspot(models.Model):
    name = models.CharField(max_length=100)
    business = models.ForeignKey(Business)

    user = business.name
    LAT = models.FloatField()
    LNG = models.FloatField()
    description = models.CharField(max_length=1000)
    logo = models.CharField(max_length=100)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

class CheckIn(models.Model):
    user = models.ForeignKey(User)
    hotspot = models.ForeignKey(Hotspot)

    time_in = models.DateTimeField('time in')
    time_out = models.DateTimeField('time out')


    def __unicode__(self):  # Python 3: def __str__(self):
        return self.user.get_full_name()+" @ "+str(self.hotspot)
