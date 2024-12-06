from flask import Flask, render_template, request, redirect, url_for, jsonify
from game.Pokemon.pokemon_api import PokemonAPI
from game.engine.game_state import GameState
import os
from game.Pokemon.poke_db import get_db_conn, init_db

app = Flask(__name__)
pokemon_api = PokemonAPI()
game_states = {}  # Dictionary to store game states for different trainer pairs


@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('select_pokemon', player=1))


@app.route('/select/<int:player>', methods=['GET', 'POST'])
def select_pokemon(player):
    if player not in [1, 2]:
        return redirect(url_for('select_pokemon', player=1))

    if request.method == 'POST':
        selected = request.form.getlist('pokemon_selection')
        if len(selected) != 3:
            return render_template('select_pokemon.html',
                                   pokemon_list=pokemon_api.get_all_available_pokemon(),
                                   player=player,
                                   error="Please select exactly 3 Pokemon!")

        # Store selections in database
        conn = get_db_conn()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO trainer_pokemon 
            (trainer_id, pokemon1, pokemon2, pokemon3)
            VALUES (?, ?, ?, ?)
        ''', (player, selected[0], selected[1], selected[2]))

        conn.commit()
        conn.close()

        if player == 1:
            return redirect(url_for('select_pokemon', player=2))
        else:
            return redirect(url_for('display_battle'))

    return render_template('select_pokemon.html',
                           pokemon_list=pokemon_api.get_all_available_pokemon(),
                           player=player)


@app.route('/battle')
def display_battle():
    conn = get_db_conn()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM trainer_pokemon WHERE trainer_id IN (1, 2)')
    pokemon_rows = cursor.fetchall()
    conn.close()

    if len(pokemon_rows) != 2:
        return redirect(url_for('select_pokemon', player=1))

    players_pokemon = {}
    for row in pokemon_rows:
        player_pokemon = []
        for pokemon_name in [row['pokemon1'], row['pokemon2'], row['pokemon3']]:
            pokemon_data = pokemon_api.get_pokemon_data(pokemon_name)
            if pokemon_data['success']:
                player_pokemon.append(pokemon_data)
        players_pokemon[row['trainer_id']] = player_pokemon

    game_id = 'trainer_1_2'
    if game_id not in game_states:
        game_states[game_id] = GameState()
        game_states[game_id].initialize_battle(players_pokemon[1], players_pokemon[2])

    battle_state = game_states[game_id].get_current_state()

    print("\n=== DEBUG INFO ===")
    print("Battle State:", battle_state)
    print("\nPlayer 1 Pokemon Details:")
    for pokemon in battle_state['player1_pokemon']:
        print(f"Pokemon: {pokemon}")
    print("==================\n")

    return render_template('battle.html',
                           player1_pokemon=battle_state['player1_pokemon'],
                           player2_pokemon=battle_state['player2_pokemon'],
                           battle_log=battle_state['battle_log'],
                           current_turn=battle_state['current_turn'])


@app.route('/battle/move', methods=['POST'])
def execute_move():
    game_id = 'trainer_1_2'
    battle_state = game_states[game_id].get_current_state()

    if game_id not in game_states:
        return jsonify({'success': False, 'message': 'Invalid game state'})

    data = request.get_json()
    player = data.get('player')
    action_type = data.get('action_type')
    action_index = data.get('action_index')

    params_valid = all([player, action_type, action_index is not None])
    if not params_valid:
        return jsonify({'success': False, 'message': 'Invalid request parameters'})

    game_state = game_states[game_id]
    current_turn = game_state.current_turn

    if (current_turn % 2 == 1 and player != 1) or (current_turn % 2 == 0 and player != 2):
        return jsonify({'success': False, 'message': 'Not your turn'})

    result = game_state.execute_turn(player, action_type, action_index)
    if not result['success']:
        return jsonify(result)

    battle_state = game_state.get_current_state()

    if battle_state['game_over']:
        game_states.pop(game_id, None)

    return jsonify({
        'success': True,
        'player1_pokemon': battle_state['player1_pokemon'],
        'player2_pokemon': battle_state['player2_pokemon'],
        'battle_log': battle_state['battle_log'],
        'current_turn': battle_state['current_turn'],
        'game_over': battle_state['game_over']
    })


@app.route('/battle/state')
def get_battle_state():
    game_id = 'trainer_1_2'
    if game_id not in game_states:
        return jsonify({'success': False, 'message': 'Invalid game state'})

    battle_state = game_states[game_id].get_current_state()
    return jsonify({
        'success': True,
        **battle_state
    })


@app.route('/battle/reset', methods=['POST'])
def reset_battle():
    game_id = 'trainer_1_2'
    game_states.pop(game_id, None)

    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM trainer_pokemon WHERE trainer_id IN (1, 2)')
    conn.commit()
    conn.close()

    return redirect(url_for('home'))


if __name__ == '__main__':
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    app.template_folder = template_dir
    init_db()
    app.run(debug=True)