import html
import inspect

from django import forms
from django.views.generic import TemplateView

from cotton_bs5.views import CottonBS5ComponentMixin


class BaseMixin:
    """
    Base mixin for common functionality across views.
    This can be extended or modified as needed.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        source = inspect.getsource(self.__class__)
        escaped_code = html.escape(source)
        context["view_class"] = escaped_code
        context["view_class_name"] = self.__class__.__name__
        return context


class ExampleForm(forms.Form):
    search = forms.CharField(label="Name", max_length=100)
    email = forms.EmailField(
        label="Email",
        help_text="Enter a valid email address.",
    )

    country = forms.CharField(
        label="Country",
    )
    continent = forms.CharField(
        label="Continent",
    )

    text = forms.CharField(
        label="Text",
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text="Enter some text here.",
    )


class StandardLayout(BaseMixin, CottonBS5ComponentMixin, TemplateView):
    template_name = "example/standard.html"
    sections = {
        "sidebar_primary": "example.sidebar.primary",
        "sidebar_secondary": "example.sidebar.secondary",
    }
    sidebar_primary_config = {
        "breakpoint": "md",
        "class": "border-end",
        "width": "16rem",
        "header": {
            "title": "Primary Sidebar",
            "title_class": "fs-5",
        },
        "footer": {
            "sticky": True,
        },
    }
    sidebar_secondary_config = {
        "breakpoint": "md",
        "class": "border-start",
        "width": "15rem",
        "header": {
            "title": "Secondary Sidebar",
            "title_class": "fs-6",
        },
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ExampleForm()
        context["layout"] = self.layout
        return context


class SecondarySidebarEmpty(StandardLayout):
    """
    View to demonstrate a layout with the secondary sidebar hidden.
    Inherits from StandardLayout and modifies the sidebar_secondary_config.
    """

    sections = {
        "sidebar_secondary": "sections.sidebar.empty",
    }
    sidebar_primary_config = {
        "header": {
            "title": "Updated config Sidebar",
            "title_class": "fs-5",
        },
        "breakpoint": "md",
    }


class PrimarySidebarEmpty(StandardLayout):
    """
    View to demonstrate a layout with the primary sidebar hidden.
    Inherits from StandardLayout and modifies the sidebar_primary_config.
    """

    sections = {
        "sidebar_primary": "sections.sidebar.empty",
    }


class SecondarySidebarRemoved(StandardLayout):
    """ """

    template_name = "example/standard.html"

    layout = {
        "wrapper_class": "container",
    }
    sections = {
        "sidebar_secondary": False,
    }


class PrimarySidebarRemoved(StandardLayout):
    """
    View to demonstrate a layout with the primary sidebar hidden.
    Inherits from StandardLayout and modifies the sidebar_primary_config.
    """

    layout = {
        "wrapper_class": "container",
    }
    sections = {
        "sidebar_primary": False,
    }
