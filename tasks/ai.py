import google.generativeai as genai
from django.conf import settings

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

# Load Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_task(title, description, deadline, priority, estimated_hours):
    prompt = f"""
You are an AI productivity assistant.

Analyze this task:

Title: {title}
Description: {description}
Deadline: {deadline}
Priority: {priority}
Estimated Hours: {estimated_hours}

Give the answer in exactly this format:

Risk Level:
Reason:
Suggestion:
"""

    response = model.generate_content(prompt)
    return response.text


def generate_schedule(title, description, deadline, priority, estimated_hours):

    prompt = f"""
You are an expert productivity coach.

Create a realistic hourly schedule for this task.

Task:
Title: {title}
Description: {description}
Deadline: {deadline}
Priority: {priority}
Estimated Hours: {estimated_hours}

Return only a schedule.

Example:

09:00 - 10:00
Research

10:15 - 12:00
Coding

12:00 - 01:00
Lunch

01:00 - 03:00
Testing
"""

    response = model.generate_content(prompt)

    return response.text


import json

def parse_voice_command(command):

    prompt = f"""
You are an AI Task Parser.

Convert the user's spoken command into JSON.

Return ONLY valid JSON.

Use this exact format:

{{
"title":"Complete ML Project",
"description":"Finish all pending work",
"priority":"High",
"estimated_hours":5,
"deadline":"2026-06-30T18:00"
}}

Rules:

1. Return ONLY JSON.
2. Deadline format must be:
YYYY-MM-DDTHH:MM
3. Priority must be High, Medium or Low.
4. Estimated hours must be a number.
5. If user doesn't mention deadline,
assume tomorrow at 6:00 PM.

User command:

{command}
"""

    response = model.generate_content(prompt)

    text = response.text.strip()

    print(text)

    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()

    elif text.startswith("```"):
        text = text.replace("```", "").strip()

    return json.loads(text)



def recommend_priority(title, description, deadline, priority, estimated_hours):

    prompt = f"""
You are an expert productivity assistant.

Analyze the task and recommend the BEST priority.

Task
Title: {title}
Description: {description}
Deadline: {deadline}
Current Priority: {priority}
Estimated Hours: {estimated_hours}

Reply ONLY in this format:

Recommended Priority:
Reason:
"""

    response = model.generate_content(prompt)

    return response.text

def productivity_recommendation(title, description, deadline, estimated_hours):

    prompt = f"""
You are an AI productivity coach.

Task:
Title: {title}
Description: {description}
Deadline: {deadline}
Estimated Hours: {estimated_hours}

Give practical productivity recommendations.

Reply only with bullet points.
"""

    response = model.generate_content(prompt)

    return response.text