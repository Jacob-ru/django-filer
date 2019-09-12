# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.http import Http404
from django.views.generic import View
from django.shortcuts import get_object_or_404, redirect, render

from .models import File
from filer.file_edit.base import file_editor_classes
from filer.file_edit.codemirror import CodeMirrorBaseEditor


def canonical(request, uploaded_at, file_id):
    """
    Redirect to the current url of a public file
    """
    filer_file = get_object_or_404(File, pk=file_id, is_public=True)
    if (not filer_file.file or int(uploaded_at) != filer_file.canonical_time):
        raise Http404('No %s matches the given query.' % File._meta.object_name)
    return redirect(filer_file.url)


class FileEditView(View):

    http_method_names = ['get', 'post']

    @staticmethod
    def get_editor_class(file):
        return file_editor_classes.get(file.extension, CodeMirrorBaseEditor)

    def get_template(self, file):
        editor_cls = self.get_editor_class(file)
        return editor_cls.template_name

    @staticmethod
    def get_file(request, uploaded_at, file_id):
        filer_file = get_object_or_404(File, pk=file_id)
        if (not filer_file.file
            or not filer_file.has_edit_permission(request)
            or int(uploaded_at) != filer_file.canonical_time):
            raise Http404(
                'No %s matches the given query.' % File._meta.object_name)
        return filer_file

    def get(self, request, uploaded_at, file_id):
        filer_file = self.get_file(request, uploaded_at, file_id)
        editor_cls = self.get_editor_class(filer_file)
        data = editor_cls().get_context_data()
        with open(filer_file.path, 'r') as f:
            file_data = f.read()
            data['file_data'] = file_data
            return render(self.request,
                          editor_cls.template_name,
                          data)

    def post(self, request, uploaded_at, file_id):
        filer_file = self.get_file(request, uploaded_at, file_id)
        content = self.request.POST['content']
        editor_cls = self.get_editor_class(filer_file)
        data = editor_cls().get_context_data()
        valid, err_mes = editor_cls._validate(content)
        if valid:
            with open(filer_file.path, 'w') as f:
                f.write(content)
                data['file_data'] = content
                return render(self.request,
                              editor_cls.template_name,
                              data)
        else:
            data['file_data'] = content
            data['error_messsage'] = err_mes
            return render(self.request,
                          self.get_template(filer_file),
                          data)
