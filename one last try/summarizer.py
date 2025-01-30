import ollama

def summarize_text(text):
    """ Summarizes a meeting transcript using Ollama Mistral locally """
    response = ollama.chat("mistral", messages=[{"role": "user", "content": f"Summarize this meeting transcript:\n{text}"}])
    return response["message"]["content"]

def extract_action_items(text):
    """ Extracts action items from the meeting """
    response = ollama.chat("mistral", messages=[{"role": "user", "content": f"Extract clear action items from this meeting:\n{text}"}])
    return response["message"]["content"]

def extract_dates(text):
    """ Identifies important deadlines and dates """
    response = ollama.chat("mistral", messages=[{"role": "user", "content": f"Extract all important dates and deadlines from this meeting:\n{text}"}])
    return response["message"]["content"]

def identify_speakers(text):
    """ Labels speakers if not identified in transcript """
    response = ollama.chat("mistral", messages=[{"role": "user", "content": f"Identify speakers in this conversation:\n{text}"}])
    return response["message"]["content"]
