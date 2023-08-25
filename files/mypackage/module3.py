from random import randint
import csv

players = ['John', 'Hannah', 'Jack', 'Isaac', 'Arianna']


def round_simulator(players: list, rounds: int) -> list:
    res = []
    for i in range(1, rounds + 1):
        for player in players:
            score = (player, randint(0, 1000))
            res.append(score)
    return res


def record_score():
    with open('./files/score.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['Player name', 'Score'])
        content = round_simulator(players, 100)
        for score in content:
            writer.writerow(score)
