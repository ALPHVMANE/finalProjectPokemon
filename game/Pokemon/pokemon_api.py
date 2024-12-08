# pokemon_api.py
import requests


class PokemonAPI:
    def __init__(self):
        self.base_url = 'https://pokeapi.co/api/v2/pokemon/'
        self.sprite_url = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/'
        #Dict
        self.available_pokemon = {
            'raichu': 26,
            'charizard': 6,
            'venusaur': 3,
            'blastoise': 9,
            'mewtwo': 150,
            'gengar': 94
        }
        #List
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

#DEMO AREA
if __name__ == '__main__':
    pokemon_api = PokemonAPI()

    print("\n--- Single Pokemon ---")
    raichu_data = pokemon_api.get_pokemon_data('raichu')
    print(f"Raichu data: {raichu_data}")

    print("\n--- Invalid Pokemon ---")
    invalid_data = pokemon_api.get_pokemon_data('pikachu')
    print(f"Invalid Pokemon data: {invalid_data}")

    print("\n--- All Available Pokemon ---")
    all_pokemon = pokemon_api.get_all_available_pokemon()
    print("Available Pokemon:")
    for pokemon in all_pokemon:
        print(f"- {pokemon['name']} (ID: {pokemon['id']}, Sprite: {pokemon['image_url']})")