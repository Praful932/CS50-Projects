#import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True

records=[]

@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    # request.form for post arguments request.args for get arguments
    name=request.form.get("pname")
    select=request.form.get("favselect")
    mb=request.form.get("mb")
    if not name or not select or not mb:
        return render_template("error.html")
    else:
        # newline='' avoids insertion of new lines betn rows
        file=open("survey.csv","a",newline='')
        writer=csv.writer(file)
        # pass in a tuple to writerow
        writer.writerow((name,select,mb))
        file.close()
        return redirect("/sheet")


@app.route("/sheet", methods=["GET"])
def get_sheet():
    file=open("survey.csv","r")
    reader=csv.reader(file)
    for row in reader:
        # to avoid duplicates and send a unique set of records each time
        if row not in records:
            records.append(row)   
    # pass in extra parameter records to use in registered.html
    return render_template("registered.html",records=records)

