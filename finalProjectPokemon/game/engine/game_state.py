from finalProjectPokemon.game.Pokemon.poke_db import pokemon_stats
from finalProjectPokemon.game.Pokemon.pokemon_battle import Pokemon, Move
from finalProjectPokemon.game.Pokemon.pokemon_api import PokemonAPI


class GameState:
    def __init__(self):
        self.player1_pokemon = []
        self.player2_pokemon = []
        self.current_turn = 1
        self.battle_log = []
        self.game_over = False
        self.active_pokemon = {"player1": None, "player2": None}
        self._initialize_moves()
        self.pokemon_api = PokemonAPI()

    def _initialize_moves(self):
        """Initialize available moves for each Pokemon"""
        self.available_moves = {
            'raichu': [
                Move('Thunderbolt', 90, 100),
                Move('Iron Tail', 100, 75),
                Move('Quick Attack', 40, 100),
                Move('Thunder Wave', 0, 90)
            ],
            'charizard': [
                Move('Flamethrower', 90, 100),
                Move('Dragon Claw', 80, 100),
                Move('Air Slash', 75, 95),
                Move('Fire Blast', 110, 85)
            ],
            'venusaur': [
                Move('Solar Beam', 120, 100),
                Move('Sludge Bomb', 90, 100),
                Move('Razor Leaf', 55, 95),
                Move('Sleep Powder', 0, 75)
            ],
            'blastoise': [
                Move('Hydro Pump', 110, 80),
                Move('Ice Beam', 90, 100),
                Move('Skull Bash', 130, 100),
                Move('Water Pulse', 60, 100)
            ],
            'mewtwo': [
                Move('Psychic', 90, 100),
                Move('Shadow Ball', 80, 100),
                Move('Aura Sphere', 80, 100),
                Move('Ice Beam', 90, 100)
            ],
            'gengar': [
                Move('Shadow Ball', 80, 100),
                Move('Sludge Bomb', 90, 100),
                Move('Dream Eater', 100, 100),
                Move('Hex', 65, 100)
            ]
        }

    def _get_pokemon_stats(self, name):
        """Get Pokemon stats from pokemon_stats tuple"""
        name = name.lower()
        for stats in pokemon_stats:
            if stats[1].lower() == name:
                return {
                    'id': stats[0],
                    'name': stats[1],
                    'hp': stats[2],
                    'attack': stats[3],
                    'defense': stats[4],
                    'sp_attack': stats[5],
                    'speed': stats[6],
                    'type': stats[7]
                }
        return None

    def initialize_battle(self, player1_pokemon, player2_pokemon):
        """Initialize battle with selected Pokemon"""
        self.player1_pokemon = []
        self.player2_pokemon = []

        # Initialize Player 1's Pokemon
        for pokemon_data in player1_pokemon:
            stats = self._get_pokemon_stats(pokemon_data['name'])
            if stats:
                pokemon = Pokemon(
                    stats['name'],
                    stats['hp'],
                    stats['attack'],
                    stats['defense'],
                    stats['speed'],
                    self.available_moves[stats['name'].lower()]
                )
                self.player1_pokemon.append(pokemon)

        # Initialize Player 2's Pokemon
        for pokemon_data in player2_pokemon:
            stats = self._get_pokemon_stats(pokemon_data['name'])
            if stats:
                pokemon = Pokemon(
                    stats['name'],
                    stats['hp'],
                    stats['attack'],
                    stats['defense'],
                    stats['speed'],
                    self.available_moves[stats['name'].lower()]
                )
                self.player2_pokemon.append(pokemon)

        # Set active Pokemon
        if self.player1_pokemon and self.player2_pokemon:
            self.active_pokemon["player1"] = self.player1_pokemon[0]
            self.active_pokemon["player2"] = self.player2_pokemon[0]
            self.battle_log.append("Battle started!")
            self.battle_log.append(
                f"Player 1's {self.active_pokemon['player1'].name} vs Player 2's {self.active_pokemon['player2'].name}")
        else:
            raise ValueError("Both players must have at least one Pokemon")

    def execute_turn(self, player, action_type, action_index):
        if self.game_over:
            return {'success': False, 'message': 'Game is already over!'}

        attacker_key = "player1" if player == 1 else "player2"
        defender_key = "player2" if player == 1 else "player1"

        if action_type == 'switch':
            return self._execute_switch(player, action_index)
        elif action_type == 'move':
            return self._execute_move(attacker_key, defender_key, action_index)
        else:
            return {'success': False, 'message': 'Invalid action type!'}

    def _execute_move(self, attacker_key, defender_key, move_index):
        """Execute a move action"""
        attacker = self.active_pokemon[attacker_key]
        defender = self.active_pokemon[defender_key]

        if not attacker or not defender:
            return {'success': False, 'message': 'Invalid battle state!'}

        if move_index >= len(attacker.moves):
            return {'success': False, 'message': 'Invalid move index!'}

        move = attacker.moves[move_index]
        result = attacker.use_move(move, defender)

        if result['success']:
            self.battle_log.append(result['message'])
            self.current_turn += 1

            if defender.is_fainted:
                self.battle_log.append(f"{defender.name} fainted!")
                self._handle_fainted_pokemon(2 if attacker_key == "player1" else 1)

        return {
            'success': True,
            'battle_log': self.battle_log,
            'game_over': self.game_over,
            'damage_dealt': result.get('damage', 0),
            'target_hp': result.get('target_remaining_hp', 0)
        }

    def _execute_switch(self, player, pokemon_index):
        """Execute a switch action"""
        pokemon_list = self.player1_pokemon if player == 1 else self.player2_pokemon
        player_key = f"player{player}"

        # Validate switch
        if pokemon_index >= len(pokemon_list):
            return {'success': False, 'message': 'Invalid Pokemon index!'}

        new_pokemon = pokemon_list[pokemon_index]

        if new_pokemon.is_fainted:
            return {'success': False, 'message': f'{new_pokemon.name} has fainted and cannot battle!'}

        if new_pokemon == self.active_pokemon[player_key]:
            return {'success': False, 'message': f'{new_pokemon.name} is already in battle!'}

        # Perform switch
        old_pokemon = self.active_pokemon[player_key]
        self.active_pokemon[player_key] = new_pokemon

        # Reorder Pokemon list to maintain consistency
        pokemon_list.remove(new_pokemon)
        if old_pokemon in pokemon_list:
            pokemon_list.remove(old_pokemon)
        pokemon_list.insert(0, new_pokemon)
        if not old_pokemon.is_fainted:
            pokemon_list.append(old_pokemon)

        self.battle_log.append(f"Player {player} withdrew {old_pokemon.name} and sent out {new_pokemon.name}!")
        self.current_turn += 1

        return {
            'success': True,
            'battle_log': self.battle_log,
            'game_over': self.game_over,
            'switched_from': old_pokemon.name,
            'switched_to': new_pokemon.name
        }

    def _handle_fainted_pokemon(self, player):
        player_key = f"player{player}"
        pokemon_list = self.player1_pokemon if player == 1 else self.player2_pokemon

        # Remove fainted Pokemon
        pokemon_list.pop(0)

        if not pokemon_list:
            winner = 2 if player == 1 else 1
            self.battle_log.append(f"Player {winner} wins the battle!")
            self.game_over = True
            self.active_pokemon[player_key] = None
        else:
            # Switch to next Pokemon
            next_pokemon = pokemon_list[0]
            self.active_pokemon[player_key] = next_pokemon
            self.battle_log.append(f"Player {player} sends out {next_pokemon.name}!")

    def get_available_switches(self, player):
        pokemon_list = self.player1_pokemon if player == 1 else self.player2_pokemon
        active_pokemon = self.active_pokemon[f"player{player}"]

        return [
            {
                'index': idx,
                'name': pokemon.name,
                'current_hp': pokemon.current_hp,
                'max_hp': pokemon.max_hp
            }
            for idx, pokemon in enumerate(pokemon_list)
            if not pokemon.is_fainted and pokemon != active_pokemon
        ]

    def get_current_state(self):
        """Get current battle state"""
        return {
            'player1_pokemon': [
                {
                    'name': p.name,
                    'current_hp': p.current_hp,
                    'max_hp': p.max_hp,
                    'moves': [m.__dict__ for m in p.moves],
                    'img_url': self.pokemon_api.get_pokemon_data(p.name)['image_url']
                } for p in self.player1_pokemon
            ],
            'player2_pokemon': [
                {
                    'name': p.name,
                    'current_hp': p.current_hp,
                    'max_hp': p.max_hp,
                    'moves': [m.__dict__ for m in p.moves],
                    'img_url': self.pokemon_api.get_pokemon_data(p.name)['image_url']
                } for p in self.player2_pokemon
            ],
            'current_turn': self.current_turn,
            'battle_log': self.battle_log,
            'game_over': self.game_over,
            'active_pokemon': {
                'player1': self.active_pokemon['player1'].name if self.active_pokemon['player1'] else None,
                'player2': self.active_pokemon['player2'].name if self.active_pokemon['player2'] else None
            }
        }