import tkinter as tk
from tkinter import messagebox
from AgentClient import AgentClient
from HotelAgent import AgentHotel
from NegotiatorAgent import AgentNegociateur
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# Charger la clé API
load_dotenv()
google_api_key = "AIzaSyDNWdevmyLrV9baBzb90p63Tg97OF57wHI"

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.5,
    google_api_key=google_api_key,
)

# Initialiser les agents
client_agent = AgentClient(llm)
negotiator_agent = AgentNegociateur()
hotel_agent = AgentHotel()

class HotelBookingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Système de réservation d'hôtel")

        # Création des champs pour l'utilisateur
        self.create_widgets()

    def create_widgets(self):
        # Zone de texte pour afficher les questions
        self.question_label = tk.Label(self.master, text="Chargement des questions...", wraplength=300)
        self.question_label.grid(row=0, column=0, columnspan=2)

        # Champ pour l'utilisateur de répondre à chaque question
        self.response_entry = tk.Entry(self.master)
        self.response_entry.grid(row=1, column=0, columnspan=2)

        # Bouton pour soumettre la réponse
        self.submit_button = tk.Button(self.master, text="Répondre", command=self.submit_response)
        self.submit_button.grid(row=2, column=0, columnspan=2)

        # Variable pour suivre l'étape des questions
        self.current_question_idx = 0
        self.client_responses = {}

    def submit_response(self):
        response = self.response_entry.get().strip()

        if response:
            # Sauvegarder la réponse
            if self.current_question_idx == 0:
                self.client_responses["budget"] = float(response)  # Budget est converti en float
            elif self.current_question_idx == 1:
                self.client_responses["location"] = response
            elif self.current_question_idx == 2:
                self.client_responses["activities"] = response.split(",")  # Activités séparées par des virgules
            elif self.current_question_idx == 3:
                self.client_responses["equipments"] = response.split(",")  # Équipements séparés par des virgules
            elif self.current_question_idx == 4:
                self.client_responses["rooms_needed"] = int(response)  # Nombre de chambres

            # Passer à la question suivante ou terminer
            self.current_question_idx += 1
            if self.current_question_idx < len(self.questions):
                self.display_next_question()
            else:
                # L'utilisateur a répondu à toutes les questions
                self.process_responses()

    def display_next_question(self):
        """Affiche la question suivante."""
        question = self.questions[self.current_question_idx]
        self.question_label.config(text=question)
        self.response_entry.delete(0, tk.END)

    def process_responses(self):
        """Traite les réponses une fois toutes les questions posées."""
        # Passer les données au négociateur
        negotiator_agent.set_client_data(
            self.client_responses["budget"], 
            self.client_responses["location"], 
            self.client_responses["activities"], 
            self.client_responses["equipments"], 
            "",  # catégorie d'hôtel optionnelle
            self.client_responses["rooms_needed"]
        )

        # Recherche des meilleures offres via l'agent négociateur
        best_offer = negotiator_agent.negotiate_with_hotel(hotel_agent)
        
        if best_offer:
            offers_str = "\n".join([f"Location: {offer['location']}, Prix: {offer['price_per_night']} €/nuit, Évaluation: {offer['rating']}" 
                                   for offer in best_offer])
            messagebox.showinfo("Offres disponibles", offers_str)
        else:
            messagebox.showerror("Erreur", "Aucune offre n'a pu être trouvée.")

    def start_interview(self):
        """Démarre l'interview avec LLM."""
        # Pose les questions via l'agent client
        self.questions = client_agent.ask_questions(max_questions=5)
        self.display_next_question()

# Initialiser l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = HotelBookingApp(root)

    # Démarrer l'interview avec LLM
    app.start_interview()

    root.mainloop()
