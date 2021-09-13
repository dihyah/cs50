{% extends "layout.html" %}

{% block title %}
    Buy
{% endblock %}

{% block main %}
    <form action="/buy" method="post">
        <div class="form-group">
            <input style="text-transform:uppercase" autocomplete="off" autofocus class="form-control" name="symbol" placeholder="RHT" type="text">
        </div>
        <div class="form-group">
            <input class="form-control" name="shares" placeholder="Shares" type="number" min="1">
        </div>
        <button class="btn btn-primary" type="submit">Buy</button>
    </form>
{% endblock %}
