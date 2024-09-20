import pygame
import math

def get_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def get_agent(selected_item, agent_buttons):
    if selected_item == "Name":
        return agent_buttons[0]
    else:
        return agent_buttons[1]




def existRule(temp):
    with open('rule.txt', 'r') as file:
        for line in file:
            if temp in line:  
                return line
    return False
