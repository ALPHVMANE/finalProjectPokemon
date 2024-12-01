# pokemon_api.py
import requests


class PokemonAPI:
    def __init__(self):
        self.base_url = 'https://pokeapi.co/api/v2/pokemon/'
        self.sprite_url = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/'
        # Dictionary of available Pokemon with their IDs
        self.available_pokemon = {
            'pikachu': 25,
            'charizard': 6,
            'venusaur': 3,
            'blastoise': 9,
            'mewtwo': 150,
            'gengar': 94
        }
        self.selected_pokemon = []

    def get_pokemon_data(self, pokemon_name):
        """Fetch Pokemon data and sprite"""
        pokemon_name = pokemon_name.lower()

        if pokemon_name not in self.available_pokemon:
            return {'success': False}

        pokemon_id = self.available_pokemon[pokemon_name]
        sprite_url = f"{self.sprite_url}{pokemon_id}.png"

        # Get sprite image
        response = requests.get(sprite_url)

        if response.status_code == 200:
            return {
                'name': pokemon_name.capitalize(),
                'image_url': sprite_url,
                'id': pokemon_id,
                'success': True
            }
        return {'success': False}

    def get_all_available_pokemon(self):
        """Get data for all available Pokemon"""
        pokemon_list = []
        for pokemon_name in self.available_pokemon.keys():
            data = self.get_pokemon_data(pokemon_name)
            if data['success']:
                pokemon_list.append(data)
        return pokemon_list