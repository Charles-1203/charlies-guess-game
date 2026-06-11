from flask import Flask, render_template, request, jsonify, session
import random
import os

app = Flask(__name__)

app.secret_key = "charlie_guess_game_secret"

LEADERBOARD_FILE = "leaderboard.txt"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start():

    data = request.get_json()

    session["name"] = data["name"]
    session["random_number"] = random.randint(1, 100)
    session["guesses"] = []

    return jsonify({
        "status": "started",
        "name": session["name"]
    })


@app.route("/guess", methods=["POST"])
def guess():

    data = request.get_json()

    user_num = int(data["guess"])

    guesses = session.get("guesses", [])

    guesses.append(user_num)

    session["guesses"] = guesses

    random_number = session["random_number"]

    if user_num < random_number:

        return jsonify({
            "status": "continue",
            "message": "📈 Higher Number Please",
            "attempts": len(guesses)
        })

    elif user_num > random_number:

        return jsonify({
            "status": "continue",
            "message": "📉 Lower Number Please",
            "attempts": len(guesses)
        })

    else:

        score = len(guesses)

        if score <= 3:
            grade = "A+"
        elif score <= 5:
            grade = "A"
        elif score <= 7:
            grade = "B+"
        elif score <= 9:
            grade = "B"
        elif score <= 11:
            grade = "C"
        else:
            grade = "Needs More Practice"

        with open(LEADERBOARD_FILE, "a") as f:
            f.write(
                f"{session['name']},{score},{grade}\n"
            )

        return jsonify({
            "status": "won"
        })


@app.route("/score")
def score():

    guesses = session.get("guesses", [])

    score = len(guesses)

    if score <= 3:
        grade = "A+"
    elif score <= 5:
        grade = "A"
    elif score <= 7:
        grade = "B+"
    elif score <= 9:
        grade = "B"
    elif score <= 11:
        grade = "C"
    else:
        grade = "Needs More Practice"

    leaderboard = []

    if os.path.exists(LEADERBOARD_FILE):

        with open(LEADERBOARD_FILE, "r") as f:

            for line in f:

                parts = line.strip().split(",")

                if len(parts) == 3:

                    leaderboard.append({
                        "name": parts[0],
                        "attempts": int(parts[1]),
                        "grade": parts[2]
                    })

    leaderboard.sort(
        key=lambda x: x["attempts"]
    )

    leaderboard = leaderboard[:10]

    return render_template(
        "score.html",
        name=session["name"],
        attempts=score,
        grade=grade,
        guesses=guesses,
        random_number=session["random_number"],
        leaderboard=leaderboard
    )


if __name__ == "__main__":
    app.run(debug=True)