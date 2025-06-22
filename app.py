from flask import Flask, request, render_template
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()  # Only needed for local development

# Load API key from environment (Render or local .env)
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

app = Flask(__name__)

def ask_chatgpt(question):
    prompt = (
        f"Answer this question in 1-2 sentences. "
        f"End your answer with a new line that says just 'Answer: Yes' or 'Answer: No'.\n\n"
        f"Question: {question}"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You're a helpful assistant that answers questions briefly and clearly."},
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

    # Decide short 'Yes' / 'No' based on final word
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

