{% load blueprint_tag %}
{% autoescape off %}
+ Attributes (object)

{% for field in attribute.fields %}
{% field field %}
{% endfor %}
{% endautoescape %}
