from .base import AlgebraProblem
from .utils import set_variables, coef_term, maybe_div, get_num_range, get_symbolic_chance
import numpy as np
import random

class Generate_Linear_Two_V(AlgebraProblem):
    def __init__(self):
        super().__init__(problem_type="equations.linear.two_v")
        self.variables = ["x", "y"]
        self.lhs = []
        self.rhs = []

    def generate_question(self, level="easy"):
        self.level = level
        self.variables = set_variables()
        self.lhs, self.rhs = self.generate_equations(level)
        self.question = self.question_text()
        self.json = self.generate_json()
        return self.question, self.json

    def make_equation(self, level):
        num_range = get_num_range(level)
        symbolic_chance = get_symbolic_chance(level)

        lhs_terms = []
        vars = self.variables

        a = random.randint(*num_range)
        b = random.randint(*num_range)
        c = random.randint(*num_range)

        if np.random.rand() < symbolic_chance:
            a = random.choice(string.ascii_lowercase)
        if np.random.rand() < symbolic_chance:
            b = random.choice(string.ascii_lowercase)

        term1 = coef_term(a, vars[0])
        term2 = coef_term(b, vars[1])

        terms = [t for t in [term1, term2] if t]
        if len(terms) == 2:
            if random.random() < 0.5:
                lhs = f"{terms[0]} + {terms[1]}"
            else:
                lhs = f"{terms[0]} - {terms[1].replace('-', '')}"
        elif terms:
            lhs = terms[0]
        else:
            lhs = "0"

        lhs = maybe_div(lhs, level)

        rhs = str(c)
        if symbolic_chance > 0 and np.random.rand() < symbolic_chance:
            rhs = f"{rhs} + {random.choice(string.ascii_lowercase)}"
        if level == "hard" and np.random.rand() < 0.3:
            rhs = f"({rhs})/{random.choice([str(random.randint(2,15)), random.choice(string.ascii_lowercase)])}"

        return lhs, rhs

    def generate_equations(self, level):
        eqs_lhs, eqs_rhs = [], []
        for _ in range(2):
            lhs, rhs = self.make_equation(level)
            eqs_lhs.append(lhs)
            eqs_rhs.append(rhs)
        return eqs_lhs, eqs_rhs

    def question_text(self):
        templates = [
            "Solve for {variables}: {lhs0} = {rhs0} and {lhs1} = {rhs1}.",
            "Find {variables} such that {lhs0} = {rhs0}, {lhs1} = {rhs1}.",
            "Determine the values of {variables} satisfying {lhs0} = {rhs0} and {lhs1} = {rhs1}.",
            "What are {variables} if {lhs0} = {rhs0} and {lhs1} = {rhs1}?",
            "Solve the following system of equations for {variables}: {lhs0} = {rhs0}, {lhs1} = {rhs1}.",
            "Given {lhs0} = {rhs0} and {lhs1} = {rhs1}, find {variables}."
        ]
        tpl = random.choice(templates)
        return tpl.format(
            variables=" and ".join(self.variables),
            lhs0=self.lhs[0],
            rhs0=self.rhs[0],
            lhs1=self.lhs[1],
            rhs1=self.rhs[1]
        )

    def generate_json(self):
        base_json = super().generate_json()
        base_json.update({
            "variables": self.variables,
            "lhs": self.lhs,
            "rhs": self.rhs
        })
        return base_json
