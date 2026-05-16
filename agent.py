import os
import json
import re
from dotenv import load_dotenv
from groq import Groq
from catalog import search

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def build_system_prompt(relevant_tests):
    tests_text = ""
    for test in relevant_tests:
        tests_text += f"- {test['name']} ({test['test_type']}) : {test['description']} | URL: {test['url']}\n"

    return f"""You are an SHL Assessment Recommender chatbot.

You help hiring managers pick the right tests from SHL's catalog.

RULES:
1. If the user is vague (like "I need a test"), ask what role they are hiring for
2. Only recommend tests from the list below - never make up tests
3. If asked about salary, legal, or anything not SHL related - politely refuse
4. Recommend between 1 and 10 tests when you have enough information
5. Always respond in this EXACT JSON format - nothing else:

{{
  "reply": "your message to the user here",
  "recommendations": [
    {{"name": "test name", "url": "test url", "test_type": "letter"}}
  ],
  "end_of_conversation": false
}}

If you are still asking questions, keep recommendations as empty list [].

AVAILABLE SHL TESTS:
{tests_text}
"""


def chat(messages):
    # Step 1: get all the user text to search catalog
    user_text = " ".join(
        m["content"] for m in messages if m["role"] == "user"
    )

    # Step 2: search catalog for relevant tests
    relevant_tests = search(user_text, top_k=10)

    # Step 3: build the instruction prompt
    system_prompt = build_system_prompt(relevant_tests)

    # Step 4: send to Groq AI and get reply
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_prompt}] + messages,
        temperature=0.2,
        max_tokens=1024
    )

    # Step 5: get the text reply
    raw = response.choices[0].message.content
    print("GROQ RAW RESPONSE:", raw)

    # Step 6: clean and parse the JSON
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    try:
        result = json.loads(raw)
    except:
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            try:
                result = json.loads(match.group())
            except:
                result = {
                    "reply": "Could you tell me what role you are hiring for?",
                    "recommendations": [],
                    "end_of_conversation": False
                }
        else:
            result = {
                "reply": "Could you tell me what role you are hiring for?",
                "recommendations": [],
                "end_of_conversation": False
            }

    return result


if __name__ == "__main__":
    messages = [
        {"role": "user", "content": "I am hiring a Java developer"}
    ]
    result = chat(messages)
    print(result)