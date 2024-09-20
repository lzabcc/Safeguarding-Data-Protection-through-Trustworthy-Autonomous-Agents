import pygame
from Config import *
from enum import Enum


class State(Enum):
    IDLE = "IDLE"

    SENDING_USER = "SENDING_USER"
    SENDING_AGENT = "SENDING_AGENT"
    SENDING_SERVICE = "SENDING_SERVICE"

    ARRIVED_USER = "ARRIVED_USER"
    ARRIVED_AGENT = "ARRIVED_AGENT"
    ARRIVED_SERVICE = "ARRIVED_SERVICE"


# Service
class Service:
    def __init__(self, name, color, position):
        self.name = name
        self.color = color
        self.position = position
        self.rect = pygame.Rect(position[0] - 20, position[1] - 20, 40, 40)

    def draw(self, win):
        pygame.draw.circle(win, self.color, self.position, 20, 2)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# User
class User:
    def __init__(self, name, age, address, color, position):
        self.name = name
        self.age = age
        self.address = address
        self.color = color
        self.position = position
        self.rect = pygame.Rect(position[0] - 20, position[1] - 20, 40, 40)

    def draw(self, win):
        pygame.draw.circle(win, self.color, self.position, 20, 2)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# Agent
class Agent:
    def __init__(self, name, color, position):
        self.name = name
        self.color = color
        self.position = position
        self.rect = pygame.Rect(position[0] - 20, position[1] - 20, 40, 40)

    def draw(self, win):
        pygame.draw.circle(win, self.color, self.position, 20, 2)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.Font(None, 36)
            text = font.render(self.text, 1, BLACK)
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


