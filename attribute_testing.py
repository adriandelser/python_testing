class Vehicle:
    def __init__(self) -> None:
        self.source_strength = 1
    

attribute = 'source_strength'

if not hasattr(Vehicle(), attribute):
    print(f"Attribute {attribute} does not exist in the Vehicle class.")