# 🧠 Smart Task Planner AI

An intelligent web application that uses Google's Gemini AI to break down high-level goals into a detailed, actionable project plan.
This project features a full-stack implementation with a Flask backend, a SQLite database, and a responsive web interface.

## ✨ Features

* **AI-Powered Planning**: Leverages the Gemini Pro model to generate logical and comprehensive task breakdowns.
* **Interactive Web Interface**: A clean and user-friendly frontend built with HTML, CSS, and JavaScript for submitting goals and viewing plans.
* **Database Persistence**: Automatically saves every generated plan to a SQLite database for future reference.
* **Structured JSON API**: A robust backend API that provides plans in a clean, predictable JSON format.
* **Dynamic Results**: Displays generated tasks instantly on the webpage without needing a refresh.

## 🛠️ Technical Stack

* **Backend**: Python, Flask
* **Database**: SQLite
* **AI Model**: Google Gemini Pro
* **Frontend**: HTML5, CSS3, JavaScript
* **Deployment**: Gunicorn / Waitress (Production-ready)

## 🚀 Setup and Installation

### **Prerequisites**
* Python 3.8+
* A Google AI API Key

### **Instructions**

1.  **Clone the repository**:
    ```bash
    git clone [https://github.com/your-github-username/smart-task-planner.git](https://github.com/your-github-username/smart-task-planner.git)
    cd smart-task-planner
    ```

2.  **Create a `.env` file** in the root directory and add your Google AI API Key:
    ```
    GOOGLE_API_KEY=YOUR_API_KEY_HERE
    ```

3.  **Install the required Python packages**:
    ```bash
    # It's recommended to create a virtual environment first
    python -m venv venv
    source venv/bin/activate # On Windows, use `venv\Scripts\activate`

    # Install requirements
    pip install -r requirements.txt
    ```

4.  **Run the Flask application**:
    ```bash
    python app.py
    ```
    The application will start, create the `plans.db` file automatically, and be accessible at `http://127.0.0.1:5000`.

## ⚙️ How to Use

1.  Open your web browser and navigate to `http://127.0.0.1:5000`.
2.  Enter a goal into the text box (e.g., "Renovate my kitchen in 2 months").
3.  Click "Generate Plan".
4.  The AI-generated task list will appear on the page.
5.  To see all previously saved plans, navigate to `http://127.0.0.1:5000/plans`.

## 📝 API Endpoints

The application exposes the following API endpoints:

* **`POST /create-plan`**: Accepts a JSON object `{"goal": "your goal here"}` and returns the generated plan.
* **`GET /plans`**: (Browser only) Renders a page listing all saved plans.
* **`GET /plans/<id>`**: Returns the full JSON data for a single saved plan by its ID.