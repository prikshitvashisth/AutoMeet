from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

meeting_summary = ""  # Store the summary in memory

@app.route("/transcribe", methods=["POST"])
def transcribe():
    """ Calls the Python script to start transcription """
    global meeting_summary
    try:
        result = subprocess.run(["python", "main.py"], check=True, capture_output=True, text=True)
        meeting_summary = result.stdout  # Capture the generated summary
        return jsonify({"message": "Transcription started and sent to Slack!"})
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"})

@app.route("/summary", methods=["GET"])
def get_summary():
    """ Returns the AI-generated summary """
    return jsonify({"summary": meeting_summary})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
