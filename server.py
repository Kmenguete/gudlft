import json
from flask import Flask, render_template, request, redirect, flash, url_for


def load_clubs():
    with open('gudlft/clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions():
    with open('gudlft/competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/show_summary', methods=['POST'])
def show_summary():
    club = [club for club in clubs if club['email'] == request.form['email']]
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = [c for c in clubs if c['name'] == club]
    found_competition = [c for c in competitions if c['name'] == competition]
    if found_club and found_competition:
        return render_template('booking.html', club=found_club, competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


def get_competition():
    for competition in competitions:
        return competition


def get_club():
    for club in clubs:
        return club


def update_points_of_club(club, places_required):
    club['points'] = int(club['points']) - places_required
    clubs_file = open("gudlft/clubs.json", "w")
    json_clubs = json.load(clubs_file)
    json.dump(json_clubs, clubs_file)
    clubs_file.close()
    return club


@app.route('/purchase_places', methods=['POST'])
def purchase_places():
    competition = get_competition()
    club = get_club()
    if competition['name'] == request.form['competition'] and club['name'] == request.form['club']:
        places_required = int(request.form['places'])
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
        update_points_of_club(club, places_required)
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competition=competition)
    else:
        flash("Sorry a problem occurs during the request :/")
    return render_template('welcome.html', club=club, competition=competition)


@app.route('/points_board', methods=['GET'])
def get_points_of_clubs():
    return render_template('points_board.html', clubs=clubs)


@app.route('/back_to_welcome_page', methods=['GET'])
def get_back_to_welcome_page():
    club = [club for club in clubs]
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
