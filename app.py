# app.py (Final version with Database)

import os
import json
import sqlite3 # Built-in library for SQLite
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# --- NEW: Database Setup ---
def init_db():
    # Establishes a connection to the database file (creates it if it doesn't exist)
    conn = sqlite3.connect('plans.db')
    cursor = conn.cursor()
    # Creates a 'plans' table if it doesn't already exist
    # We store the plan_data as a JSON text string
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            plan_data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('models/gemini-pro-latest') 
except KeyError:
    print("🔴 Error: GOOGLE_API_KEY not found. Please set it in the .env file.")
    exit()

# --- Page Routes ---
@app.route('/')
def index():
    return render_template('index.html')

# --- NEW: Route to view all saved plans ---
@app.route('/plans')
def view_plans():
    conn = sqlite3.connect('plans.db')
    # Use a dictionary cursor to get column names
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    # Fetch all plans, newest first
    cursor.execute("SELECT id, project_name, created_at FROM plans ORDER BY created_at DESC")
    plans = cursor.fetchall()
    conn.close()
    # Render a new HTML page to display the list of plans
    return render_template('plans.html', plans=plans)

# --- API Endpoints ---
@app.route('/create-plan', methods=['POST'])
def create_plan_endpoint():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400
    
    data = request.get_json()
    goal = data.get('goal')

    if not goal:
        return jsonify({"error": "The 'goal' field is required."}), 400
    
    print(f"🚀 Received goal: {goal}")
    plan = generate_plan(goal)
    
    if "error" in plan:
        return jsonify(plan), 500
    
    # --- NEW: Save the successful plan to the database ---
    try:
        conn = sqlite3.connect('plans.db')
        cursor = conn.cursor()
        # Convert the plan dictionary to a JSON string for storage
        plan_json_string = json.dumps(plan)
        cursor.execute(
            "INSERT INTO plans (project_name, plan_data) VALUES (?, ?)",
            (plan.get('project_name', 'Untitled Plan'), plan_json_string)
        )
        conn.commit()
        conn.close()
        print("💾 Plan saved to database successfully!")
    except Exception as e:
        print(f"🔴 Database save error: {e}")

    print("✅ Plan generated successfully!")
    return jsonify(plan)

# --- NEW: API endpoint to get a single saved plan ---
@app.route('/plans/<int:plan_id>')
def get_plan(plan_id):
    conn = sqlite3.connect('plans.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT plan_data FROM plans WHERE id = ?", (plan_id,))
    plan_record = cursor.fetchone()
    conn.close()
    if plan_record:
        # The data is stored as a string, so we parse it back into JSON
        plan_data = json.loads(plan_record['plan_data'])
        return jsonify(plan_data)
    return jsonify({"error": "Plan not found"}), 404

def generate_plan(goal):
    prompt = f"""
    Break down the following goal into a detailed plan.
    The goal is: "{goal}"

    Provide a valid JSON object as output. Do not include any text or markdown formatting before or after the JSON.
    The object must have a key "project_name" with a creative name for the project, and a key "tasks" which is a list of task objects.
    Each task object must have these keys: "task_id", "task_name", "description", "timeline_days", and "dependencies".
    "dependencies" must be a list of "task_id"s. If there are no dependencies, it must be an empty list [].
    """
    
    try:
        response = model.generate_content(prompt)
        json_response_text = response.text.strip().lstrip("```json").rstrip("```").strip()
        plan = json.loads(json_response_text)
        return plan
    except Exception as e:
        print(f"🔴 An error occurred: {e}")
        return {"error": "Failed to generate a valid plan from the AI model."}

# Initialize the database when the app starts
if __name__ == '__main__':
    init_db() 
    app.run(host='0.0.0.0', port=5000, debug=True)