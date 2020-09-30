{% extends "layout.html" %}

{% block title %}
    Reset Cash
{% endblock %}

{% block main %}
    <div class="alert alert-danger" role="alert">
        WARNING! All your current data will be lost and cannot be undone! <br>Enter your password and password confirmation if you would like to proceed.<br> Click <a href="/">here</a> if you didn't intend to delete your data.
    </div>
    <form action="/reset" method="post">
        <div class="form-group">
            <input autocomplete="off" autofocus class="form-control" name="password" placeholder="Password" type="password">
        </div>
        <div class="form-group">
            <input class="form-control" name="confirmation" placeholder="Password Confirmation" type="password">
        </div>
        <button class="btn btn-primary" type="submit">Reset</button>
    </form>
{% endblock %}
