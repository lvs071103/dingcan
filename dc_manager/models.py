from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.


class DingCan(models.Model):
    username = models.CharField(max_length=50)
    food = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    type = models.CharField(max_length=10)
    timestamp = models.DateTimeField()
    price = models.FloatField(max_length=5)
    ip_address = models.IPAddressField()

    def __unicode__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('dingcan_edit', kwargs={'pk': self.pk})


class DingCanPost(models.Model):
    title = models.CharField(max_length=150)
    url1 = models.URLField()
    url2 = models.URLField(default='')
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return self.title
