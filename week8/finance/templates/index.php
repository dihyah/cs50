{% extends "layout.html" %}

{% block title %}
    Portfolio
{% endblock %}

{% block main %}
    <h1>Portfolio</h1>
    <table class="table">
        <thead style="font-weight:bold">
            <td>Symbol</td>
            <td>Name</td>
            <td>Shares</td>
            <td>Price</td>
            <td>TOTAL</td>
        </thead>
        {% for row in rows: %}
        <tbody>
            <td> {{ row[2] }}</td>
            <td> {{ row[3] }}</td>
            <td> {{ row[4] }}</td>
            <td> ${{ row[5] }}</td>
            <td> ${{ row[6] }}</td>
        </tbody>
        {% endfor %}
        <tr> 
            <td>Equity</td>
        {% for row in range(3): %}
            <td></td>
        {% endfor %}
            <td>${{ balance }}</td>
        </tr>
        <tfoot>
        {% for row in range(4): %}
            <td></td>
        {% endfor %}
            <td>$10000.00</td>
        <tfoot>
    </table>
{% endblock %}

