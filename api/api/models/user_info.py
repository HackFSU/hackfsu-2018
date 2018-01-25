from django.db import models
from django.contrib.auth.models import User
from api.models import Hackathon
from django.contrib import admin
from hackfsu_com.admin import hackfsu_admin


class UserInfo(models.Model):
    SHIRT_SIZE_CHOICES = (
        ('m-s',     'Men\'s Small'),
        ('m-m',     'Men\'s Medium'),
        ('m-l',     'Men\'s Large'),
        ('m-xl',    'Men\'s XL'),
        ('m-2xl',   'Men\'s XXL'),
        ('m-3xl',   'Men\'s XXXL'),
        ('w-s',     'Women\'s Small'),
        ('w-m',     'Women\'s Medium'),
        ('w-l',     'Women\'s Large'),
        ('w-xl',    'Women\'s XL')
    )
    created = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    shirt_size = models.CharField(max_length=10, choices=SHIRT_SIZE_CHOICES)
    diet = models.CharField(max_length=500, default='', blank=True)
    github = models.CharField(max_length=100, default='', blank=True)
    linkedin = models.CharField(max_length=100, default='', blank=True)
    last_hackathon = models.ForeignKey(to=Hackathon, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    comments = models.CharField(max_length=1000, default='', blank=True)
    hexcode = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return '[UserInfo {} {}]'.format(self.user.first_name, self.user.last_name)


@admin.register(UserInfo, site=hackfsu_admin)
class UserInfoAdmin(admin.ModelAdmin):
    list_filter = ('shirt_size',)
    list_display = ('id', 'user_info', 'phone_number', 'shirt_size', 'diet', 'github', 'linkedin', 'created')
    list_editable = ()
    list_display_links = ('id',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'diet', 'github', 'linkedin')
    ordering = ('-created',)

    @staticmethod
    def user_info(obj):
        return "{} {} - {}".format(obj.user.first_name, obj.user.last_name, obj.user.email)
