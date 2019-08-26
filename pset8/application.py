import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
# this flask_session implements server-side session
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

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    tv=0
    cash=db.execute("SELECT cash from users where id=:id",id=session["user_id"])
    info=db.execute("SELECT Symbol,Company,sum(Shares) from 'Portfolio' WHERE UserId=:id GROUP BY Symbol ORDER BY Shares DESC",id=session["user_id"])
    for row in info:
        quote=lookup(row['Symbol'])
        shares=row['sum(Shares)']
        # update adds new columns if required(dict object)
        row.update({'Price':usd(quote["price"])})
        row.update({'TotalPrice':usd(shares*quote["price"])})
        tv=tv+quote["price"]*shares
    # only send shares having >0 count
    finfo=list(filter(lambda row:row['sum(Shares)']!=0,info))
    dollars=cash[0]["cash"]
    # totalvalue
    tv=tv+dollars
    return render_template("index.html",info=finfo,dollars=usd(dollars),tv=usd(tv))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol=request.form.get("symbol")
        try:
            shares=int(request.form.get("shares"))
        except ValueError:
            return apology("Invalid Input")
        quote=lookup(symbol)
        if not symbol or not shares:
            return apology("Missing one or more fields!")
        elif shares<1:
            return apology("No. of shares should be atleast 1")
        elif quote is None:
            return apology("No such symbol")
        elif isinstance(shares,float):
            return apology("No Floating Numbers")
        elif isinstance(shares,int):
            # check if theres enough cash
            rows=db.execute("SELECT cash from users where id=:id",id=session["user_id"])
            if rows[0]["cash"]<(shares*quote["price"]):
                return apology("Not enough cash")
            else:
                db.execute("INSERT INTO Portfolio (UserId,Company,Symbol,Action,Value,Shares,TotalValue) VALUES (:id,:Company,:symbol,'Buy',:Value,:Shares,:TotalValue)",id=session["user_id"],Company=quote["name"],symbol=symbol.upper(),Value=quote["price"],Shares=shares,TotalValue=+shares*quote["price"])
                t=shares*quote["price"]
                db.execute(f"UPDATE users SET cash=cash-{t} where id=:id",id=session["user_id"])
                flash("Bought!!")
                return redirect("/")
        else:
            return apology("Invalid Input")

@app.route("/check", methods=["GET"])
def check():
    username=request.args.get("username").lower()
    check=db.execute("SELECT username from users where username =:username",username=username)
    if check:
        return jsonify(False)
    else:
        return jsonify(True)

@app.route("/history")
@login_required
def history():
    info=db.execute('SELECT Symbol,Company,Action,Shares,TotalValue,TransactedOn  FROM `Portfolio` where UserId=:id',id=session["user_id"])
    return render_template("history.html",info=info)

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
        # :username is used to insert a value as a format to prevent injection attack
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username").lower())
        # rows[0] will contain one user's details
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "GET":
        return render_template("quote.html")
    # pass symbol to lookup function which will return a dict
    quote=lookup(request.form.get("symbol"))
    if quote:
        quote["price"]=usd(quote["price"])
        return render_template("quoted.html",quote=quote)
    else:
        return apology("Invalid Symbol")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username=request.form.get("username").lower()
        password=request.form.get("password")
        confirmation=request.form.get("confirmation")
        if not username or not password or not confirmation:
            return apology("Missing one or more Fields!!")
        elif password!=confirmation:
            return apology("Passwords do not match!")
        else:
            hash=generate_password_hash(password)
            result=db.execute("SELECT * from users where username =:username",username=username)
            if result:
                return apology("Username already taken!")
            else:
                rows=db.execute("INSERT INTO users (username,hash) VALUES(:username,:hash)",username=username,hash=hash)
                # since it is a insert query, it will directly return me with the primary key
                session["user_id"]=rows
                return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    stocks=db.execute("SELECT Symbol,sum(Shares) from 'Portfolio' WHERE UserId=:id GROUP BY Symbol",id=session["user_id"])
    fstocks=list(filter(lambda row:row["sum(Shares)"]!=0,stocks))
    if request.method == "GET":
        return render_template("sell.html",stocks=fstocks)
    else:
        symbol=request.form.get("symbol").upper()
        quote=lookup(symbol)
        # shares user inputted
        shares=int(request.form.get("shares"))
        # returns key value pairs,shares actually user has
        nos=db.execute("SELECT sum(Shares) from 'Portfolio' WHERE UserId=:id AND Symbol=:s GROUP BY Symbol",id=session["user_id"],s=symbol)
        # since returned is a list of dicts
        noofshares=int(nos[0]["sum(Shares)"])
        if shares<1 or shares>noofshares:
            return apology("Invalid Input")
        else:
            db.execute("INSERT INTO Portfolio (UserId,Company,Symbol,Action,Value,Shares,TotalValue) VALUES (:id,:Company,:symbol,'Sell',:Value,:Shares,:TotalValue)",id=session["user_id"],Company=quote["name"],symbol=symbol,Value=quote["price"],Shares=-shares,TotalValue=shares*quote["price"])
            t=shares*quote["price"]
            db.execute(f"UPDATE users SET cash=cash+{t} where id=:id",id=session["user_id"])
            flash("Sold!!")
            return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
