import csv
import random
from src.Pokemon import Pokemon
from src.PokemonMove import PokemonMove

class DataLayer:
    POKEMON_FILE='./data/Pokemon.csv'
    MOVES_FILE='./data/PokemonMoves.csv'
    LEARNABLE_MOVES_FILE='./data/PokemonLearnableMoves.csv'
    MULTIPLIER_FILE='./data/AttackTypeMultipliers.csv'
    
    def __init__(self):
        """
        Constructor for DataLayer class.
        Initializes the data access layer by loading multipliers, move data, and available moves for Pokemon.
        """
        print("Initializing Data Access")
        super().__init__()
        self.attack_defense_multipliers = self.load_multipliers()
        self.move_properties = self.load_move_data()
        self.pokemon_available_moves = self.load_learnable_move_data()
 
    def load_move_data(self):
        """
        Loads move data from the MOVES_FILE.
        Returns a dictionary containing move names as keys and corresponding PokemonMove objects.
        """
        move_dict = {}
        with open(self.MOVES_FILE, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                move = PokemonMove(row["Name"], row["Accuracy"], int(row["BasePower"]), row["Category"], int(row["PP"]), row["Type"])
                move_dict[row["Name"].replace(" ","").lower()] = move
        return move_dict
    
    def load_multipliers(self):
        """
        Loads attack/defense multipliers from the MULTIPLIER_FILE.
        Returns a dictionary containing attack/defense pairs as keys and corresponding multiplier values.
        
        """
        multiplier_dict = {}
        with open(self.MULTIPLIER_FILE, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                multiplier_dict[row["Attack/Defense"]] = row
        return multiplier_dict
    
    def load_learnable_move_data(self):
        """
        Loads learnable move data from the LEARNABLE_MOVES_FILE.
        Returns a dictionary containing Pokemon names as keys and lists of learnable moves as values.
        """
        move_dict = {}
        with open(self.LEARNABLE_MOVES_FILE, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                moves = row["Moveset"].split("|")
                move_dict[row["Name"].replace(" ","").lower()] = moves
        return move_dict
    
    def load_pokemon_data(self):
        """
        Loads Pokemon data from the POKEMON_FILE.
        Returns a list of dictionaries containing Pokemon data.
        """
        with open(self.POKEMON_FILE, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            pokemon_list = [row for row in reader]
        return pokemon_list
        
    def select_contestants(self, num_contestants: int = 2, num_moves: int = 4):
        """
        Selects Pokemon contestants for battle.
        Returns a list of Pokemon objects.
        """
        contestants = []
        for pkmn in random.sample(self.load_pokemon_data(), num_contestants):
            stats_dict = {}
            for pair in pkmn["Stats"].split('|'):
                key, value = pair.split(':')
                stats_dict[key] = value
            moves_list = self.select_moves(pkmn["Name"].lower(), num_moves)    
            contestants.append(Pokemon(pkmn["Name"], pkmn["Types"], stats_dict, moves_list))
        return contestants

    def select_moves(self, name: str, move_count: int):
        """
        Selects moves for a Pokemon based on its name and move count.
        Returns a list of PokemonMove objects.
        """
        moves = []
        for move in random.sample(self.pokemon_available_moves[name], move_count):
            moves.append(self.move_properties[move])
        return moves  
    
    def select_attack_defense_multipler(self, attack_category: str, defense_category_list=None):
        """
        Selects attack-defense multiplier based on attack and defense categories.
        Returns the multiplier value.
        """
        multiplier = 1
        for category in defense_category_list:
            multiplier *= float(self.attack_defense_multipliers[attack_category][category])
        return multiplier
