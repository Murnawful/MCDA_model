from math import *


def canon_effect_on_wall(wall_state):
    x = wall_state
    a = 1
    b = 30
    c = 0.5
    sigma = 0.2
    return a / (1 + exp(-sigma * (b - x))) + c


def canon_effect_on_civil(wall_state):
    x = wall_state
    a = 50
    b = 30
    c = 0
    sigma = 0.2
    return a / (1 + exp(-sigma * (b - x))) + c


def canon_effect_on_enemy_soldiers(wall_state):
    x = wall_state
    a = 190
    b = 40
    c = 10
    sigma = 0.2
    return a / (1 + exp(-sigma * (b - x))) + c


def canon_effect_on_allied_soldiers(canon_state):
    x = canon_state
    a = 3
    b = 20
    c = 0
    sigma = 0.2
    return a / (1 + exp(-sigma * (b - x))) + c


def canon_deterioration(canon_state):
    x = canon_state
    a = 1
    sigma = 0.01
    return a * exp(-sigma * x)


def assault_effect_on_ennemy_soldiers(wall_state, soldiers_sent, remaining_defenders):
    x = wall_state
    ax = 1
    bx = 40
    cx = 0.5
    sigmax = 0.07
    sigmox = ax / (1 + exp(-sigmax * (bx - x))) + cx

    y = soldiers_sent
    ay = 1
    by = 30000
    cy = 0
    sigmay = 0.0001
    sigmoy = ay / (1 + exp(-sigmay * (by - y))) + cy

    z = soldiers_sent / remaining_defenders
    if z <= 1:
        factz = z
    else:
        factz = 1 / z

    return sigmox * sigmoy * factz


def assault_effect_on_allied_soldiers(wall_state, soldiers_sent, remaining_defenders):
    x = wall_state
    ax = 0.5
    bx = 60
    cx = 0.75
    sigmax = 0.07
    sigmox = ax / (1 + exp(-sigmax * (x - bx))) + cx

    y = soldiers_sent
    ay = -1
    by = 50000
    cy = 2
    sigmay = 0.0001
    sigmoy = ay / (1 + exp(-sigmay * (by - y))) + cy

    z = remaining_defenders / soldiers_sent
    if z <= 1:
        factz = z
    else:
        factz = 1 / z

    return sigmox * sigmoy * factz


def assault_effect_on_civil(wall_state, soldiers_sent, remaining_defenders):
    error_rate = 0.2

    base_line = soldiers_sent * error_rate

    x = wall_state
    ax = -1
    bx = 75
    cx = 1
    sigmax = 0.07
    sigmox = ax / (1 + exp(-sigmax * (x - bx))) + cx

    z = remaining_defenders
    az = -1
    bz = 4000
    cz = 1
    sigmaz = 0.001
    sigmoz = az / (1 + exp(-sigmaz * (z - bz))) + cz

    return base_line * sigmox * sigmoz
