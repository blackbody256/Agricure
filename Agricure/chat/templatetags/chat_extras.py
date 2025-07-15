# In a template tag file if you don't already have basename
from django import template
import os
import re

register = template.Library()

@register.filter
def basename(value):
    return os.path.basename(value)

@register.filter
def regex_search(value, pattern):
    return re.search(pattern, value) is not None