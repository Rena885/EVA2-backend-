import os

content = open('ticketRB/settings.py', 'r', encoding='utf-8').read()
content = content.replace("'drf_spectacular',", "'drf_spectacular',\n    'django_filters',")
content = content.replace("'DEFAULT_PERMISSION_CLASSES': [", "'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],\n    'DEFAULT_PERMISSION_CLASSES': [")
open('ticketRB/settings.py', 'w', encoding='utf-8').write(content)
