from django import template

register = template.Library()

#from common.models import Location

def code_to_name(value):
    """Converts country code to name"""
    exists = Location.objects.filter(country_code=value)

    if exists:
    	country = exists[0]
    	return country.country_name

    return ''