"""
    Handles link keys that are used to give anonymous users elevated privileges. These can be used for different things
    and should be tied to the user it should be used by. These keys should be temporary.
"""

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from hackfsu_com.admin import hackfsu_admin
from django.conf import settings
import string
import random


class LinkKey(models.Model):
    KEY_MAX_LENGTH = 64
    TYPE_PASSWORD_RESET = 0
    TYPE = (
        (TYPE_PASSWORD_RESET, 'Password Reset'),
    )
    LINK_BASE = {
        TYPE_PASSWORD_RESET: settings.URL_BASE + '/user/password/reset/{}/'
    }

    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    type = models.SmallIntegerField(choices=TYPE)
    key = models.CharField(max_length=KEY_MAX_LENGTH)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)

    @staticmethod
    def generate_key() -> str:
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(LinkKey.KEY_MAX_LENGTH))

    def get_link(self):
        return LinkKey.LINK_BASE[self.type].format(self.key)


@admin.register(LinkKey, site=hackfsu_admin)
class LinkKeyAdmin(admin.ModelAdmin):
    list_filter = ('type',)
    list_display = ('id', 'type', 'user_info', 'key', 'created_at', 'expires_at')
    list_editable = ()
    list_display_links = ('id',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    ordering = ('-created_at',)

    @staticmethod
    def user_info(obj):
        return "{} {} - {}".format(obj.user.first_name, obj.user.last_name, obj.user.email)
