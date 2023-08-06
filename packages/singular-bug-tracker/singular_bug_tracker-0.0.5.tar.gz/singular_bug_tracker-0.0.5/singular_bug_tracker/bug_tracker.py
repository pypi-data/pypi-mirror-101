import sys
from traceback import format_tb

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string


def handler500(request, *args, **argv):
    type_, value, traceback = sys.exc_info()
    _request = traceback.tb_next.tb_frame.f_locals['request']
    traceback = format_tb(traceback)
    send_mail(value.args[0], '', settings.DEFAULT_FROM_EMAIL,
              [settings.BUGTRACKER_EMAIL],
              html_message=render_to_string('traceback.html', {
                  'url': _request.path,
                  'post': _request.POST,
                  'get': _request.GET,
                  'traceback':traceback
              }))
    return render(request,'500.html', status=500)
