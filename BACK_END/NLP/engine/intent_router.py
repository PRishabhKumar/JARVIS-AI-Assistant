import ollama
import json
import os
import re

# loading the system prompt

def load_prompt():
    path = os.path.join(os.path.dirname(__file__), 'system_prompt.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()

PROMPT = load_prompt()

def sanitize_parameter(parameter, intent, user_input):
    """Post-process extracted parameter to fix common model output issues."""
    if parameter is None:
        return None

    # Convert to string in case the model returns a number
    parameter = str(parameter).strip()

    # Strip key:value format labels (e.g., "contact name:Mom" → "Mom")
    if ':' in parameter:
        # Split on first colon and keep only the value part
        parts = parameter.split(':', 1)
        # Check if the left side looks like a label (contains letters, not a time like "7:30")
        left = parts[0].strip()
        if not left.isdigit() and not re.match(r'^\d{1,2}$', left):
            parameter = parts[1].strip()

    # For SET_ALARM, ensure we have the full time expression (e.g., "6 AM" not just "6")
    if intent == "SET_ALARM" and parameter:
        # If parameter is just a number, try to extract full time from user input
        if re.match(r'^\d{1,2}$', parameter):
            time_match = re.search(r'(\d{1,2}(?::\d{2})?\s*(?:AM|PM|am|pm|a\.m\.|p\.m\.))', user_input)
            if time_match:
                parameter = time_match.group(1).strip()

    if parameter == "" or parameter.lower() == "null":
        return None

    return parameter

def warmup_ollama():
    """Warms up the Ollama model by sending a dummy request."""
    try:
        print("Please wait, warming up AI Brain...")
        ollama.generate(model='llama3.2:1b', prompt='hello', options={"num_predict": 1})
        print("AI Brain is ready.")
    except Exception as e:
        print(f"Ollama Warmup Error: {e}")

def get_intent(user_input:str)->dict:
    try:
        response = ollama.generate(
            model= 'llama3.2:1b',
            system=PROMPT,
            prompt=user_input,
            options={
                "temperature":0
            },
            format="json"
        )
        raw = response['response'].strip()
        result = json.loads(raw)
        # check if the response has the required keys
        intent = result.get('intent', 'CHAT').upper()
        parameter = result.get('parameter', None)

        # Safeguard: Override CHAT/other to CLOSE_JARVIS if clear exit keywords are present
        exit_keywords = ['goodbye', 'shut down', 'exit', 'bye bye']
        if any(word in user_input.lower() for word in exit_keywords) and intent == "CHAT":
            print(f"DEBUG [Ollama]: Safeguard triggered - Exit keyword found. Overriding to CLOSE_JARVIS.")
            intent = "CLOSE_JARVIS"
            parameter = None
        
        # Safeguard: If the model thinks it's weather but no weather keywords are present, fallback to CHAT.
        # This helps smaller models (1B) which sometimes hallucinate weather intent for fact questions.
        if intent == "GET_WEATHER":
            weather_keywords = ['weather', 'forecast', 'temperature', 'temp', 'rain', 'raining', 'snow', 'hot', 'cold', 'sunny', 'cloudy', 'humidity', 'cats and dogs']
            if not any(word in user_input.lower() for word in weather_keywords):
                print(f"DEBUG [Ollama]: Safeguard triggered - No weather keywords found in '{user_input}'. Falling back to CHAT.")
                intent = "CHAT"
                parameter = None

        # Safeguard: CHAT should never have a parameter
        if intent == "CHAT":
            parameter = None

        if parameter == "null" or parameter == "":
            parameter = None

        # Post-process the parameter to fix common issues
        parameter = sanitize_parameter(parameter, intent, user_input)

        print(f"DEBUG [Ollama]: Intent={intent}, Parameter={parameter}")
        return {
            "intent": intent,
            "parameter":parameter
        }
    except json.JSONDecodeError as e:
        print(f"DEBUG [Ollama]: JSON parse error: {e}")
        print(f"DEBUG [Ollama]: Raw response was: {response['response']}")
        return {"intent": "CHAT", "parameter": None}
    
    except Exception as e:
        print(f"DEBUG [Ollama]: Error: {e}")
        return {"intent": "CHAT", "parameter": None}
    