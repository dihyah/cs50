import os

import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect database with SQLite3
db = sqlite3.connect("finance.db", check_same_thread=False)

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.php")
    else:
        username = request.form.get('username')
        if not username:
            return apology("must provide a username, 403")
        password = request.form.get('password')
        if not password:
            return apology("must provide a password, 403")
        confirmation = request.form.get('confirmation')
        if not confirmation:
            return apology("Must enter password twice for confirmation, 403")
        if confirmation != password:
            return apology("password mismatched, 403")
        hashval = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", [username, hashval])
        db.commit()
        flash("Successfully registered!")
        return redirect('/')


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        # Query database for username
        username = request.form.get('username')
        rows = db.execute("SELECT * FROM users WHERE username LIKE ?", [ username ]).fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], password=request.form.get('password')):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Redirect user to home page
        flash("Welcome, "+username.title()+'.')
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.php")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    rows = db.execute("SELECT * FROM active WHERE id = ? ORDER BY time DESC", [session['user_id']]).fetchall()
    cash = db.execute("SELECT cash FROM users WHERE id = ?", [session['user_id']]).fetchone()
    return render_template("index.php", rows=rows, balance=cash[0])


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.php")
    else:
        symbol = request.form.get("symbol").upper()
        if not symbol:
            return apology("Enter a symbol.", 400)
        quote = lookup(symbol)
        if quote == None:
            return apology("No symbol found.", 400)
        return render_template("quoted.php", quote=quote)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.php")
    symbol = request.form.get("symbol")
    if not symbol:
        return apology("Please enter a stock.")
    quote = lookup(symbol)
    if quote == None:
        return apology("Stock not found.")
    shares = request.form.get("shares")
    if not shares:
        return apology("Enter the shares you want to buy.")
    cash = db.execute("SELECT cash FROM users where id = ?", [session['user_id']]).fetchone()
    balance = cash[0]
    price = quote['price']
    total = round(price)* float(shares) 
    name = quote['name']
    if total > balance:
        return apology("Transaction amount exceeds balance.")
    active = db.execute("SELECT shares FROM active WHERE id = ? AND symbol LIKE ?", [session['user_id'], symbol]).fetchone()
    if active == None:
        db.execute("INSERT INTO active (id, time, symbol, name, shares, price, total) VALUES(?, datetime('now'), ?, ?, ?, ?, ?)", [session['user_id'], symbol.upper(), name, shares, price, total])
    else:
        db.execute("UPDATE active SET shares=shares+:shares WHERE id = ? AND symbol=:symbol", [ shares, session['user_id'], symbol.upper()])
    db.execute("UPDATE users SET cash=cash-:total WHERE id = ?", [ total, session['user_id'] ])
    db.execute("INSERT INTO trades (id, time, trade, symbol, name, shares, price, total) VALUES(?, datetime('now'), 'BUY', ?, ?, ?, ?, ?)", 
            [session['user_id'], symbol.upper(), name, shares, price, total])
    db.commit()
    flash("Stocks bought!")
    return redirect("/")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    rows = db.execute("SELECT DISTINCT(symbol) FROM trades WHERE id = ?", [session['user_id']]).fetchall()
    if request.method == "GET":
        return render_template("sell.php", rows=rows)
    symbol = request.form.get("symbol")
    if not symbol:
        return apology("Please choose the symbol you want to sell.")
    quote = lookup(symbol)
    shares = request.form.get("shares")
    if not shares:
        return apology("Enter the shares you want to sell.")
    owned = db.execute("SELECT SUM(shares) FROM active WHERE id = ? AND symbol LIKE ? GROUP BY symbol", 
            [ session['user_id'], symbol ]).fetchall()
    if len(owned) != 1 or owned[0][0] < 0:
            return apology("Stock shares not found.")
    if int(shares) > owned[0][0]:
            return apology("Number exceeds owned shares.")
    balance = db.execute("SELECT cash FROM users WHERE id = ?", [session['user_id']]).fetchone()
    equity = balance
    price = quote['price']
    total = round( price )* float(shares)
    name = quote['name']
    db.execute("UPDATE users SET cash=cash+:total WHERE id = ?", [total, session['user_id']])
    db.execute("INSERT INTO trades (id, time, trade, symbol, name, shares, price, total) VALUES(?, datetime('now'), 'SELL', ?, ?, ?, ?, ?)", 
            [session['user_id'], rows[0][0].upper(), name, shares, price, total])
    db.execute("UPDATE active SET shares=shares-:shares WHERE id = ? AND symbol=:symbol", [ shares, session['user_id'], symbol.upper()])
    active = db.execute("SELECT shares FROM active WHERE id = ? AND symbol LIKE ?", [session['user_id'], symbol]).fetchone()
    if active[0] <= 0:
        db.execute("DELETE FROM active WHERE id=? AND symbol LIKE ?", [session['user_id'], symbol])
        db.commit()
    db.commit()
    flash("Stock shares sold!")
    return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("SELECT * FROM trades WHERE id = ? ORDER BY time DESC", [session['user_id']])
    return render_template("history.php", rows=rows)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/reset", methods = ["GET", "POST"])
@login_required
def reset():
    """Reset data."""
    if request.method == "GET":
        return render_template("reset.php")
    password = request.form.get('password')
    if not password:
        return apology("must provide a password, 403")
    confirmation = request.form.get('confirmation')
    if not confirmation:
        return apology("Must enter password twice for confirmation, 403")
    if confirmation != password:
        return apology("password mismatched, 403")
    hashval = generate_password_hash(password)
    rows = db.execute("SELECT * FROM users WHERE id = ?", [ session['user_id'] ]).fetchall()

    if len(rows) != 1 or not check_password_hash(rows[0][2], password=request.form.get('password')):
        return apology("invalid password")
    db.execute("UPDATE users SET cash='10000.00' WHERE id = ?", [ session['user_id'] ])
    db.execute("DELETE FROM trades WHERE id = ?", [session['user_id']])
    db.execute("DELETE FROM active WHERE id = ?", [session['user_id']])
    db.commit()
    flash("Data has been reset!")
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
