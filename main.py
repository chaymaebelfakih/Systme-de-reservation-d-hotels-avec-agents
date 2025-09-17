from AgentClient import AgentClient
from NegotiatorAgent import AgentNegociateur
from HotelAgent import AgentHotel
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv


# Charger la clé API Google
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
# Étape 1 : L'Agent Client pose des questions
client_agent.ask_questions(max_questions=6)
client_data = client_agent.get_ordered_responses()

# Convertir les données client
budget = float(client_data.get("budget", 0))  # Budget par défaut 0
preferences = {
    "location": client_data.get("location", ""),
    "activities": client_data.get("activities", ""),
    "equipments": client_data.get("equipments", ""),
    "hotel_category": client_data.get("hotel_category", ""),
    "rooms_needed": int(client_data.get("number_of_rooms", 1))  # Par défaut 1 chambre
}

# Passer les données au négociateur
negotiator_agent.set_client_data(
    budget,
    preferences["location"],
    preferences["activities"],
    preferences["equipments"],
    preferences["hotel_category"],
    preferences["rooms_needed"]
)

# Étape 2 : Négociation entre les agents (affichage dynamique)
best_offer = negotiator_agent.negotiate_with_hotel(hotel_agent)

# Étape 3 : Afficher l'offre finale
def display_best_offer(best_offer):
    if best_offer:
        print(colored(f"\n🎉 *Offre Finale Sélectionnée* 🎉", 'green'))
        print(colored(f"\n🏨 *Nom de l'hôtel* : {best_offer['name']}", 'cyan'))
        print(colored(f"📍 *Lieu* : {best_offer['location']}", 'yellow'))
        print(colored(f"💰 *Prix par nuit* : {best_offer['price_per_night']} €", 'magenta'))
        print(colored(f"⭐ *Évaluation* : {best_offer['rating']} / 5", 'blue'))
        print(colored(f"📦 *Équipements* : {', '.join(best_offer['features'])}", 'green'))
        print(colored(f"📅 *Disponibilité* : {'Disponible' if best_offer['availability'] else 'Non disponible'}", 'red'))
        # Demander à l'utilisateur s'il accepte l'offre ajustée
        user_decision = input("\nAcceptez-vous cette offre ajustée ? (oui/non) : ").strip().lower()

        if user_decision == "oui":
          print("\n👍 Offre acceptée ! Votre réservation est en cours.")
          return best_offer  # L'offre est acceptée et retournée
        else:
          print("\n❌ Offre rejetée. Nous allons essayer de trouver une autre solution.")
        # Ici, vous pouvez décider de recommencer l'ajustement ou d'offrir une nouvelle offre.
        return None
    else:
        print(colored("\nAucune offre n'a pu être négociée.", 'red'))

display_best_offer(best_offer)

