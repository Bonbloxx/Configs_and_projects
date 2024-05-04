#!/usr/bin/python

import time
import random

points = -1


def total_points():
    global points
    points += 1
    return points


OPERATORS = ["+", "-", "*"]
MIN_OPERAND = 1
MAX_OPERAND = 15


def calculation():
    left = random.randint(MIN_OPERAND, MAX_OPERAND)
    right = random.randint(MIN_OPERAND, MAX_OPERAND)
    operator = random.choice(OPERATORS)

    expr = str(left) + operator + str(right)
    answer = eval(expr)
    return expr, answer


expr, answer = calculation()
input("Press enter to start ")
start = time.time()

max_rolls = 10
for i in range(max_rolls):
    expr, answer = calculation()
    calc = input("Problem #" + str(i + 1) + ": " + expr + " = ")
    if calc != str(answer):
        print("wrong")
    else:
        print("correct")
        total_points()

end = time.time()
total_time = round(end - start, 2)
print("Your total points are", total_points(), "and your time is", total_time)
