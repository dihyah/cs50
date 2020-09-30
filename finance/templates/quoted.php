{% extends "layout.html" %}

{% block title %}
    Symbol
{% endblock %}

{% block main %}
    <P style="font-weight:bold;">
        A share of {{ quote["name"] }} {{ (quote["symbol"]) }} costs ${{ quote["price"] }}
    </P>
{% endblock %}


