from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group


class HackFsuAdminSite(AdminSite):
    site_header = 'HackFSU Administration'
    site_title = 'HackFSU Django Admin Panel'
    index_title = 'Home'


hackfsu_admin = HackFsuAdminSite(name='hackfsu_admin')
hackfsu_admin.register(User)
hackfsu_admin.register(Group)


