# Filtre de template perso

from datetime import datetime, timedelta, timezone
from django import template
from django.utils.timesince import timesince
import markdown # Module Markdown

register = template.Library()



# Date personnalisé
@register.filter()
def post_date(published_date):
    now = datetime.now(timezone.utc) # timezone.utc = On précise la zone UTC
    try:
        difference = now - published_date
        if difference <= timedelta(minutes=1): # minutes=1 signifie maintenant - 1 minute
            return "À l'instant"
        return f"Il y a {timesince(published_date).split(', ')[0]}"
    except:
        return published_date

# # Markdown perso
# @register.filter()
# def bold(text):
#     return text.replace('**','<strong>',1).replace('**','</strong>',1)
#     # return text.replace('**', '<strong>').replace('**', '</strong>')


@register.filter()
def mark(text):
    md = markdown.Markdown()
    return md.convert(text)






