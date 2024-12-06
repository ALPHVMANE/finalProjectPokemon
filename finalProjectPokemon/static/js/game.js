// game.js
export class Game {
    constructor() {
        this.currentPlayer = 1;
        this.currentTurn = 1;
        this.gameOver = false;
        this.initializeEventListeners();
        this.updateBattleState();
    }

    initializeEventListeners() {
        // Move buttons
        document.querySelectorAll('.move-button').forEach(button => {
            button.addEventListener('click', (e) => {
                if (!this.gameOver) {
                    const moveIndex = parseInt(e.target.dataset.moveIndex);
                    this.executeMove(moveIndex);
                }
            });
        });

        // Switch buttons
        document.querySelectorAll('.switch-button').forEach(button => {
            button.addEventListener('click', (e) => {
                if (!this.gameOver) {
                    const pokemonIndex = parseInt(e.target.dataset.pokemonIndex);
                    this.executePokemonSwitch(pokemonIndex);
                }
            });
        });
    }

    async executeMove(moveIndex) {
        try {
            const response = await fetch('/battle/move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    player: this.currentPlayer,
                    action_type: 'move',
                    move_index: moveIndex
                })
            });

            const result = await response.json();
            if (result.success) {
                this.updateGameState(result);
                this.switchTurn();
            } else {
                this.showMessage(result.message);
            }
        } catch (error) {
            console.error('Error executing move:', error);
        }
    }

    async executePokemonSwitch(pokemonIndex) {
        try {
            const response = await fetch('/battle/move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    player: this.currentPlayer,
                    action_type: 'switch',
                    action_index: pokemonIndex
                })
            });

            const result = await response.json();
            if (result.success) {
                this.updateGameState(result);
                this.switchTurn();
            } else {
                this.showMessage(result.message);
            }
        } catch (error) {
            console.error('Error switching Pokemon:', error);
        }
    }

    async updateBattleState() {
        try {
            const response = await fetch('/battle/state');
            const state = await response.json();
            this.updateGameState(state);
        } catch (error) {
            console.error('Error updating battle state:', error);
        }
    }

    updateGameState(state) {
        // Update battle log
        const battleLog = document.getElementById('battleLog');
        battleLog.innerHTML = state.battle_log.map(log => `<p>${log}</p>`).join('');
        battleLog.scrollTop = battleLog.scrollHeight;

        // Update Pokemon HP and status
        this.updatePokemonStats('p1', state.player1_pokemon);
        this.updatePokemonStats('p2', state.player2_pokemon);

        // Update game state
        this.gameOver = state.game_over;
        this.currentTurn = state.current_turn;

        // Update UI based on game state
        this.updateUIState();
    }

    updatePokemonStats(playerPrefix, pokemonList) {
        pokemonList.forEach((pokemon, index) => {
            const pokemonId = `${playerPrefix}-pokemon${index + 1}`;
            const hpPercentage = (pokemon.current_hp / pokemon.max_hp) * 100;
            
            // Update HP bar
            const hpFill = document.getElementById(`${pokemonId}-hp-fill`);
            if (hpFill) {
                hpFill.style.width = `${hpPercentage}%`;
                hpFill.style.backgroundColor = this.getHPColor(hpPercentage);
            }

            // Update HP text
            const currentHPElement = document.getElementById(`${pokemonId}-current-hp`);
            const maxHPElement = document.getElementById(`${pokemonId}-max-hp`);
            if (currentHPElement) currentHPElement.textContent = pokemon.current_hp;
            if (maxHPElement) maxHPElement.textContent = pokemon.max_hp;

            // Update Pokemon card status
            const pokemonCard = document.querySelector(`.${pokemonId}`);
            if (pokemonCard) {
                pokemonCard.dataset.status = pokemon.is_fainted ? 'fainted' : 
                    (pokemon === this.activePokemon ? 'active' : 'waiting');
            }
        });
    }

    getHPColor(percentage) {
        if (percentage > 50) return '#00ff00';
        if (percentage > 25) return '#ffff00';
        return '#ff0000';
    }

    updateUIState() {
        const moveButtons = document.querySelectorAll('.move-button');
        const switchButtons = document.querySelectorAll('.switch-button');
        
        // Enable/disable controls based on current player
        const isCurrentPlayer = this.currentPlayer === 1;
        moveButtons.forEach(button => button.disabled = !isCurrentPlayer || this.gameOver);
        switchButtons.forEach(button => button.disabled = !isCurrentPlayer || this.gameOver);

        // Show game over message if applicable
        if (this.gameOver) {
            this.showMessage('Game Over!');
        }
    }

    switchTurn() {
        this.currentPlayer = this.currentPlayer === 1 ? 2 : 1;
        if (this.currentPlayer === 2) {
            // Simulate AI move for player 2
            setTimeout(() => this.executeAIMove(), 1000);
        }
    }

    executeAIMove() {
        // Simple AI: randomly choose between available moves
        const availableMoves = document.querySelectorAll('.move-button').length;
        const randomMoveIndex = Math.floor(Math.random() * availableMoves);
        this.executeMove(randomMoveIndex);
    }

    showMessage(message) {
        const battleLog = document.getElementById('battleLog');
        battleLog.innerHTML += `<p class="battle-message">${message}</p>`;
        battleLog.scrollTop = battleLog.scrollHeight;
    }
}