from django.views.generic import TemplateView
from django.shortcuts import render
from django.core.exceptions import ValidationError


file_editor_classes = {}


class FileEditMeta(type):

    def __new__(cls, *args, **kwargs):
        new_cls = super(FileEditMeta, cls).__new__(cls, *args, **kwargs)
        if new_cls.extension:
            if isinstance(new_cls.extension, (list, tuple)):
                for ext in new_cls.extension:
                    file_editor_classes[ext] = new_cls
            else:
                file_editor_classes[new_cls.extension] = new_cls
        return new_cls



class BaseFileEditor(TemplateView):
    __metaclass__ = FileEditMeta

    template_name = None
    extension = None

    @classmethod
    def _validate(cls, value):
        try:
            cls.validate(value)
            return True, None
        except ValidationError as e:
            return False, str(e)

    @classmethod
    def validate(cls, value):
        return True
