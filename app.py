from flask import Flask, render_template, request, redirect, url_for, session
import requests
import re
import hashlib
import locale  # Import the locale module

app = Flask(__name__)
app.secret_key = 'a_random_secret_key'

STEAM_API_KEY = "yours api key"

users = {}
user_games = {}

# Set the locale to the system's default locale
locale.setlocale(locale.LC_COLLATE, '')

# Function for natural sorting (considering numbers in names)
def natural_sort_key(string):
    """
    Key function for sorting that treats numbers in game names as numbers.
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', string)]

@app.route("/", methods=["GET", "POST"])
def home():
    if 'username' in session:
        return render_template("home.html", error=None)

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = users.get(username)

        if user and user["password"] == hashlib.sha256(password.encode()).hexdigest():
            session["username"] = username
            return redirect(url_for("home"))
        else:
            return render_template("home.html", error="Invalid username or password")

    return render_template("home.html", error=None)

@app.route("/login", methods=["GET", "POST"])
def login():
    if 'username' in session:
        return redirect(url_for('my_games'))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = users.get(username)

        if user and user["password"] == hashlib.sha256(password.encode()).hexdigest():
            session["username"] = username
            return redirect(url_for("my_games"))
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if 'username' in session:
        return redirect(url_for('my_games'))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users:
            return render_template("register.html", error="Username already exists")

        users[username] = {
            "password": hashlib.sha256(password.encode()).hexdigest(),
            "games": []
        }
        return redirect(url_for("home"))  # Redirect to the login page

    return render_template("register.html", error=None)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))

@app.route("/my_games", methods=["GET", "POST"])
def my_games():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session["username"]
    games = user_games.get(username, [])

    # Sorting games by name using natural_sort_key
    games.sort(key=lambda x: natural_sort_key(x["name"]))

    message = session.pop('message', None)  # Get the message and remove it from the session

    if request.method == "POST":
        # Handling the completion status of games
        completed_games = request.form.getlist("completed")
        for game in games:
            game["completed"] = str(game["appid"]) in completed_games

        # Adding a new game
        new_game_name = request.form.get("new_game_name")
        if new_game_name:
            # Check if the game already exists
            if any(game["name"].lower() == new_game_name.lower() for game in games):
                return render_template("my_games.html", games=games, error="Game with this name already exists.")
            # Add the new game to the list
            games.append({"name": new_game_name, "appid": len(games) + 1, "completed": False})
            # Sort the games alphabetically after adding the new game
            games.sort(key=lambda x: natural_sort_key(x["name"]))
            # Display a success message
            message = f"Game '{new_game_name}' added successfully!"

        # Deleting a game
        delete_game_appid = request.form.get("delete_game")
        if delete_game_appid:
            # Find and delete the game based on its app ID
            game_to_delete = next((game for game in games if str(game["appid"]) == delete_game_appid), None)
            if game_to_delete:
                games = [game for game in games if str(game["appid"]) != delete_game_appid]
                message = f"Game '{game_to_delete['name']}' deleted successfully."

        # Update the list of games after adding/removing
        user_games[username] = games
        return render_template("my_games.html", games=games, message=message)

    return render_template("my_games.html", games=games, message=message)


@app.route("/fetch_games", methods=["POST"])
def fetch_games():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session["username"]
    profile_url = request.form.get("profile_url")

    steam_id = extract_steam_id(profile_url)
    if steam_id:
        games = get_steam_games(steam_id)
        if games is not None:
            user_games[username] = games
            session['message'] = "Games successfully fetched!"
            return redirect(url_for("my_games"))
        else:
            return render_template("home.html", error="Failed to fetch games. Make sure the profile is public.")
    else:
        return render_template("home.html", error="Invalid Steam profile URL.")

def extract_steam_id(profile_url):
    try:
        match = re.match(r"https?://steamcommunity\.com/profiles/(\d+)/?", profile_url)
        if match:
            return match.group(1)

        match = re.match(r"https?://steamcommunity\.com/id/([\w\-]+)/?", profile_url)
        if match:
            vanity_name = match.group(1)
            return resolve_vanity_url(vanity_name)
    except Exception as e:
        print(f"Error extracting Steam ID: {e}")
    return None

def resolve_vanity_url(vanity_name):
    try:
        url = f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/"
        params = {
            "key": STEAM_API_KEY,
            "vanityurl": vanity_name
        }
        response = requests.get(url, params=params)
        data = response.json()
        if data.get("response", {}).get("success") == 1:
            return data["response"]["steamid"]
    except Exception as e:
        print(f"Error resolving vanity URL: {e}")
    return None

def get_steam_games(steam_id):
    try:
        url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
        params = {
            "key": STEAM_API_KEY,
            "steamid": steam_id,
            "include_appinfo": "true",
            "format": "json"
        }
        response = requests.get(url, params=params)
        data = response.json()

        if "response" in data and "games" in data["response"]:
            return [
                {"name": game["name"], "appid": game["appid"], "completed": False}
                for game in data["response"]["games"]
            ]
    except Exception as e:
        print(f"Error fetching games: {e}")
    return None

if __name__ == "__main__":
    app.run(debug=True)
