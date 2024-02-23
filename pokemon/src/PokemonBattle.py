from src.Pokemon import Pokemon
from src.DataLayer import DataLayer
import random

class PokemonBattle:
    NUMBER_FIGHTERS = 2
    NUMBER_MOVES = 4

    def __init__(self, num_moves: int = NUMBER_MOVES):
        """
        Constructor for PokemonBattle class.
        Initializes the data access layer and selects fighters for the battle.
        """
        self.dataaccess = DataLayer()
        self.fighters = None
        self.select_fighters(num_moves)

    def select_fighters(self, num_moves):
        """
        Selects Pokemon fighters for the battle.
        """
        self.fighters = self.dataaccess.select_contestants(self.NUMBER_FIGHTERS, num_moves)
        # Ensure the faster Pokemon is positioned first
        if self.fighters[1].speed < self.fighters[0].speed:
            self.fighters.insert(0, self.fighters.pop(1))

    def start_battle(self):
        """
        Initiates the battle between the selected Pokemon fighters.
        """
        print("Contestant 1\n{desc}".format(desc=self.fighters[0].description()))
        print("Contestant 2\n{desc}".format(desc=self.fighters[1].description()))
        print("Let's Get Ready To Rumble!")
        
        round = 0
        while ((self.fighters[0].health > 0) & (self.fighters[1].health > 0)):
            round += 1
            print("===============")
            print("Round", round)
            if round % 2 == 0:
                self.attack(0, 1)
            else:
                self.attack(1, 0)

        winner_index = 0 if (self.fighters[0].health > 0) else 1

        print("=======================================================")
        print(self.fighters[winner_index].name, " wins in ", round, " rounds")
        print("=======================================================")

    def attack(self, attacker: int, defender: int):
        """
        Simulates an attack between the attacker and defender Pokemon.
        """
        move_index = random.randint(0, len(self.fighters[attacker].moves) - 1)
        attack_move = self.fighters[attacker].moves[move_index]
        print("Attacker=", self.fighters[attacker].name, " Health=", self.fighters[attacker].health)
        print("Defender=", self.fighters[defender].name, " Health=", self.fighters[defender].health)
        print("Attack Move Name=", attack_move.name)
        print("Attack Category=", attack_move.category)

        # make sure the attacker can use the move
        if attack_move.PP == 0:
            print("Can not use this move anymore")
            return
        else:
            self.fighters[attacker].moves[move_index].PP -= 1

        if attack_move.category == 'Status':
            print("No Damage")
            return

        # Determine attack and defense values based on move category
        attack = self.fighters[attacker].attack if (attack_move.category == 'Physical') else self.fighters[attacker].special_attack
        defense = self.fighters[defender].attack if (attack_move.category == 'Physical') else self.fighters[defender].special_attack

        # Calculate damage
        damage = ((2 * self.fighters[attacker].level + 10) / 250 * ((attack / defense) * attack_move.base_power)) + 2

        # Apply move type effectiveness multipliers
        attack_category_multiplier = 1.25 if attack_move.move_type in self.fighters[attacker].types else 1
        damage *= attack_category_multiplier

        # Apply attack-defense multipliers based on move type and defender's types
        attack_defense_multiplier = self.dataaccess.select_attack_defense_multipler(attack_move.move_type,
                                                                                     self.fighters[defender].types)
        damage *= attack_defense_multiplier

        print("Attack Value = ", attack)
        print("Defense Value = ", defense)
        print("Attacker/Attack Move Category Multiplier = ", attack_category_multiplier)
        print("Attack Move/Defender Type Multiplier = ", attack_defense_multiplier)
        print("Damage inflicted = ", damage)

        # Determine if the attack hits based on accuracy
        accuracy_level = 100 if attack_move.accuracy == "TRUE" else float(attack_move.accuracy)
        accuracy = random.randint(1, 100)
        print(accuracy, accuracy_level)
        if accuracy <= accuracy_level:
            self.fighters[defender].health -= damage
        else:
            print("Attack Failed, No Damage Applied")
        return
