export class Game {
    constructor() {
        this.currentTurn = 1;
        this.gameOver = false;
        this.initialize();
    }

    initialize() {
        this.setupEventListeners();
        this.startBattleStatePolling();
    }

    setupEventListeners() {
        const moveButtons = document.querySelectorAll('.move-button');
        moveButtons.forEach(button => {
            button.addEventListener('click', (e) => this.handleMoveSelection(e));
        });
    }

    getCurrentPlayer() {
        return this.currentTurn % 2 === 1 ? 1 : 2;
    }

    async handleMoveSelection(event) {
        if (this.gameOver) return;

        const moveIndex = event.target.closest('.move-button').dataset.moveIndex;
        const currentPlayer = this.getCurrentPlayer();

        try {
            const response = await fetch('/battle/state');
            const stateResult = await response.json();

            if (!stateResult.success) {
                this.showMessage('Error getting battle state');
                return;
            }

            // Update current turn from server state
            this.currentTurn = stateResult.current_turn;

            // Check if it's the right player's turn
            if (this.getCurrentPlayer() !== currentPlayer) {
                this.showMessage("Not your turn!");
                return;
            }

            const moveResponse = await fetch('/battle/move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    player: currentPlayer,
                    action_type: 'move',
                    action_index: parseInt(moveIndex)
                })
            });

            const result = await moveResponse.json();

            if (result.success) {
                this.updateBattleState(result);
                location.reload(); // Reload to update the moves display
            } else {
                this.showMessage(result.message);
            }
        } catch (error) {
            console.error('Error executing move:', error);
            this.showMessage('An error occurred while executing the move.');
        }
    }

    updateBattleState(state) {
        // Update Pokemon HP and status
        ['player1_pokemon', 'player2_pokemon'].forEach((player, playerIndex) => {
            state[player].forEach((pokemon, index) => {
                const playerNum = playerIndex + 1;
                const hpFill = document.querySelector(`#p${playerNum}-pokemon${index + 1}-hp-fill`);
                const currentHpSpan = document.querySelector(`#p${playerNum}-pokemon${index + 1}-current-hp`);
                const maxHpSpan = document.querySelector(`#p${playerNum}-pokemon${index + 1}-max-hp`);

                if (hpFill && currentHpSpan && maxHpSpan) {
                    const hpPercentage = (pokemon.current_hp / pokemon.max_hp) * 100;
                    hpFill.style.width = `${hpPercentage}%`;
                    currentHpSpan.textContent = pokemon.current_hp;
                    maxHpSpan.textContent = pokemon.max_hp;
                }
            });
        });

        // Update battle log
        this.updateBattleLog(state.battle_log);

        // Update turn indicator
        this.updateTurnIndicator(state.current_turn);

        // Check if game is over
        if (state.game_over) {
            this.handleGameOver();
        }
    }

    updateBattleLog(logs) {
        const battleLog = document.getElementById('battleLog');
        if (!battleLog) return;

        battleLog.innerHTML = '';
        logs.forEach(log => {
            const p = document.createElement('p');
            p.textContent = log;
            battleLog.appendChild(p);
        });
        battleLog.scrollTop = battleLog.scrollHeight;
    }

    updateTurnIndicator(turn) {
        const turnIndicator = document.getElementById('turnIndicator');
        if (turnIndicator) {
            turnIndicator.textContent = `Current Turn: Player ${(turn % 2) + 1}`;
        }
    }

    handleGameOver() {
        this.gameOver = true;
        const moveButtons = document.querySelectorAll('.move-button');
        moveButtons.forEach(button => button.disabled = true);

        if (!document.querySelector('#resetButton')) {
            const resetButton = document.createElement('button');
            resetButton.id = 'resetButton';
            resetButton.textContent = 'Play Again';
            resetButton.classList.add('reset-button');
            resetButton.addEventListener('click', () => this.resetBattle());
            document.querySelector('.controls-section').appendChild(resetButton);
        }
    }

    async resetBattle() {
        try {
            await fetch('/battle/reset', { method: 'POST' });
            window.location.href = '/';
        } catch (error) {
            console.error('Error resetting battle:', error);
            this.showMessage('An error occurred while resetting the battle.');
        }
    }

    startBattleStatePolling() {
        setInterval(async () => {
            if (this.gameOver) return;

            try {
                const response = await fetch('/battle/state');
                const result = await response.json();

                if (result.success) {
                    this.updateBattleState(result);
                }
            } catch (error) {
                console.error('Error polling battle state:', error);
            }
        }, 2000);
    }

    showMessage(message) {
        const battleLog = document.getElementById('battleLog');
        const messageElement = document.createElement('p');
        messageElement.classList.add('error-message');
        messageElement.textContent = message;
        battleLog.appendChild(messageElement);
        battleLog.scrollTop = battleLog.scrollHeight;
    }
}