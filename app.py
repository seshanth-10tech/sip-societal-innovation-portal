import os
import secrets
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

from ai_engine import analyze_problem

from database import (
    init_database,
    save_problem,
    get_problems_by_university,
    get_all_problems,
    accept_problem,
    update_problem
)

load_dotenv()

app = Flask(__name__)

from datetime import datetime

@app.context_processor
def inject_current_year():
    return {"current_year": datetime.now().year}

# Use an environment-provided key for stable deployments. Local runs get a
# temporary random key so the repository never contains a reusable secret.
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(32)


# ============================================================
# UNIVERSITY ACCOUNTS
# ============================================================

UNIVERSITY_ACCOUNTS = {

    "nitjsr": {
        "password": "nit123",
        "university": "NIT Jamshedpur"
    },

    "bitsindri": {
        "password": "bit123",
        "university": "BIT Sindri"
    },

    "bitmesra": {
        "password": "bit123",
        "university": "BIT Mesra"
    },

    "bau": {
        "password": "bau123",
        "university": "Birsa Agricultural University"
    },

    "gecpalamu": {
        "password": "gec123",
        "university": "GEC Palamu"
    },

    # Added because your current AI engine is returning
    # "Birsa Institute of Technology"
    "birsa": {
        "password": "birsa123",
        "university": "Birsa Institute of Technology"
    }
}


# ============================================================
# INITIALIZE DATABASE
# ============================================================

init_database()


# ============================================================
# HELPER
# ============================================================

def safe_text(value):

    if value is None:
        return ""

    if isinstance(value, list):
        return ", ".join(str(x) for x in value)

    if isinstance(value, dict):
        return str(value)

    return str(value)


# ============================================================
# HOME / PORTAL
# ============================================================

@app.route("/")
def home():
    return render_template("portal.html")


@app.route("/portal")
def portal():
    return render_template("portal.html")


# ============================================================
# CITIZEN PORTAL
# ============================================================

@app.route("/citizen")
def citizen():
    return render_template("index.html")


# ============================================================
# ANALYZE CITIZEN PROBLEM
# ============================================================
#
# IMPORTANT:
# This route ONLY analyzes the problem.
#
# It DOES NOT save the problem.
#
# Saving happens only after the citizen clicks
# "Submit Challenge".
# ============================================================

@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No data received."
            }), 400

        problem = data.get("problem", "").strip()

        if not problem:
            return jsonify({
                "success": False,
                "error": "Please enter a problem."
            }), 400


        print("\n")
        print("=" * 60)
        print("ANALYZING CITIZEN CHALLENGE")
        print("=" * 60)
        print(problem)


        # --------------------------------------------
        # AI ANALYSIS
        # --------------------------------------------

        result = analyze_problem(problem)

        print("\nAI RESULT:")
        print(result)


        # --------------------------------------------
        # Extract AI result
        # --------------------------------------------

        university_data = result.get("university", {})

        if isinstance(university_data, dict):

            university = university_data.get(
                "name",
                "University not identified"
            )

            university_location = university_data.get("location", "Jharkhand")
            university_match = university_data.get("score", 0)
            university_focus = university_data.get("domains", [])

        else:

            university = safe_text(university_data)
            university_location = "Jharkhand"
            university_match = 0
            university_focus = []


        category = (
            result.get("category")
            or result.get("domain")
            or "General"
        )

        priority = result.get(
            "priority",
            "Medium"
        )

        confidence = result.get(
            "confidence",
            0
        )

        expertise = result.get(
            "expertise",
            ""
        )

        team = result.get(
            "team",
            "General Innovation Team"
        )

        solution = result.get(
            "solution",
            "Start by learning from the people affected, then work with a local institution to test a practical next step."
        )


        # --------------------------------------------
        # Convert values safely
        # --------------------------------------------

        category = safe_text(category)
        priority = safe_text(priority)
        expertise = safe_text(expertise)
        team = safe_text(team)
        university = safe_text(university)
        solution = safe_text(solution)

        university_details = {
            "name": university,
            "location": safe_text(university_location),
            "focus_areas": safe_text(university_focus) or category,
            "match_score": university_match
        }


        try:
            confidence = float(confidence)
        except:
            confidence = 0


        print("\nANALYSIS RESULT")
        print("-" * 40)
        print("University:", university)
        print("Category:", category)
        print("Priority:", priority)
        print("Confidence:", confidence)
        print("Expertise:", expertise)
        print("Team:", team)
        print("-" * 40)


        # --------------------------------------------
        # Store analysis temporarily in SESSION
        # --------------------------------------------
        #
        # This is NOT saved to database yet.
        #
        # The citizen must click
        # "Submit Challenge".
        # --------------------------------------------

        session["pending_challenge"] = {

            "problem": problem,

            "category": category,

            "priority": priority,

            "confidence": confidence,

            "expertise": expertise,

            "team": team,

            "solution": solution,

            "university_details": university_details,

            "university": university
        }


        # --------------------------------------------
        # Send result back to browser
        # --------------------------------------------

        return jsonify({

            "success": True,

            "problem": problem,

            "category": category,

            "domain": category,

            "priority": priority,

            "confidence": confidence,

            "expertise": expertise,

            "team": team,

            "solution": solution,

            "university_details": university_details,

            "university": university,

            "message": "Challenge analyzed successfully."
        })


    except Exception as e:

        print("\nERROR DURING ANALYSIS:")
        print(str(e))

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# ============================================================
# SUBMIT CHALLENGE
# ============================================================
#
# This is called ONLY when the citizen clicks
# "Submit Challenge".
# ============================================================

