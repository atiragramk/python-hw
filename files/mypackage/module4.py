import csv


def record_highest_score():
    res_dict = {}
    with open('./files/score.csv', 'r') as score_file:
        next(score_file)
        reader = csv.reader(score_file)
        for row in reader:
            name, score = row
            if name in res_dict:
                res_dict[name].append(score)
            else:
                res_dict[name] = [score]
    for key, value in res_dict.items():
        res_dict[key] = max(value)

    sorted_results = sorted(
        res_dict.items(), key=lambda el: el[1], reverse=True)

    with open('./files/highestscore.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['Player name', 'Hignest Score'])
        for row in sorted_results:
            writer.writerow(row)
