from .base import AlgebraProblem
from .utils import set_variable, coef_term, maybe_div, get_num_range, get_symbolic_chance
import numpy as np
import random
import string

class Generate_Quadratic_One_V(AlgebraProblem):
    def __init__(self):
        super().__init__(problem_type="equations.quadratic.one_v")
        self.variable = "x"
        self.lhs = None
        self.rhs = None

    def generate_question(self, level="easy"):
        self.level = level
        self.variable = set_variable()
        self.lhs, self.rhs = self.generate_equation(level)
        self.question = self.question_text()
        self.json = self.generate_json()
        return self.question, self.json

    def generate_equation(self, level):
        num_range = get_num_range(level)
        symbolic_chance = get_symbolic_chance(level)

        a = random.randint(*num_range)
        b = random.randint(*num_range)
        c = random.randint(*num_range)
        d = random.randint(*num_range)

        while a == 0:
            a = random.randint(*num_range)

        if np.random.rand() < symbolic_chance:
            a = random.choice(string.ascii_lowercase)
        if np.random.rand() < symbolic_chance:
            b = random.choice(string.ascii_lowercase)
        if np.random.rand() < symbolic_chance and level == "hard":
            c = random.choice(string.ascii_lowercase)

        terms = []
        for coef, p in zip([a, b, c], [2, 1, 0]):
            term = coef_term(coef, self.variable, p)
            if term:
                terms.append(term)
        lhs = " + ".join(terms)
        lhs = lhs.replace("+ -", "- ")

        lhs = maybe_div(lhs, level)

        if level == "easy":
            rhs = "0"
        elif level == "medium":
            rhs = str(d)
        else:
            rhs = coef_term(random.randint(*num_range), self.variable, 1)
            if np.random.rand() < 0.4:
                rhs += f" + {random.choice(string.ascii_lowercase)}"
            rhs = maybe_div(rhs, level)

        return lhs, rhs

    def question_text(self):
        templates = [
            "Solve for {variable}: {lhs} = {rhs}.",
            "Find the value(s) of {variable} that satisfy {lhs} = {rhs}.",
            "Determine {variable} such that {lhs} = {rhs}.",
            "When does {lhs} = {rhs}? Solve for {variable}.",
            "Find all possible {variable} for which {lhs} = {rhs}.",
            "Solve the quadratic equation {lhs} = {rhs}."
        ]
        tpl = random.choice(templates)
        return tpl.format(variable=self.variable, lhs=self.lhs, rhs=self.rhs)

    def generate_json(self):
        base_json = super().generate_json()
        base_json.update({
            "variables": [self.variable],
            "lhs": [self.lhs],
            "rhs": [self.rhs]
        })
        return base_json












class Generate_Quadratic_Inequality_One_V(AlgebraProblem):
    def __init__(self):
        super().__init__(problem_type="inequalities.quadratic.one_v")
        self.variable = "x"
        self.lhs = None
        self.rhs = None
        self.inequality_sign = None

    def generate_question(self, level="easy"):
        self.level = level
        self.variable = set_variable()
        self.lhs, self.rhs = self.generate_equation(level)  # Reuse the equation generation!
        self.inequality_sign = self.get_inequality_sign(level)
        self.question = self.question_text()
        self.json = self.generate_json()
        return self.question, self.json

    def generate_equation(self, level):
        """Reuse the exact same equation generation from Generate_Quadratic_One_V"""
        num_range = get_num_range(level)
        symbolic_chance = get_symbolic_chance(level)

        a = random.randint(*num_range)
        b = random.randint(*num_range)
        c = random.randint(*num_range)
        d = random.randint(*num_range)

        while a == 0:
            a = random.randint(*num_range)

        if np.random.rand() < symbolic_chance:
            a = random.choice(string.ascii_lowercase)
        if np.random.rand() < symbolic_chance:
            b = random.choice(string.ascii_lowercase)
        if np.random.rand() < symbolic_chance and level == "hard":
            c = random.choice(string.ascii_lowercase)

        terms = []
        for coef, p in zip([a, b, c], [2, 1, 0]):
            term = coef_term(coef, self.variable, p)
            if term:
                terms.append(term)
        lhs = " + ".join(terms)
        lhs = lhs.replace("+ -", "- ")

        lhs = maybe_div(lhs, level)

        if level == "easy":
            rhs = "0"
        elif level == "medium":
            rhs = str(d)
        else:
            rhs = coef_term(random.randint(*num_range), self.variable, 1)
            if np.random.rand() < 0.4:
                rhs += f" + {random.choice(string.ascii_lowercase)}"
            rhs = maybe_div(rhs, level)

        return lhs, rhs

    def get_inequality_sign(self, level):
        """Get appropriate inequality sign based on level."""
        basic_signs = ["<", ">", "≤", "≥"]
        compound_signs = ["<", ">", "≤", "≥", "≠"]
        
        if level == "easy":
            return random.choice(basic_signs)
        elif level == "medium":
            return random.choice(compound_signs)
        else:  # hard
            # For hard, sometimes create compound inequalities
            if np.random.rand() < 0.2:
                sign1 = random.choice(["<", "≤"])
                sign2 = random.choice([">", "≥"]) 
                return f"{sign1} {self.variable} {sign2}"
            return random.choice(compound_signs)

    def question_text(self):
        inequality = f"{self.lhs} {self.inequality_sign} {self.rhs}"
        templates = [
            f"Solve for {self.variable}: {inequality}",
            f"What values of {self.variable} satisfy {inequality}?",
            f"Find {self.variable} such that {inequality}.",
            f"Solve the quadratic inequality {inequality} for {self.variable}.",
            f"Determine the solution set for {inequality}.",
            f"Find all {self.variable} that make {inequality} true.",
            f"For which values of {self.variable} is {inequality} true?",
            f"Solve the inequality {inequality}."
        ]
        return random.choice(templates)

    def generate_json(self):
        base_json = super().generate_json()
        base_json.update({
            "variables": self.variable],
            "lhs": [self.lhs],
            "rhs": [self.rhs],
            "inequality_sign": self.inequality_sign
        })
        return base_json