@app.route("/submit", methods=["POST"])
def submit_challenge():

    try:

        # Get pending challenge from session
        pending = session.get("pending_challenge")


        if not pending:

            return jsonify({

                "success": False,

                "error": "No analyzed challenge found. Please analyze your problem first."

            }), 400


        print("\n")
        print("=" * 60)
        print("SUBMITTING CITIZEN CHALLENGE")
        print("=" * 60)


        # --------------------------------------------
        # SAVE TO DATABASE
        # --------------------------------------------

        register_number = save_problem(

            problem=pending["problem"],

            category=pending["category"],

            priority=pending["priority"],

            confidence=pending["confidence"],

            expertise=pending["expertise"],

            team=pending["team"],

            university=pending["university"]
        )


        print("Problem submitted successfully.")
        print("REGISTER NUMBER:", register_number)


        # --------------------------------------------
        # Remove temporary challenge
        # --------------------------------------------

        session.pop("pending_challenge", None)


        # Remember latest register number
        session["last_register_number"] = register_number


        return jsonify({

            "success": True,

            "register_number": register_number,

            "status": "Submitted",

            "message": "Your challenge has been submitted successfully."
        })


    except Exception as e:

        print("\nERROR DURING SUBMISSION:")
        print(str(e))

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# ============================================================
# UNIVERSITY LOGIN
# ============================================================

@app.route("/university/login", methods=["GET", "POST"])
def university_login():

    if request.method == "GET":

        return render_template(
            "university_login.html"
        )


    username = request.form.get(
        "username",
        ""
    ).strip()

    password = request.form.get(
        "password",
        ""
    )


    account = UNIVERSITY_ACCOUNTS.get(username)


    if account and account["password"] == password:

        session["university_logged_in"] = True

        session["username"] = username

        session["university"] = account["university"]


        return redirect(
            url_for("university_dashboard")
        )


    return render_template(

        "university_login.html",

        error="Invalid username or password."

    )


# ============================================================
# UNIVERSITY DASHBOARD
# ============================================================

@app.route("/university/dashboard")
def university_dashboard():

    if not session.get("university_logged_in"):

        return redirect(
            url_for("university_login")
        )


    university = session.get(
        "university"
    )


    return render_template(

        "university_dashboard.html",

        university=university,

        username=session.get("username", "University team")

    )


# ============================================================
# UNIVERSITY REPORTS API
# ============================================================

@app.route("/api/university/<path:university_name>")
def university_reports(university_name):

    if not session.get("university_logged_in"):

        return jsonify({

            "success": False,

            "error": "Unauthorized."

        }), 401


    logged_university = session.get(
        "university"
    )


    # Security check
    if university_name != logged_university:

        return jsonify({

            "success": False,

            "error": "Access denied."

        }), 403


    reports = get_problems_by_university(
        logged_university
    )


    return jsonify({

        "success": True,

        "university": logged_university,

        "reports": reports

    })


# ============================================================
# ALL REPORTS
# ============================================================

@app.route("/api/problems")
def all_problems():

    reports = get_all_problems()

    return jsonify({

        "success": True,

        "reports": reports

    })


# ============================================================
# ACCEPT PROBLEM
# ============================================================

@app.route(
    "/api/problem/<register_number>/accept",
    methods=["POST"]
)
def accept_problem_route(register_number):

    if not session.get("university_logged_in"):

        return jsonify({

            "success": False,

            "error": "Unauthorized."

        }), 401


    university = session.get(
        "university"
    )


    try:

        result = accept_problem(

            register_number,

            university

        )


        return jsonify({

            "success": result

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# ============================================================
# UPDATE PROBLEM
# ============================================================

@app.route(
    "/api/problem/<register_number>/update",
    methods=["POST"]
)
def update_problem_route(register_number):

    if not session.get("university_logged_in"):

        return jsonify({

            "success": False,

            "error": "Unauthorized."

        }), 401


    university = session.get(
        "university"
    )


    try:

        data = request.get_json() or {}


        status = data.get(
            "status"
        )

        progress = data.get(
            "progress"
        )

        solution = data.get(
            "solution"
        )


        result = update_problem(

            register_number,

            university,

            status=status,

            progress=progress,

            solution=solution

        )


        return jsonify({

            "success": result

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# ============================================================
# UNIVERSITY LOGOUT
# ============================================================

@app.route("/university/logout")
def university_logout():

    session.pop(
        "university_logged_in",
        None
    )

    session.pop(
        "username",
        None
    )

    session.pop(
        "university",
        None
    )


    return redirect(
        url_for("home")
    )


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=os.environ.get("FLASK_DEBUG", "").lower() in {"1", "true", "yes"},
        host="127.0.0.1",
        port=int(os.environ.get("PORT", "5000"))
    )
