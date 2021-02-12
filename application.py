import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


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
    if not request.form.get("name") or not request.form.get("house") or not request.form.get("position"):
        return render_template("error.html", message="Error!Go back and fill the empty fields")
    with open('survey.csv', 'w', newline='') as csvfile:
        fieldnames = ['Name', 'House','Position']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({"Name": request.form.get("name"), "House": request.form.get("house"),"Position": request.form.get("position")})
    return render_template("sheet.html")

students = []
@app.route("/sheet", methods=["POST"])
def get_sheet():
    with open("survey.csv", "r") as file:
        reader = csv.DictReader(file)
        students = list(reader)
    return render_template("represent.html", students=students)

