import streamlit as st
from backend import PokeAPI
import random
import asyncio

# Créer une instance de la classe PokeAPI
poke_api = PokeAPI()

def display_pokemon_stats():
    st.header('Obtenir les statistiques de ton Pokémon')
    name = st.text_input('Entre le nom ou l\'ID de ton Pokémon : ')
    if st.button("Obtenir les statistiques"):
        stats = poke_api.fetch_pokemon_stats(name)
        if stats:
            st.success(f"Statistiques de {stats['name']}:")
            st.write(f"Points de vie (HP): {stats['hp']}")
            st.write(f"Attaque: {stats['attack']}")
            st.write(f"Défense: {stats['defense']}")
            st.write(f"Attaque spéciale: {stats['special_attack']}")
            st.write(f"Défense spéciale: {stats['special_defense']}")
            st.write(f"Vitesse: {stats['speed']}")
            st.write(f"Types: {', '.join(stats['types'])}")
        else:
            st.error("Pokémon non trouvé.")

def compare_pokemons():
    st.header('Comparer deux Pokémon')
    pokemon_1 = st.text_input('Entre le nom ou l\'ID de ton premier Pokémon : ')
    pokemon_2 = st.text_input('Entre le nom ou l\'ID de ton deuxième Pokémon : ')
    if st.button('Comparer'):
        stats_pokemon_1, stats_pokemon_2, comparison = poke_api.compare_pokemons(pokemon_1, pokemon_2)
        if stats_pokemon_1 and stats_pokemon_2:
            st.success(f"Comparaison entre {stats_pokemon_1['name']} et {stats_pokemon_2['name']}:")
            st.write(f"{stats_pokemon_1['name']} a {stats_pokemon_1['hp']} HP et {stats_pokemon_1['attack']} d'attaque.")
            st.write(f"{stats_pokemon_2['name']} a {stats_pokemon_2['hp']} HP et {stats_pokemon_2['attack']} d'attaque.")
            if comparison['hp'] > 0:
                st.write(f"{stats_pokemon_1['name']} a plus de points de vie.")
            elif comparison['hp'] < 0:
                st.write(f"{stats_pokemon_2['name']} a plus de points de vie.")
            else:
                st.write("Les deux Pokémon ont le même nombre de points de vie.")
            if comparison['attack'] > 0:
                st.write(f"{stats_pokemon_1['name']} a plus d'attaque.")
            elif comparison['attack'] < 0:
                st.write(f"{stats_pokemon_2['name']} a plus d'attaque.")
            else:
                st.write("Les deux Pokémon ont la même attaque.")
        else:
            st.error("Un ou deux Pokémon non trouvés.")

def display_type_stats():
    st.header("Obtenir des statistiques sur un type de Pokémon")
    
    # Récupérer les types disponibles
    types = poke_api.get_all_types()
    
    # Menu déroulant pour sélectionner un type
    selected_type = st.selectbox("Sélectionnez un type de Pokémon :", types)

    if st.button("Obtenir les statistiques du type"):
        pokemon_count, average_hp = poke_api.get_type_hp(selected_type)
        if pokemon_count > 0:
            st.success(f"Le type principal sélectionné est {selected_type}.")
            st.write(f"Il y a {pokemon_count} Pokémon de type {selected_type}.")
            st.write(f"La moyenne des points de vie (HP) pour ce type est de {average_hp:.2f}.")
        else:
            st.error("Aucun Pokémon trouvé pour ce type.")

def simulate_requests():
    st.header("Simulation de Requêtes vers l'API Pokémon")
    st.write("Cette application simule un grand nombre de requêtes vers l'API Pokémon.")

    # Entrée utilisateur pour le nombre de requêtes
    num_requests = st.number_input("Nombre de requêtes à simuler :", min_value=1, max_value=100000, value=700, step=100)
    
    # Option pour afficher un résumé des appels et des réponses
    display_summary = st.checkbox("Afficher un résumé des appels et des réponses")

    if st.button("Lancer la simulation"):
        st.write("Simulation en cours...")
        successful_requests = []
        urls = []

        # Générer les URLs pour les requêtes
        for _ in range(num_requests):
            url = f"https://pokeapi.co/api/v2/pokemon/{random.randint(1, 1000)}"
            urls.append(url)

        # Appel asynchrone pour récupérer les données
        results = asyncio.run(poke_api.fetch_all_data(urls))

        for result, url in zip(results, urls):
            if result:
                response_code = 200  # Simuler un code de succès
                successful_requests.append((url, result, response_code))
            else:
                response_code = 500  # Simuler une erreur
                successful_requests.append((url, {"error": "Erreur ou réponse vide."}, response_code))

        # Afficher le nombre de requêtes réussies
        st.write(f"Nombre de requêtes réussies : {len(successful_requests)} sur {num_requests}.")

        # Affichage du résumé si l'option est sélectionnée
        if display_summary:
            st.subheader("Résumé des appels et des réponses")
            for url, response, code in successful_requests:
                st.write(f"**URL :** {url}")
                st.write(f"**Code retour :** {code}")
                if "error" in response:
                    st.write(f"**Réponse :** {response['error']}")
                else:
                    st.write(f"**Réponse :** {response.get('name', 'Inconnu')}")
                st.write("---")  # Ligne de séparation entre les résumés

