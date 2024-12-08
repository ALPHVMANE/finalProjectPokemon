class Move:
    def __init__(self, name, power, accuracy):
        self.name = name
        self.power = power
        self.accuracy = accuracy

class Pokemon:
    def __init__(self, name, hp, attack, defense, speed, moves):
        self.name = name
        self.max_hp = hp
        self.current_hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.moves = moves
        self.is_fainted = False

    def take_damage(self, damage):
        self.current_hp = max(0, self.current_hp - damage)
        if self.current_hp == 0:
            self.is_fainted = True

    def use_move(self, move, target):
        if self.is_fainted:
            return {
                'success': False,
                'message': f'{self.name} has fainted and cannot move!'
            }

        # Basic damage calculation
        damage = int((((2 * 1 + 10) / 250) * (self.attack / target.defense) * move.power + 2))
        target.take_damage(damage)

        return {
            'success': True,
            'message': f'{self.name} used {move.name} on {target.name}!',
            'damage': damage,
            'target_remaining_hp': target.current_hp
        }

#DEMO AREA
if __name__ == '__main__':
    # Create powerful moves
    flamethrower = Move("Flamethrower", power=90, accuracy=100)
    blast_burn = Move("Blast Burn", power=150, accuracy=90)
    air_slash = Move("Air Slash", power=75, accuracy=95)
    dragon_claw = Move("Dragon Claw", power=80, accuracy=100)

    psychic = Move("Psychic", power=90, accuracy=100)
    shadow_ball = Move("Shadow Ball", power=80, accuracy=100)

    # Create Pokemon with their moves
    charizard = Pokemon(
        name="Charizard",
        hp= 12,
        attack=267,
        defense=247,
        speed=299,
        moves=[flamethrower, blast_burn, air_slash, dragon_claw]
    )

    mewtwo = Pokemon(
        name="Mewtwo",
        hp=416,
        attack=350,
        defense=216,
        speed=394,
        moves=[psychic, shadow_ball]
    )

    # Simulate battle
    print("=== Poke Sim ===")
    print(f"{charizard.name} HP: {charizard.current_hp}")
    print(f"{mewtwo.name} HP: {mewtwo.current_hp}\n")

    # Round 1: Charizard uses Blast Burn
    result = charizard.use_move(blast_burn, mewtwo)
    print(result['message'])
    print(f"Damage dealt: {result['damage']}")
    print(f"{mewtwo.name}'s remaining HP: {result['target_remaining_hp']}\n")

    # Round 2: Mewtwo counters
    result = mewtwo.use_move(psychic, charizard)
    print(result['message'])
    print(f"Damage dealt: {result['damage']}")
    print(f"{charizard.name}'s remaining HP: {result['target_remaining_hp']}\n")

    # Round 3: Charizard uses Dragon Claw
    result = charizard.use_move(dragon_claw, mewtwo)
    print(result['message'])
    print(f"Damage dealt: {result['damage']}")
    print(f"{mewtwo.name}'s remaining HP: {result['target_remaining_hp']}\n")

    # Round 4: Mewtwo uses Shadow Ball
    result = mewtwo.use_move(shadow_ball, charizard)
    print(result['message'])
    print(f"Damage dealt: {result['damage']}")
    print(f"{charizard.name}'s remaining HP: {result['target_remaining_hp']}\n")

    # Show final battle status
    print("=== Battle Status ===")
    print(f"{charizard.name}: {'Fainted' if charizard.is_fainted else 'HP: ' + str(charizard.current_hp)}")