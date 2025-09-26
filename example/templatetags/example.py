from django import template
from django.template.loader import render_to_string
from django.utils.html import escape

register = template.Library()


@register.filter
def strip(value):
    """Strips leading and trailing whitespace from the given string."""
    return value.strip()


@register.simple_tag
def render_html(html_string):
    """
    Usage: {% render_html html_var %}
    Renders the given HTML string verbatim (unescaped).
    """
    return escape(html_string)


@register.simple_tag
def render_document(template_name):
    """Reads in a template file and returns its content as a string."""

    content = render_to_string(template_name)
    return {
        "verbatim": escape(content),
        "rendered": content,
    }


@register.tag(name="block_to_string")
def do_block_to_string(parser, token):
    nodelist = parser.parse(("endblock_to_string",))
    parser.delete_first_token()
    return BlockToStringNode(nodelist)


class BlockToStringNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        html = self.nodelist.render(context)
        lines = [line.strip() for line in html.strip().splitlines() if line.strip()]
        level = 0
        indent = "  "
        result = []

        for line in lines:
            if line.startswith("</"):
                level -= 1
            result.append(f"{indent * level}{line}")
            if (
                line.startswith("<")
                and not line.startswith("</")
                and not line.endswith("/>")
            ):
                level += 1
        return escape("\n".join(result).strip())
