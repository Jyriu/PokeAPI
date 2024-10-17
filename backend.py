import requests
import time
import aiohttp
import asyncio
import requests_cache
import random


class PokeAPI:
    def __init__(self):
        self.base_url = 'https://pokeapi.co/api/v2'
        # initialisons le cache avec une expiration à 1h
        requests_cache.install_cache('pokeapi_cache', expire_after=3600)

    # On récupère les données avec error handling
    def fetch_data(self, url, retries=3, delay=2):
        """ Fonction pour récupérer des données depuis une URL avec gestion des erreurs courantes. """
        for attempt in range(retries):
            try:
                response = requests.get(url)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:  # Too Many Requests
                    print("Trop de requêtes. Attendez quelques instants.")
                    time.sleep(delay)
                elif response.status_code in [500, 503]:  # Internal Server Error / Service Unavailable
                    print("Erreur du serveur. Réessayez plus tard.")
                    time.sleep(delay)
                elif response.status_code == 400:  # Bad Request
                    print("Requête invalide.")
                    return None
                elif response.status_code == 401:  # Unauthorized
                    print("Non autorisé. Vérifiez vos identifiants.")
                    return None
                elif response.status_code == 403:  # Forbidden
                    print("Accès interdit.")
                    return None
                elif response.status_code == 404:  # Not Found
                    print("Ressource non trouvée.")
                    return None
                else:
                    print(f"Erreur HTTP : {e}")
                return None
            except requests.exceptions.RequestException as e:
                print(f"Erreur de connexion : {e}")
                return None
        print("Nombre maximum de tentatives atteint.")
        return None

    # Fonction pour récupérer les stats d'un Pokémon
    def fetch_pokemon_stats(self, name):
        url = f"{self.base_url}/pokemon/{name.lower()}"
        data = self.fetch_data(url)

        if data:
            # Vérifier si les clés existent
            stats = {
                "name": data.get('name', 'Inconnu').capitalize(),
                "hp": data['stats'][0].get('base_stat', 0),  # Valeur par défaut si la clé n'existe pas
                "attack": data['stats'][1].get('base_stat', 0),
                "defense": data['stats'][2].get('base_stat', 0),
                "special_attack": data['stats'][3].get('base_stat', 0),
                "special_defense": data['stats'][4].get('base_stat', 0),
                "speed": data['stats'][5].get('base_stat', 0),
                "types": [t['type']['name'] for t in data.get('types', [])]  # Assurez-vous que les types sont extraits correctement
            }
            return stats

        return None

    # Fonction pour comparer les stats de 2 Pokémon
    def compare_pokemons(self, pokemon_1, pokemon_2):
        stats_pokemon_1 = self.fetch_pokemon_stats(pokemon_1)
        stats_pokemon_2 = self.fetch_pokemon_stats(pokemon_2)

        if stats_pokemon_1 and stats_pokemon_2:
            comparison = {
                'hp': stats_pokemon_1['hp'] - stats_pokemon_2['hp'],
                'attack': stats_pokemon_1['attack'] - stats_pokemon_2['attack']
            }
            return stats_pokemon_1, stats_pokemon_2, comparison
        return None, None, None

    def get_all_types(self):
        """ Récupérer la liste de tous les types de Pokémon disponibles. """
        url = f"{self.base_url}/type"
        response = requests.get(url)
        response.raise_for_status()
        return [type_info['name'] for type_info in response.json()['results']]

    # Fonction pour récupérer le type d'un Pokémon puis tous les Pokémon de ce type et leurs HP moyens
    def get_type_hp(self, type_name):
        """ Récupérer le nombre de Pokémon d'un type donné et calculer la moyenne des HP. """
        url = f"{self.base_url}/type/{type_name}"
        type_data = requests.get(url).json()
        
        total_hp = 0
        pokemon_count = len(type_data['pokemon'])

        for poke in type_data['pokemon']:
            poke_data = requests.get(poke['pokemon']['url']).json()
            total_hp += poke_data['stats'][0]['base_stat']

        average_hp = total_hp / pokemon_count if pokemon_count > 0 else 0
        return pokemon_count, average_hp

    async def fetch_async_data(self, session, url, retries=3, delay=2):
        """ Fonction asynchrone pour récupérer des données avec gestion des erreurs. """
        for attempt in range(retries):
            try:
                async with session.get(url) as response:
                    response.raise_for_status()  # Vérifier les erreurs HTTP
                    return await response.json()
            except aiohttp.ClientResponseError as e:
                if e.status == 429:  # Trop de requêtes
                    print("Trop de requêtes. Attendez quelques instants.")
                    await asyncio.sleep(delay)
                elif e.status in [500, 503]:  # Erreurs du serveur
                    print("Erreur du serveur. Réessayez plus tard.")
                    await asyncio.sleep(delay)
                elif e.status == 400:  # Mauvaise requête
                    print("Requête invalide.")
                    return None
                elif e.status == 401:  # Non autorisé
                    print("Non autorisé. Vérifiez vos identifiants.")
                    return None
                elif e.status == 403:  # Accès interdit
                    print("Accès interdit.")
                    return None
                elif e.status == 404:  # Non trouvé
                    print("Ressource non trouvée.")
                    return None
                else:
                    print(f"Erreur HTTP : {e}")
                return None
            except Exception as e:
                print(f"Erreur de connexion : {e}")
                return None
        print("Nombre maximum de tentatives atteint.")
        return None

    async def fetch_all_data(self, urls):
        """ Fonction pour gérer des millions de requêtes de manière efficace. """
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_async_data(session, url) for url in urls]
            return await asyncio.gather(*tasks)

    def simulate_heavy_load(self, num_requests):
        """ Simule une charge élevée avec un nombre donné de requêtes vers des URLs différentes. """
        urls = [
            f"{self.base_url}/pokemon/{random.randint(1, 1000)}" for _ in range(num_requests)
        ]
        results = asyncio.run(self.fetch_all_data(urls))
        
        # Traitement des résultats (pour afficher ou logger)
        successful_requests = [result for result in results if result and 'error' not in result]
        # Toujours retourner le nombre de requêtes réussies et le total
        return len(successful_requests), num_requests

