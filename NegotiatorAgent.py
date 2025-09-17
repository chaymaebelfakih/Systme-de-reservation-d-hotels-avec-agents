class AgentNegociateur:
    def __init__(self):
        self.client_data = {}

    def set_client_data(self, budget, location, activities, equipments, hotel_category, rooms_needed):
        self.client_data['budget'] = budget
        self.client_data['location'] = location
        self.client_data['activities'] = activities
        self.client_data['equipments'] = equipments
        self.client_data['hotel_category'] = hotel_category
        self.client_data['rooms_needed'] = rooms_needed

    def find_exact_offer(self, hotel_agent):
        """Recherche une offre correspondant exactement aux critères de l'utilisateur."""
        preferences = {
            "location": self.client_data['location'],
            "activities": self.client_data['activities'],
            "equipments": self.client_data['equipments'],
            "hotel_category": self.client_data['hotel_category'],
            "rooms_needed": self.client_data['rooms_needed']
        }
        budget = self.client_data['budget']
        return hotel_agent.search_offers(preferences, budget)

    def propose_adjusted_offer(self, hotel_agent, initial_offers):
        """Propose une offre ajustée en fonction des préférences et du budget."""
        budget = self.client_data['budget']
        for offer in initial_offers:
            if offer["price_per_night"] > budget:
                # Ajuster l'offre
                print(f"[Agent Négociateur] Ajustement de l'offre : {offer['name']}")
                return hotel_agent.adjust_offer(offer, budget, self.client_data)
        return None

    def negotiate_with_hotel(self, hotel_agent):
     """Négocier avec l'Agent Hôtel pour ajuster l'offre en fonction des préférences."""
     preferences = {
        "location": self.client_data["location"],
        "activities": self.client_data["activities"],
        "equipments": self.client_data["equipments"],
        "hotel_category": self.client_data["hotel_category"],
        "rooms_needed": self.client_data["rooms_needed"]
    }
     budget = self.client_data["budget"]

    # Rechercher des offres correspondant aux préférences
     offers = hotel_agent.search_offers(preferences, budget)

     if not offers:
        print("[Agent Négociateur] Aucune correspondance exacte trouvée. Proposition d'une offre ajustée :")
        offers = hotel_agent.get_all_offers()

     if offers:
        # Négocier la meilleure offre
        best_offer = min(offers, key=lambda x: x["price_per_night"])
        if best_offer["price_per_night"] > budget:
            best_offer = hotel_agent.adjust_offer(best_offer, budget, self.client_data)
        return best_offer
     else:
        print("[Agent Négociateur] Aucune offre disponible.")
        return None