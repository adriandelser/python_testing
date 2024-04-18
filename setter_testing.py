class Case:
    def __init__(self, name):
        self._name = None
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value in ["value1", "value2", "value3"]:  # Restrict name to certain values
            self._name = value
        else:
            raise ValueError("Invalid name value")

# Example usage
case = Case("value2")
print(case.name)  # Output: value2

# case.name = "value4"  # Raises ValueError: Invalid name value