{% load blueprint_tag %}
{% autoescape off %}
### {{ method }} [{{ method }} {{ action|path }}]

{{ document }}

{% parameters parameters %}

{% for request in requests %}
{% request request %}
{% endfor %}

{% for response in responses %}
{% response response %}
{% endfor %}
{% endautoescape %}
