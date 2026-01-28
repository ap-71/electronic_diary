from django import template

register = template.Library()


@register.filter
def grade_color(value):
    colors = {
        5: "success", 4: "info", 3: "warning", 2: "danger", 1: "secondary"
    }
    return colors.get(value, "secondary")