def simulate_battle():
    st.header("Simuler un combat entre deux Pokémon")
    pokemon_1 = st.text_input('Entre le nom ou l\'ID du premier Pokémon : ')
    pokemon_2 = st.text_input('Entre le nom ou l\'ID du deuxième Pokémon : ')
    if st.button("Lancer le combat"):
        stats_pokemon_1, stats_pokemon_2, winner, total_damage_1, total_damage_2 = poke_api.simulate_battle(pokemon_1, pokemon_2)
        if stats_pokemon_1 and stats_pokemon_2:
            st.success(f"Combat entre {stats_pokemon_1['name']} et {stats_pokemon_2['name']}")
            st.write(f"**{stats_pokemon_1['name']}**:")
            st.write(f"Points de vie (HP): {stats_pokemon_1['hp']}")
            st.write(f"Attaque: {stats_pokemon_1['attack']}")
            st.write(f"Défense: {stats_pokemon_1['defense']}")
            st.write(f"Attaque spéciale: {stats_pokemon_1['special_attack']}")
            st.write(f"Défense spéciale: {stats_pokemon_1['special_defense']}")
            st.write(f"Total des dégâts infligés sur 5 tours: {total_damage_1}")
            st.write("---")
            st.write(f"**{stats_pokemon_2['name']}**:")
            st.write(f"Points de vie (HP): {stats_pokemon_2['hp']}")
            st.write(f"Attaque: {stats_pokemon_2['attack']}")
            st.write(f"Défense: {stats_pokemon_2['defense']}")
            st.write(f"Attaque spéciale: {stats_pokemon_2['special_attack']}")
            st.write(f"Défense spéciale: {stats_pokemon_2['special_defense']}")
            st.write(f"Total des dégâts infligés sur 5 tours: {total_damage_2}")
            st.write("---")
            st.write(f"Le gagnant est : {winner}")
        else:
            st.error("Erreur : l'un des Pokémon n'a pas pu être trouvé.")

# Fonction principale
def main():
    st.title('PokéAPI - Informations sur vos Pokémon.')

    # Initialiser l'état de la session
    if 'current_section' not in st.session_state:
        st.session_state.current_section = "home"

    # Sections cliquables à gauche
    st.sidebar.header("Sections")
    if st.sidebar.button("Obtenir les statistiques d'un Pokémon"):
        st.session_state.current_section = "pokemon_stats"
    if st.sidebar.button("Comparer deux Pokémon"):
        st.session_state.current_section = "compare"
    if st.sidebar.button("Obtenir des statistiques sur un type de Pokémon"):
        st.session_state.current_section = "type_stats"
    if st.sidebar.button("Simulation de requêtes vers l'API Pokémon"):
        st.session_state.current_section = "simulate_requests"
    if st.sidebar.button("Simuler un combat entre deux Pokémon"):
        st.session_state.current_section = "simulate_battle"

    # Affichage de la section sélectionnée
    if st.session_state.current_section == "pokemon_stats":
        display_pokemon_stats()
    elif st.session_state.current_section == "compare":
        compare_pokemons()
    elif st.session_state.current_section == "type_stats":
        display_type_stats()  # Appel de la fonction pour afficher les stats par type
    elif st.session_state.current_section == "simulate_requests":
        simulate_requests()
    elif st.session_state.current_section == "simulate_battle":
        simulate_battle()
    else:
        st.write("Sélectionnez une fonctionnalité dans le menu à gauche.")

if __name__ == "__main__":
    main()