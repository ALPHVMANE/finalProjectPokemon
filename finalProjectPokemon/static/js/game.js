import { MessageManager } from './managers/MessageManager.js';

updateGameState() {
    this.messageManager.updateMessages(this.gameState.messages);
    this.uiManager.updateHealthBar(this.gameState.entities);
    this.renderManager.render(this.gameState);

    // Play combat sound if there was combat this turn
    if (this.gameState.combat_this_turn) {
        this.audioManager.playRandomSwing();
    }

    // Handle game over state
    if (this.gameState.game_over) {
        this.gameOverlay.style.display = 'flex';
    } else {
        this.gameOverlay.style.display = 'none';
    }
}

// Update HP display function
    window.updateHP = function(pokemonId, currentHP, maxHP) {
        const currentHPElement = document.getElementById(`${pokemonId}-current-hp`);
        const hpFillElement = document.getElementById(`${pokemonId}-hp-fill`);

        if (currentHPElement && hpFillElement) {
            currentHPElement.textContent = currentHP;

            // Update HP bar fill
            const percentage = (currentHP / maxHP) * 100;
            hpFillElement.style.width = `${percentage}%`;

            // Change color based on HP percentage
            if (percentage > 50) {
                hpFillElement.style.backgroundColor = '#00ff00';
            } else if (percentage > 25) {
                hpFillElement.style.backgroundColor = '#ffff00';
            } else {
                hpFillElement.style.backgroundColor = '#ff0000';
            }
        }
    };
});