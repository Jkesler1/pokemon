import csv
import random

class Pokemon:

    def __init__(self, Name: str, Types, Stats, Moves, Level=1):
        """
        Constructor method for Pokemon class.
        Initializes a Pokemon instance with the provided attributes.
        """
        print(Stats)  
        self.name = Name
        self.types = Types.split("|") 
        
        # Assigning stats to the Pokemon object
        self.level = Level
        self.health = int(Stats['hp'])
        self.attack = int(Stats['atk'])
        self.defense = int(Stats['def'])
        self.special_attack = int(Stats['spa'])
        self.special_defense = int(Stats['spd'])
        self.speed = int(Stats['spe'])
        self.moves = Moves  

    def move_list_str(self):
        """
        Returns a string representation of the moves available to the Pokemon.

        """
        move_list = str.join(",", [move.name for move in self.moves]) 
        return move_list

    def description(self):
        """
        Returns a formatted string describing the Pokemon's attributes.
        """
        return "Name: {name}\nHealth : {health}\nSpeed: {speed}\nTypes: {types}\nMoves: {moves}".format(
            name=self.name, moves=self.move_list_str(), health=self.health, speed=self.speed, types=self.types)
