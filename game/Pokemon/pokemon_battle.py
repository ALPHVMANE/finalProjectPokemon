
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