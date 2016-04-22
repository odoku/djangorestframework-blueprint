{% load blueprint_tag %}
{% autoescape off %}
## {{ resource|path }}

{{ resource.document }}

{% for action in resource.actions %}
{% action action %}
{% endfor %}
{% endautoescape %}
