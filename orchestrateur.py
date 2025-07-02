import os
import sys
import json
from dotenv import load_dotenv
from openai import AzureOpenAI

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

model_name = os.getenv("AI_MODEL_DEPLOYMENT_NAME")
deployment = os.getenv("AI_MODEL_DEPLOYMENT")

api_version = "2024-12-01-preview"

LLM = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=os.getenv("AZURE_AI_ENDPOINT"),
    api_key=os.getenv("AZURE_AI_KEY"),
)

# Point d'amelioration :
    # Les agents devrait pouvoir s'appeler entre eux
    # Les prochain agent doivent avoir les reponses des agents precedents
    # Il faudrait envoyer au agent une description de ce qu'il doivent faire

def last_action(message: str):
    return "laste action"

def detect_intents(message: str) -> list[dict]:
    available_agents = [
        {"agent": "document_agent", "description": "Pour obtenir des informations documentaires, notamment sur les plantes, objets ou données textuelles."},
        {"agent": "weather_agent", "description": "Pour récupérer les prévisions météorologiques ou les conditions climatiques."},
        {"agent": "general", "description": "Pour les cas généraux où aucun agent spécifique ne convient."}
    ]

    prompt = (
        f"Voici la liste des agents disponibles : {json.dumps(available_agents, ensure_ascii=False)}\n"
        "Tu es un routeur intelligent. Selon le message utilisateur, retourne une liste JSON ordonnée avec les agents à appeler.\n"
        "Chaque élément de la liste doit être un objet avec :\n"
        "- 'agent': le nom de l'agent\n"
        "- 'reason': une phrase expliquant pourquoi cet agent est utile\n"
        "Exemple : [{\"agent\": \"document_agent\", \"reason\": \"pour connaître les besoins d'arrosage\"}, {\"agent\": \"weather_agent\", \"reason\": \"pour savoir s'il va pleuvoir\"}]\n"
        f"Message utilisateur : {message}"
    )

    response = LLM.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "Tu es un planificateur intelligent qui détermine les agents à appeler, dans l'ordre, avec une raison."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0
    )

    try:
        intents = json.loads(response.choices[0].message.content.strip())
        print("intents : ",intents)
        if isinstance(intents, list):
            return intents
    except:
        pass
    return [{"agent": "general", "reason": "aucun agent spécifique détecté"}]

def call_general_agent(message: str) -> str:
    response = LLM.chat.completions.create(
        messages=[
            {"role": "system", "content": "Tu es un assistant intelligent expert dans la gestion de plante"},
            {"role": "user", "content": message}
        ],
        max_tokens=1024,
        temperature=1.0,
        top_p=1.0,
        model=deployment,
    )

    return response.choices[0].message.content

def orchestrate(user_message: str):
    agents_plan = detect_intents(user_message)
    context = {}

    for step in agents_plan:
        agent = step.get("agent")
        if agent == "document_agent":
            # context["document"] = call_document_agent(user_message)
            context["document"] = "Il faut arroser les plantes"
        elif agent == "weather_agent":
            # context["weather"] = call_weather_agent(user_message)
            context["weather"] = "Il va pleuvoir dans 6 heures"
        elif agent == "general":
            context["general"] = call_general_agent(user_message)

    context_prompt = "Voici les informations obtenues des différents agents :\n"
    for key, value in context.items():
        context_prompt += f"[{key.upper()}]: {value}\n"
    context_prompt += "\nEn te basant uniquement sur ces informations, réponds à la question de l'utilisateur :\n"
    context_prompt += user_message

    response = LLM.chat.completions.create(
        model=deployment,
        stream=True,
        messages=[
            {"role": "system", "content": "Tu es un assistant intelligent expert dans la gestion de plante qui synthétise des réponses à partir des résultats d'autres agents."},
            {"role": "user", "content": context_prompt}
        ],
        max_tokens=1024,
        temperature=0.7
    )

    for update in response:
        if update.choices:
            print((update.choices[0].delta.content or "").encode('utf-8', errors='ignore').decode('utf-8'), end="")

    # return response.choices[0].message.content
    # return "End Message"

if __name__ == "__main__":
    message = input("Message: ")
    orchestrate(message)