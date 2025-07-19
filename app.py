from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

with open('faq.json') as f:
    faqs = json.load(f)

@app.route('/')
def home():
    return render_template('index.html', faq=faqs)

@app.route('/get', methods=['POST'])
def chatbot_response():
    user_input = request.form['msg']
    best_match = None
    highest_score = 0

    for faq in faqs:
        score = fuzz.ratio(user_input.lower(), faq['question'].lower())
        if score > highest_score:
            highest_score = score
            best_match = faq

    if highest_score > 60:  # minimum match threshold
        response = best_match['answer']
    else:
        response = "Sorry, I don't understand that yet. Please try asking differently or check with a tax expert."

    return response

if __name__ == '__main__':
    app.run(debug=True)
