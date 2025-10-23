import numpy as np
import random
import string

def set_variable(default="x", custom_chance=0.2):
    """Helper to set variable name with optional customization."""
    if np.random.rand() > custom_chance:
        return default
    else:
        return random.choice(string.ascii_lowercase.replace('efghij', 'fgh') + string.ascii_uppercase)

def set_variables(defaults=["x", "y"], custom_chance=0.2):
    """Helper to set variable names for multi-variable equations."""
    if np.random.rand() < custom_chance:
        return random.sample(string.ascii_lowercase.replace('efghij', 'fgh'), len(defaults))
    else:
        return defaults

def coef_term(coef, var, power=1):
    """Format a coefficient-variable term (handle 0, 1, -1)."""
    if coef == 0:
        return ""
    
    if power == 2:
        if coef == 1:
            return f"{var}^2"
        if coef == -1:
            return f"-{var}^2"
        return f"{coef}{var}^2"
    elif power == 1:
        if coef == 1:
            return f"{var}"
        if coef == -1:
            return f"-{var}"
        return f"{coef}{var}"
    else:  # constant term
        return str(coef)

def maybe_div(expr, level):
    """Add division optionally in hard mode."""
    if level == "hard" and np.random.rand() < 0.3:
        divisor = random.choice(
            [str(random.randint(2, 15)), random.choice(string.ascii_lowercase)]
        )
        return f"({expr})/{divisor}"
    return expr

def get_num_range(level):
    """Get appropriate number range based on difficulty level."""
    if level == "easy":
        return (-9, 9)
    elif level == "medium":
        return (-50, 50)
    else:  # hard
        return (-999, 999)

def get_symbolic_chance(level):
    """Get probability of symbolic coefficients based on level."""
    if level == "easy":
        return 0.0
    elif level == "medium":
        return 0.3
    else:  # hard
        return 0.5
