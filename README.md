## SHL Assessment Recommender
A conversational AI agent that recommends SHL Individual Test Solutions based on job requirements.
## Live API
## Base URL:https://shl-recommender-wziv.onrender.com
## Endpoint	Method	Description
`/health`	GET	Returns `{"status": "ok"}`
`/chat`	        POST	Conversational assessment recommender
## How It Works
```
User message comes in
        ↓
main.py receives it
        ↓
agent.py searches catalog
        ↓
catalog.py finds matching tests
        ↓
Groq AI picks best ones
        ↓
JSON reply goes back
```
## Example
## Request:
```json
POST /chat
{
  "messages": [
    {"role": "user", "content": "I am hiring a Java developer"}
  ]
}
```
## Response:
```json
{
  "reply": "What seniority level are you hiring for?",
  "recommendations": [],
  "end_of_conversation": false
}
```
## Agent Behaviors
# Behavior	            Example
Clarify vague queries	  "I need an assessment" → asks what role
Recommend tests	          "Hiring Java dev" → gives 1-10 tests
Refine recommendations	  "Also add personality tests" → updates list
Compare tests	          "Difference between OPQ32 and Java test?"
Refuse off-topic	  "What salary should I offer?" → politely refuses
## Test Types
# Code	Meaning
A	Ability / Aptitude
P	Personality / Behaviour
K	Knowledge / Skills
S	Situational Judgment
C	Competency
## Project Structure
```
shl-recommender/
    main.py          → FastAPI server (/health and /chat endpoints)
    agent.py         → AI brain (decides what to say)
    catalog.py       → Search engine (finds relevant tests)
    requirements.txt → Libraries needed
    data/
        catalog.json → 50 SHL Individual Test Solutions
```
## Tech Stack
# Tool	                Purpose
FastAPI	                API framework
Groq (LLaMA 3.3 70B)	Free AI model
BM25 Search	        Find relevant tests from catalog
Render.com	        Free hosting
## Run Locally
```bash
# Install libraries
pip install -r requirements.txt

# Add your Groq API key
echo "GROQ_API_KEY=your_key_here" > .env

# Start server
uvicorn main:app --reload

# Test it
# Open http://127.0.0.1:8000/docs
```
## API Schema
Every /chat response follows this exact schema:
```json
{
  "reply": "string",
  "recommendations": [
    {
      "name": "string",
      "url": "string",
      "test_type": "string"
    }
  ],
  "end_of_conversation": false
}
```
. recommendations is empty when clarifying
. recommendations has 1-10 items when shortlist is ready
. end_of_conversation is true only when task is complete
