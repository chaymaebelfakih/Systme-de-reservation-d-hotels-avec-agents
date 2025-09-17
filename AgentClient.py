from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from termcolor import colored
import emoji
import os 
# Charger la clé API Google et initialiser l'LLM
load_dotenv()
google_api_key ="AIzaSyDNWdevmyLrV9baBzb90p63Tg97OF57wHI"

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.5,
    google_api_key=google_api_key,
)

# Définir le template de prompt pour les questions
prompt = PromptTemplate(
    input_variables=["context"],
    template="""
    Vous êtes un agent intelligent qui aide à recommander des hôtels en posant des questions pertinentes 
    pour comprendre les besoins de l'utilisateur. Voici les informations disponibles sur l'utilisateur : 
    {context}
    Actuellement, vous devez poser une question uniquement sur les catégories suivantes.

    Voici les catégories possibles que vous pouvez traiter dans vos questions :
    
    - Le budget prévu pour le séjour.
    - La localisation ou la ville souhaitée pour l'hôtel.
    - Les équipements (ex. piscine, parking, wi-fi, sports, etc.).
    - Les activités recherchés (ex. spa, randonnées, visites culturelles)
    - La catégorie de l'hôtel (familial, luxe, économique, etc.).
    - Le nombre de chambres ou de lits nécessaires.
    

    Posez une question claire et concise qui se concentre uniquement sur une catégorie 
    Votre question doit permettre de collecter une information précise et utile.
    """
)


class AgentClient:
    def __init__(self, llm):
        self.context = ""
        self.responses = {  # Chaque catégorie devient une clé distincte
            'budget': None,
            'location': None,
            'equipments': None,
            'activities': None,
            'hotel_category': None,
            'number_of_rooms': None
        }
        self.question_count = 0
        self.llm = llm

    def categorize_question(self, question_text):
        # Utiliser des catégories explicites pour identifier la question
        if "votre budget" in question_text.lower():
            return "budget"
        elif "localisation" in question_text.lower() or "ville" in question_text.lower():
            return "location"
        elif "équipements" in question_text.lower():
            return "equipments"
        elif "activités" in question_text.lower():
            return "activities"
        elif "catégorie d'hôtel" in question_text.lower():
            return "hotel_category"
        elif "nombre de chambres" in question_text.lower():
            return "number_of_rooms"
        else:
            return "autre"

    def ask_questions(self, max_questions=6):
        print("Je vais commencer à poser des questions pour mieux comprendre vos besoins.")
        
        while self.question_count < max_questions:
            formatted_prompt = prompt.format(context=self.context)
            question_message = self.llm.invoke(formatted_prompt)
            question_text = question_message.content

            # Identifier la catégorie de la question
            category = self.categorize_question(question_text)

            print(f"Question : {question_text}")
            response = input("Votre réponse : ")

            # Enregistrer la réponse dans la catégorie appropriée
            self.responses[category] = response

            self.context += f"\nQuestion : {question_text}\nRéponse : {response}"
            self.question_count += 1

        print("Merci d'avoir répondu à toutes les questions nécessaires.")

    def get_ordered_responses(self):
        # Ordre cohérent des catégories
        ordered_categories = ["budget", "location", "equipments", "activities", "hotel_category", "number_of_rooms"]
        ordered_responses = {}

        for category in ordered_categories:
            if self.responses[category]:
                ordered_responses[category] = self.responses[category]
        
        return ordered_responses