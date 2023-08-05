import random
import json


def create_groups(people: list, groups: int):
    people_left = people
    amount_of_people = len(people)

    insert_name_here = amount_of_people / groups

    with open("groups.json", "r") as f:
        json_groups = json.load(f)

    for i in range(groups):

        json_groups["Group " + str(i + 1)] = []

        for i2 in range(int(insert_name_here)):
            chosen = random.choice(people_left)

            people_left.remove(chosen)

            json_groups["Group " + str(i + 1)].append(chosen)

    with open("groups.json", "w") as f:
        json.dump(json_groups, f, indent=4)

    return json_groups
