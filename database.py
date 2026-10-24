import sqlite3
from datetime import datetime
from pathlib import Path


DATABASE_NAME = str(Path(__file__).resolve().parent / "sip_database.db")


# =========================================================
# CONVERT ANY VALUE TO SQLITE-SAFE TEXT
# =========================================================

def safe_value(value):

    if value is None:
        return ""

    if isinstance(value, list):
        return ", ".join(str(item) for item in value)

    if isinstance(value, tuple):
        return ", ".join(str(item) for item in value)

    if isinstance(value, dict):

        if "name" in value:
            return str(value["name"])

        return ", ".join(
            f"{key}: {val}"
            for key, val in value.items()
        )

    return str(value)


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    conn.row_factory = sqlite3.Row

    return conn


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def init_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS problems (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            register_number TEXT UNIQUE,

            problem TEXT NOT NULL,

            category TEXT,

            priority TEXT,

            confidence REAL,

            expertise TEXT,

            team TEXT,

            university TEXT,

            status TEXT DEFAULT 'Pending',

            progress INTEGER DEFAULT 0,

            solution TEXT DEFAULT '',

            created_at TEXT,

            updated_at TEXT

        )
    """)

    conn.commit()

    conn.close()

    print("Database initialized successfully.")


# =========================================================
# GENERATE REGISTER NUMBER
# =========================================================

def get_next_register_number():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM problems
    """)

    row = cursor.fetchone()

    total = row["total"] + 1

    conn.close()

    return f"{total:03d}"


# =========================================================
# SAVE PROBLEM
# =========================================================

def save_problem(
    problem,
    category="",
    priority="Medium",
    confidence=0,
    expertise="",
    team="",
    university=""
):

    # Convert EVERYTHING to safe SQLite values

    problem = safe_value(problem)

    category = safe_value(category)

    priority = safe_value(priority)

    expertise = safe_value(expertise)

    team = safe_value(team)

    university = safe_value(university)

    try:
        confidence = float(confidence)
    except:
        confidence = 0.0


    register_number = get_next_register_number()

    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO problems (

            register_number,
            problem,
            category,
            priority,
            confidence,
            expertise,
            team,
            university,
            status,
            progress,
            solution,
            created_at,
            updated_at

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        register_number,
        problem,
        category,
        priority,
        confidence,
        expertise,
        team,
        university,
        "Pending",
        0,
        "",
        now,
        now

    ))


    conn.commit()

    conn.close()


    print(
        f"Problem {register_number} saved successfully."
    )

    return register_number


# =========================================================
# GET ONE PROBLEM
# =========================================================

def get_problem(register_number):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM problems
        WHERE register_number = ?
    """, (
        register_number,
    ))

    row = cursor.fetchone()

    conn.close()


    if row is None:
        return None


    return dict(row)


# =========================================================
# GET ALL PROBLEMS FOR UNIVERSITY
# =========================================================

def get_problems_by_university(
    university
):

    university = safe_value(
        university
    )

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM problems
        WHERE university = ?
        ORDER BY id DESC
    """, (
        university,
    ))

    rows = cursor.fetchall()

    conn.close()


    return [
        dict(row)
        for row in rows
    ]


# =========================================================
# GET ALL PROBLEMS
# =========================================================

def get_all_problems():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM problems
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()


    return [
        dict(row)
        for row in rows
    ]


# =========================================================
# ACCEPT PROBLEM
# =========================================================

def accept_problem(
    register_number,
    university
):

    conn = get_connection()

    cursor = conn.cursor()

    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    cursor.execute("""
        UPDATE problems

        SET
            status = ?,
            progress = ?,
            updated_at = ?

        WHERE register_number = ? AND university = ?
    """, (

        "In Progress",
        10,
        now,
        register_number,
        safe_value(university)

    ))


    changed = cursor.rowcount

    conn.commit()

    conn.close()


    return changed > 0


# =========================================================
# UPDATE PROBLEM
# =========================================================

def update_problem(
    register_number,
    university,
    status=None,
    progress=None,
    solution=None
):

    conn = get_connection()

    cursor = conn.cursor()


    existing = get_problem(
        register_number
    )


    if existing is None or existing["university"] != safe_value(university):

        conn.close()

        return False


    if status is None:
        status = existing["status"]

    if progress is None:
        progress = existing["progress"]

    if solution is None:
        solution = existing["solution"]


    status = safe_value(status)

    solution = safe_value(solution)


    try:

        progress = int(progress)

    except:

        progress = 0


    progress = max(
        0,
        min(
            100,
            progress
        )
    )


    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    cursor.execute("""
        UPDATE problems

        SET
            status = ?,
            progress = ?,
            solution = ?,
            updated_at = ?

        WHERE register_number = ? AND university = ?
    """, (

        status,
        progress,
        solution,
        now,
        register_number,
        safe_value(university)

    ))


    changed = cursor.rowcount

    conn.commit()

    conn.close()


    return changed > 0
