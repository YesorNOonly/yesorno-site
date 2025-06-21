import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()

app = Flask(__name__)


def ask_chatgpt(question):
    prompt = (
        f"Answer this question in 1-2 sentences. "
        f"End your answer with a new line that says just 'Answer: Yes' or 'Answer: No'.\\n\\n"
        f"Question: {question}"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You're a helpful assistant that answers questions briefly and clearly."},
            {"role": "user", "content": prompt}
        ]
    )

    full_answer = response.choices[0].message.content.strip()

    # Extract final Yes/No from the line starting with 'Answer:'
    final_word = "couldn't decide"
    for line in full_answer.splitlines():
        if line.strip().lower().startswith("answer:"):
            final_word = line.split(":")[-1].strip().lower()
            break

    if "yes" == final_word:
        result = "Yes"
    elif "no" == final_word:
        result = "No"
    else:
        result = "Couldn't decide"

    return result, full_answer

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    full_answer = ""

    if request.method == "POST":
        question = request.form["question"]
        result, full_answer = ask_chatgpt(question)
        return render_template("index.html", answer=result, explanation=full_answer)

    return render_template("index.html", answer=result, explanation=full_answer)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)








