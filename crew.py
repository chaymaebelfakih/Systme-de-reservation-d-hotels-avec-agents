from crewai import Crew,Process
from tasks import research_task,write_task
from agents import news_researcher,news_writer
from agents import AgentClient
from agents import AgentNegotiation
from agents import AgentHotel
## Forming the tech focused crew with some enhanced configuration
crew=Crew(
    agents=[news_researcher,news_writer],
    tasks=[research_task,write_task],
    process=Process.sequential,

)

## starting the task execution process wiht enhanced feedback

result=crew.kickoff(inputs={'topic':'AI in healthcare'})
print(result)
if __name__ == "__main__":
    # Initialiser les agents
    client_agent = AgentClient()
    negotiation_agent = AgentNegotiation()
    hotel_agent = AgentHotel()

    # Étape 1 : Le client exprime ses besoins
    user_profile = client_agent.ask_user_questions()

    # Étape 2 : L'Agent Client recommande des offres
    recommendations = client_agent.send_recommendations()

    # Étape 3 : L'utilisateur choisit une offre (simulé ici)
    user_choice = recommendations[0]  # Par exemple, le premier choix
    print(f"L'utilisateur a choisi : {user_choice}")

    # Étape 4 : L'Agent de Négociation négocie avec l'Agent Hôtel
    final_offer = negotiation_agent.negotiate_with_hotel(user_choice, hotel_agent)

    # Étape 5 : Réservation finalisée
    print(f"Réservation finalisée avec l'offre : {final_offer}")
