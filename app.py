from flask import Flask, render_template, request
import os
import openai  # or whatever you're using for ChatGPT

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

def ask_chatgpt(question):
    prompt = f"""Answer this question in 1-2 sentences.
End your answer with a new line that says just 'Answer: Yes' or 'Answer: No'.\n\n
Question: {question}"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You're a helpful assistant that answers questions briefly."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

from flask import request  # ✅ Make sure this import is at the top

@app.route("/ask", methods=["POST"])
def ask_chatgpt():  # ✅ No arguments here
    data = request.get_json()
    question = data.get("question", "")

    prompt = f"""Answer this question in 1-2 sentences.
End your answer with a new line that says just 'Answer: Yes' or 'Answer: No'.\n\n
Question: {question}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You're a helpful assistant that answers questions briefly."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print("OpenAI error:", e)
        return "Error: Couldn't get a response from OpenAI"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
