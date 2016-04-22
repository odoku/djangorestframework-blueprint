{% load blueprint_tag %}
{% autoescape off %}
FORMAT: 1A
HOST: {{ document.base_url }}

# {{ document.title }}

{{ document.description }}

{% for resource in document.resources %}
{% resource resource %}
{% endfor %}
{% endautoescape %}
