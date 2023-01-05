import json
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    make_response,
)
from datetime import datetime


def load_clubs():
    with open("clubs.json") as c:
        list_of_clubs = json.load(c)["clubs"]
        return list_of_clubs


def load_competitions():
    with open("competitions.json") as comps:
        list_of_competitions = json.load(comps)["competitions"]
        return list_of_competitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = load_competitions()
clubs = load_clubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/show_summary", methods=["POST"])
def show_summary():
    try:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
        return render_template("welcome.html", club=club, competitions=competitions)
    except IndexError:
        response = make_response(
            "<p>Sorry, the email you provided was not found in our system.<p>"
        )
        response.status_code = 400
        return response


@app.route("/book/<competition>/<club>/<number_of_places>", methods=["GET"])
def book(competition, club, number_of_places):
    try:
        found_club = [c for c in clubs if c["name"] == club][0]
        found_competition = [c for c in competitions if c["name"] == competition][0]
        found_places = [c for c in competitions if c["numberOfPlaces"] == number_of_places][0]
        if found_club and found_competition and found_places:
            if (
                datetime.strptime(found_competition["date"], "%Y-%m-%d %H:%M:%S")
                < datetime.now()
            ):
                response = make_response(
                    "<p>You cannot book places in a past competition<p>"
                )
                response.status_code = 400
                return response
            else:
                return render_template(
                    "booking.html", club=club, competition=competition, number_of_places=number_of_places
                )
        else:
            flash("Something went wrong-please try again")
            return render_template("welcome.html", club=club, competitions=competitions)
    except IndexError:
        response = make_response(
            "<p>You did not provide the necessary credentials to access this page.<p>"
        )
        response.status_code = 401
        return response


@app.route("/purchase_places", methods=["POST"])
def purchase_places():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][0]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    places_required = int(request.form["places"])
    if places_required > 12:
        response = make_response(
            "<p>You cannot book more than 12 places per competition.<p>"
        )
        response.status_code = 400
        return response
    elif places_required > int(club["points"]):
        response = make_response("<p>You cannot use more than your allowed points.<p>")
        response.status_code = 400
        return response
    else:
        competition["numberOfPlaces"] = (
            int(competition["numberOfPlaces"]) - places_required
        )
        club["points"] = int(club["points"]) - places_required
        flash("Great-booking complete!")
        return redirect(url_for("get_back_to_welcome_page", club_name=club["name"]))


@app.route("/points_board/<club_name>", methods=["GET"])
def get_points_of_clubs(club_name):
    try:
        current_club = [c for c in clubs if c["name"] == club_name][0]
        return render_template("points_board.html", clubs=clubs, current_club=current_club)
    except IndexError:
        response = make_response(
            "<p>You did not provide the necessary credentials to access this page.<p>"
        )
        response.status_code = 401
        return response


@app.route("/back_to_welcome_page/<club_name>", methods=["GET"])
def get_back_to_welcome_page(club_name):
    try:
        club = [c for c in clubs if c["name"] == club_name][0]
        return render_template("welcome.html", club=club, competitions=competitions)
    except IndexError:
        response = make_response(
            "<p>You did not provide the necessary credentials to access this page.<p>"
        )
        response.status_code = 401
        return response


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
