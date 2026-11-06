from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)
import sqlite3
from passlib.hash import bcrypt
from datetime import datetime

app = Flask(__name__)

CORS(app)

app.config["JWT_SECRET_KEY"] = "super-secure-secret-key"

jwt = JWTManager(app)

DATABASE = "database.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        patient_id TEXT,
        action TEXT,
        role TEXT,
        ip_address TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


@app.route("/register", methods=["POST"])
def register():

    data = request.json

    username = data["username"]
    password = data["password"]
    role = data["role"]

    hashed = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    try:

        conn = get_db()

        conn.execute(
            """
            INSERT INTO users
            (username,password,role)
            VALUES(?,?,?)
            """,
            (
                username,
                hashed.decode("utf-8"),
                role
            )
        )

        conn.commit()

        return jsonify({
            "message":"User Created"
        })

    except:

        return jsonify({
            "error":"User Exists"
        }),400


@app.route("/login", methods=["POST"])
def login():

    data = request.json

    username = data["username"]
    password = data["password"]

    conn = get_db()

    user = conn.execute(
        """
        SELECT * FROM users
        WHERE username=?
        """,
        (username,)
    ).fetchone()

    if not user:
        return jsonify({
            "error":"User not found"
        }),404

    if bcrypt.checkpw(
        password.encode("utf-8"),
        user["password"].encode("utf-8")
    ):

        token = create_access_token(
            identity=username
        )

        return jsonify({
            "token":token,
            "role":user["role"]
        })

    return jsonify({
        "error":"Wrong Password"
    }),401


@app.route("/add-log", methods=["POST"])
@jwt_required()
def add_log():

    current_user = get_jwt_identity()

    data = request.json

    patient_id = data["patient_id"]
    action = data["action"]
    role = data["role"]

    ip_address = request.remote_addr

    timestamp = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    conn = get_db()

    conn.execute("""
    INSERT INTO logs
    (
        username,
        patient_id,
        action,
        role,
        ip_address,
        timestamp
    )
    VALUES(?,?,?,?,?,?)
    """,
    (
        current_user,
        patient_id,
        action,
        role,
        ip_address,
        timestamp
    ))

    conn.commit()

    return jsonify({
        "message":"Access Logged"
    })


@app.route("/logs")
@jwt_required()
def logs():

    conn = get_db()

    rows = conn.execute("""
    SELECT * FROM logs
    ORDER BY id DESC
    """).fetchall()

    result = []

    for row in rows:

        result.append({
            "id":row["id"],
            "username":row["username"],
            "patient_id":row["patient_id"],
            "action":row["action"],
            "role":row["role"],
            "ip":row["ip_address"],
            "timestamp":row["timestamp"]
        })

    return jsonify(result)


@app.route("/dashboard")
@jwt_required()
def dashboard():

    conn = get_db()

    total_logs = conn.execute(
        "SELECT COUNT(*) FROM logs"
    ).fetchone()[0]

    total_users = conn.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]

    return jsonify({
        "total_logs":total_logs,
        "total_users":total_users,
        "security_alerts":7,
        "active_patients":433
    })


@app.route("/security-alerts")
@jwt_required()
def security_alerts():

    conn = get_db()

    rows = conn.execute("""
    SELECT *
    FROM logs
    GROUP BY ip_address
    HAVING COUNT(*) > 5
    """).fetchall()

    alerts = []

    for row in rows:

        alerts.append({
            "ip":row["ip_address"],
            "message":"Suspicious Activity"
        })

    return jsonify(alerts)


@app.route("/")
def home():
    return "Secure Patient Data Access Log System API Running Successfully"

if __name__ == "__main__":
    app.run(debug=True)
