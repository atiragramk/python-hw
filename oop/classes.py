class Country:
    def __init__(self, name: str, population: int) -> None:
        self.name = name
        self.population = population

    def add_two_countries(self, other):
        if type(other) != Country:
            return TypeError(f'{other} must be a Country instance')
        name = f'{self.name} {other.name}'
        population = self.population + other.population
        return Country(name, population)

    def __add__(self, other):
        if type(other) != Country:
            return TypeError(f'{other} must be a Country instance')
        name = f'{self.name} {other.name}'
        population = self.population + other.population
        return Country(name, population)


class Car:
    def __init__(self, brand: str, model: str, year: int, speed: int or float) -> None:
        self.brand = brand
        self.model = model
        self.year = year
        self.speed = speed

    def accelerate(self):
        self.speed += 5

    def brake(self):
        self.speed -= 5


class Robot:
    def __init__(self, orientation='up', position_x=0, position_y=0):
        self.orientation = orientation
        self.position_x = position_x
        self.position_y = position_y
        self.directions = ['up', 'right', 'down', 'left']

    def say_hello(self):
        print("I'm not the droid you're looking for")

    def move(self, steps):
        if self.orientation == 'up':
            self.position_y += steps
        elif self.orientation == 'down':
            self.position_y -= steps
        elif self.orientation == 'left':
            self.position_x -= steps
        elif self.orientation == 'right':
            self.position_x += steps

    def turn(self, direction):
        i = self.directions.index(self.orientation)
        if not i:
            return ValueError('Set rigth direction')
        if direction == 'right':
            self.orientation = self.directions[(i + 1) % 4]
        elif direction == 'left':
            self.orientation = self.directions[(i - 1) % 4]

    def display_position(self):
        print(f'Position: ({self.position_x}, {self.position_y})')
        print(f'Orientation: {self.orientation}')
