# game/game_state.py

from game.Pokemon.pokemon_battle import Pokemon, Move


class GameState:
    def __init__(self):
        self.player1_pokemon = []
        self.player2_pokemon = []
        self.current_turn = 1
        self.battle_log = []
        self.game_over = False

        # Define available moves
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

    def initialize_battle(self, player1_pokemon, player2_pokemon):
        # Convert pokemon data into Pokemon objects with moves
        for pokemon_data in player1_pokemon:
            pokemon = Pokemon(
                pokemon_data['name'],
                100,  # Base HP
                80,  # Base Attack
                70,  # Base Defense
                70,  # Base Speed
                self.available_moves[pokemon_data['name'].lower()]
            )
            self.player1_pokemon.append(pokemon)

        for pokemon_data in player2_pokemon:
            pokemon = Pokemon(
                pokemon_data['name'],
                100,  # Base HP
                80,  # Base Attack
                70,  # Base Defense
                70,  # Base Speed
                self.available_moves[pokemon_data['name'].lower()]
            )
            self.player2_pokemon.append(pokemon)

        self.battle_log.append("Battle started!")
        self.battle_log.append(
            f"Player 1's {self.player1_pokemon[0].name} vs Player 2's {self.player2_pokemon[0].name}")

    def execute_turn(self, player, move_index):
        if self.game_over:
            return {'success': False, 'message': 'Game is already over!'}

        attacker = self.player1_pokemon[0] if player == 1 else self.player2_pokemon[0]
        defender = self.player2_pokemon[0] if player == 1 else self.player1_pokemon[0]

        if move_index >= len(attacker.moves):
            return {'success': False, 'message': 'Invalid move index!'}

        move = attacker.moves[move_index]
        result = attacker.use_move(move, defender)

        if result['success']:
            self.battle_log.append(result['message'])
            if defender.is_fainted:
                self.battle_log.append(f"{defender.name} fainted!")
                self._handle_fainted_pokemon(2 if player == 1 else 1)

        return {
            'success': True,
            'battle_log': self.battle_log,
            'game_over': self.game_over
        }

    def _handle_fainted_pokemon(self, player):
        pokemon_list = self.player1_pokemon if player == 1 else self.player2_pokemon

        # Remove fainted Pokemon
        pokemon_list.pop(0)

        if not pokemon_list:
            winner = 2 if player == 1 else 1
            self.battle_log.append(f"Player {winner} wins the battle!")
            self.game_over = True
        else:
            self.battle_log.append(f"Player {player} sends out {pokemon_list[0].name}!")

    def get_current_state(self):
        return {
            'player1_pokemon': [
                {
                    'name': p.name,
                    'current_hp': p.current_hp,
                    'max_hp': p.max_hp,
                    'moves': [m.__dict__ for m in p.moves]
                } for p in self.player1_pokemon
            ],
            'player2_pokemon': [
                {
                    'name': p.name,
                    'current_hp': p.current_hp,
                    'max_hp': p.max_hp,
                    'moves': [m.__dict__ for m in p.moves]
                } for p in self.player2_pokemon
            ],
            'current_turn': self.current_turn,
            'battle_log': self.battle_log,
            'game_over': self.game_over
        }