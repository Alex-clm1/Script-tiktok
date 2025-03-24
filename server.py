from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

JSON_FILE = "questions.json"

@app.route("/")
def home():
    return render_template("index.html")  # Charge la page web


# Charger les questions
def load_questions():
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Sauvegarder les questions
def save_questions(questions):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=4, ensure_ascii=False)

@app.route("/get_questions", methods=["GET"])
def get_questions():
    return jsonify(load_questions())

@app.route("/add_question", methods=["POST"])
def add_question():
    data = request.json
    questions = load_questions()
    questions.append({"question": data["question"], "answer": data["answer"]})
    save_questions(questions)
    return jsonify({"message": "Question ajoutée !"})

@app.route("/delete_question", methods=["POST"])
def delete_question():
    data = request.json
    questions = load_questions()
    questions = [q for q in questions if q["question"] != data["question"]]
    save_questions(questions)
    return jsonify({"message": "Question supprimée !"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
