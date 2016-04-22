{% load blueprint_tag %}
{% autoescape off %}
+ {{ name }} ({{ field|type }}, {% if required %}required{% else %}optional{% endif %}){% if label %} - {{ label }}{% endif %}

    {{ help_text }}

    {% if default %}
    + default: `{{ default }}`
    {% endif %}

{% if choices %}
    + Members
        {% for val, label in choices.items %}
        + `{{ val }}` {% if label %}- {{ label }}{% endif %}
        {% endfor %}
{% endif %}
{% endautoescape %}
