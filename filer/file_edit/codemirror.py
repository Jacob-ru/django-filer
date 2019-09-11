import json
from django.core.exceptions import ValidationError
from lxml import objectify

from filer.file_edit.base import BaseFileEditor


class CodeMirrorBaseEditor(BaseFileEditor):
    template_name = 'admin/filer/file_edit.html'
    codemirror_extension = ''
    extension = 'txt'


class XMLEditor(CodeMirrorBaseEditor):
    codemirror_extension = 'xml'
    extension = 'xml'

    @classmethod
    def validate(cls, value):
        try:
            objectify.fromstring(value.encode())
        except Exception as e:
            raise ValidationError(str(e))


class JSONEditor(CodeMirrorBaseEditor):
    codemirror_extension = 'json'
    extension = 'json'

    @classmethod
    def validate(cls, value):
        try:
            json.loads(value)
        except Exception as e:
            raise ValueError(str(e))
