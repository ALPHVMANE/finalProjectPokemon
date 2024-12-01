from flask import Flask, render_template, request, redirect, url_for, session
from game.Pokemon.pokemon_api import PokemonAPI
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required for session management
pokemon_api = PokemonAPI()


@app.route('/', methods=['GET', 'POST'])
def select_pokemon():
    if request.method == 'POST':
        selected = request.form.getlist('pokemon_selection')
        if len(selected) != 3:
            return render_template('select_pokemon.html',
                                   pokemon_list=pokemon_api.get_all_available_pokemon(),
                                   error="Please select exactly 3 Pokemon!")

        # Store selections in session
        session['selected_pokemon'] = selected
        return redirect(url_for('display_pokemon'))

    return render_template('select_pokemon.html',
                           pokemon_list=pokemon_api.get_all_available_pokemon())


@app.route('/display')
def display_pokemon():
    if 'selected_pokemon' not in session:
        return redirect(url_for('select_pokemon'))

    selected_pokemon = []
    for pokemon_name in session['selected_pokemon']:
        pokemon_data = pokemon_api.get_pokemon_data(pokemon_name)
        if pokemon_data['success']:
            selected_pokemon.append(pokemon_data)

    return render_template('display_pokemon.html', pokemon_list=selected_pokemon)


if __name__ == '__main__':
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    app.template_folder = template_dir
    app.run(debug=True)