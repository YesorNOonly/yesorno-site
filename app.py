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

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return {"error": "No question provided."}, 400

    answer = ask_chatgpt(question)

    final_word = answer.strip().lower().split()[-1]
    if "yes" in final_word:
        short = "Yes"
    elif "no" in final_word:
        short = "No"
    else:
        short = "Couldn't decide"

    return {"answer": short, "full_answer": answer}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
