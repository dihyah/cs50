{% extends "layout.html" %}

{% block title %}
    History
{% endblock %}

{% block main %}
    <h1>Past transactions</h1>
    <table class="table">
        <thead style="font-weight:bold">
            <td>Symbol</td>
            <td>Name</td>
            <td>Time</td>
            <td>Shares</td>
            <td>Trade</td>
            <td>Price</td>
            <td>TOTAL</td>
        </thead>
        {% for row in rows: %}
        <tbody>
            <td> {{ row[3] }}</td>
            <td> {{ row[4] }}</td>
            <td> {{ row[1] }}</td>
            <td> {{ row[5] }}</td>
            <td> {{ row[2] }}</td>
            <td> ${{ row[6] }}</td>
            <td> ${{ row[7] }}</td>
        </tbody>
        {% endfor %}
    </table>
{% endblock %}

