from classes import Country, Car, Robot

if __name__ == "__main__":
    bosnia = Country('Bosnia', 10000000)
    herzegovina = Country('Herzegovina', 5000000)

    # bosnia_herzegovina = bosnia.add_two_countries(herzegovina)
    bosnia_herzegovina = bosnia + herzegovina

    print(bosnia_herzegovina.name)
    print(bosnia_herzegovina.population)

    audi = Car('audi', 'q8', 2012, 200)
    audi.accelerate()
    print(audi.speed)
    audi.brake()
    print(audi.speed)

    r2_d2 = Robot('left', 5, 10)
    r2_d2.move(10)
    r2_d2.turn('left')

    print(r2_d2.display_position())
    print(r2_d2.say_hello())
