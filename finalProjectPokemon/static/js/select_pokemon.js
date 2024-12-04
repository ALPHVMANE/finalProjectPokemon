function toggleSelection(card, pokemonName) {
            const input = card.querySelector('input');
            const selected = card.classList.toggle('selected');
            input.disabled = !selected;

            const selectedCards = document.querySelectorAll('.pokemon-card.selected');
            if (selectedCards.length > 3 && selected) {
                card.classList.remove('selected');
                input.disabled = true;
                alert('You can only select 3 Pokemon!');
                return;
            }

            // Update selection indicators
            selectedCards.forEach((selectedCard, index) => {
                const indicator = selectedCard.querySelector('.selection-indicator');
                indicator.textContent = (index + 1);
            });

            // Clear indicators for unselected cards
            document.querySelectorAll('.pokemon-card:not(.selected) .selection-indicator')
                .forEach(indicator => indicator.textContent = '✓');
        }

        document.getElementById('pokemon-form').onsubmit = function(e) {
            const selectedCount = document.querySelectorAll('.pokemon-card.selected').length;
            if (selectedCount !== 3) {
                e.preventDefault();
                alert('Please select exactly 3 Pokemon!');
            }
        };