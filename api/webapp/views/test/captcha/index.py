"""
    Captcha testing
"""

from hackfsu_com.views.generic import PageView


class CaptchaTestPage(PageView):
    template_name = 'test/captcha/index.html'
