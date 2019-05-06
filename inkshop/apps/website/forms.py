import logging
from django.forms import ModelForm, CharField, TextInput
from website.models import Template, Page, Post
from django.forms import modelformset_factory


class TemplateForm(ModelForm):
    class Meta:
        model = Template
        fields = [
            "name",
            "nav",
            "content",
            "footer",
            "css",
            "js",
            "body_override",
            "everything_override",
        ]


class PageForm(ModelForm):
    class Meta:
        model = Page
        fields = [
            "name",
            "slug",
            "title",
            "description",
            "keywords",
            "template",
            "source_text",
            "rendered_html",
        ]


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            "name",
            "raw_markdown",
            "slug",
            "title",
            "description",
            "template",
            "publish_date",
            "published",
            "private",
            "context",
        ]