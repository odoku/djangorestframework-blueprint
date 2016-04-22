{% load blueprint_tag %}
{% autoescape off %}
+ Parameters

{% for field in parameters.fields %}
{% field field %}
{% endfor %}
{% endautoescape %}
