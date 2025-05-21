import math

def user_level_from_xp(xp, base=100, exponent=1.5):
    """
    Calcula el nivel de un usuario basado en su experiencia (XP).
    La fórmula utilizada es: XP = base * (nivel ^ exponent).
    """
    level = 1
    while xp >= base * (level ** exponent):
        level += 1
    return level