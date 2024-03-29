# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os

from django.utils.timezone import now
from django.conf import settings
from django.utils.text import get_valid_filename as django_get_valid_filename
from .files import get_valid_filename


try:
    from django.utils.encoding import force_text
except ImportError:
    # Django < 1.5
    from django.utils.encoding import force_unicode as force_text


def by_date(instance, filename):
    datepart = force_text(now().strftime("%Y/%m/%d"))
    return os.path.join(datepart, get_valid_filename(filename))


def randomized(instance, filename):
    import uuid
    uuid_str = str(uuid.uuid4())
    return os.path.join(uuid_str[0:2], uuid_str[2:4], uuid_str,
            get_valid_filename(filename))

def by_folder(instance, filename):
    valid_name = django_get_valid_filename(filename)
    if instance.folder_id:
        in_media_path = os.path.join(
            instance.folder.pretty_logical_path[1:].replace('/', os.sep),
            valid_name
        )
        return in_media_path
    return valid_name

class prefixed_factory(object):
    def __init__(self, upload_to, prefix):
        self.upload_to = upload_to
        self.prefix = prefix

    def __call__(self, instance, filename):
        if callable(self.upload_to):
            upload_to_str = self.upload_to(instance, filename)
        else:
            upload_to_str = self.upload_to
        if not self.prefix:
            return upload_to_str
        return os.path.join(self.prefix, upload_to_str)
