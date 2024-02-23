import csv

class PokemonMove:

    def __init__(self, name: str, accuracy:int, base_power:int,category:str,PP:int,move_type:str):
        self.name=name
        self.category=category
        self.accuracy=accuracy
        self.base_power=base_power
        self.PP=PP            
        self.move_type=move_type
    