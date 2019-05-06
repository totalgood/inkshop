from django.template import Origin, TemplateDoesNotExist
from django.template.loaders.base import Loader as BaseLoader

from website.models import Template

TEMPLATE_CACHE = {}
TEMPLATE_CACHE_UPDATED_AT = None

TEMPLATE_NORMAL = """
{%% extends "base.html" %%}
{%% block nav %%}%(nav)s{%% endblock %%}
{%% block content %%}%(content)s{%% endblock %%}
{%% block footer %%}%(footer)s{%% endblock %%}
{%% block css %%}%(css)s{%% endblock %%}
{%% block js %%}%(js)s{%% endblock %%}
"""

TEMPLATE_WITH_OVERRIDE = """
{%% extends "base.html" %%}
{%% block body %%}%(body_override)s{%% endblock %%}
{%% block css %%}%(css)s{%% endblock %%}
{%% block js %%}%(js)s{%% endblock %%}
"""


class Loader(BaseLoader):

    def get_template_sources(self, template_name, template_dirs=None):
        yield Origin(
            name=template_name,
            template_name=template_name,
            loader=self,
        )

    def get_contents(self, origin, **kwargs):
        if origin.template_name not in TEMPLATE_CACHE.keys():
            try:
                t = Template.objects.get(name__exact=origin.template_name, **kwargs)
            except:
                raise TemplateDoesNotExist(origin.template_name)

            if t.body_override:
                template_string = TEMPLATE_WITH_OVERRIDE % t.context
            else:
                template_string = TEMPLATE_NORMAL % t.context

            TEMPLATE_CACHE[origin.template_name] = template_string

        return TEMPLATE_CACHE[origin.template_name]
