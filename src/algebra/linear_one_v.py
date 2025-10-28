from .base import AlgebraProblem
from .utils import set_variable, coef_term, maybe_div, get_num_range, get_symbolic_chance
import numpy as np
import random
import string

class Generate_Linear_One_V(AlgebraProblem):
    def __init__(self):
        super().__init__(problem_type="equations.linear.one_v")
        self.equation = None
        self.variable = None
        self.lhs = None
        self.rhs = None

    def generate_question(self, level="easy"):
        self.variable = set_variable()
        self.level = level
        self.lhs, self.rhs = self.generate_equation(level)
        self.equation = f"{self.lhs} = {self.rhs}"
        self.question = self.question_text()
        self.json = self.generate_json()
        return self.question, self.json

    def question_text(self):
        templates = [
            f"Solve for {self.variable}: {self.equation}",
            f"What value of {self.variable} makes {self.equation} true?",
            f"Find {self.variable} if {self.equation}.",
            f"Solve {self.equation} for {self.variable}.",
            f"When {self.equation}, what is {self.variable}?",
            f"Determine {self.variable} such that {self.equation}."
        ]
        return random.choice(templates)

    def generate_equation(self, level="easy"):
        def make_expr(level, symbol_allowed=False):
            num_range = get_num_range(level)
            symbolic_chance = get_symbolic_chance(level) if symbol_allowed else 0.0

            a_val = random.randint(*num_range)
            b_val = random.randint(*num_range)

            if symbol_allowed and np.random.rand() < symbolic_chance:
                a_val = random.choice(string.ascii_lowercase)
            if symbol_allowed and np.random.rand() < symbolic_chance:
                b_val = random.choice(string.ascii_lowercase)

            lhs_terms = []
            if a_val not in [0, "0"]:
                term = coef_term(a_val, self.variable)
                term = maybe_div(term, level)
                lhs_terms.append(term)

            if b_val not in [0, "0"]:
                op = "+" if (isinstance(b_val, str) or b_val > 0) else "-"
                val = b_val if isinstance(b_val, str) else abs(b_val)
                lhs_terms.append(f"{op} {val}")

            expr = " ".join(lhs_terms).strip()
            return expr or str(random.randint(1, 9))

        if level == "easy":
            lhs = make_expr("easy", symbol_allowed=False)
            rhs = str(random.randint(-9, 9))
        elif level == "medium":
            lhs = make_expr("medium", symbol_allowed=False)
            rhs = make_expr("medium", symbol_allowed=True)
        else:  # hard
            lhs = make_expr("hard", symbol_allowed=True)
            rhs = make_expr("hard", symbol_allowed=True)

            if np.random.rand() < 0.4:
                nested = make_expr("hard", symbol_allowed=True)
                lhs += f" + ({nested})"
            if np.random.rand() < 0.4:
                nested = make_expr("hard", symbol_allowed=True)
                rhs += f" + ({nested})"

        return lhs, rhs

    def generate_json(self):
        base_json = super().generate_json()
        base_json.update({
            "variables": [self.variable],
            "lhs": [self.lhs],
            "rhs": [self.rhs]
        })
        return base_json




class Generate_Linear_Inequality_One_V(AlgebraProblem):
    def __init__(self):
        super().__init__(problem_type="inequalities.linear.one_v")
        self.inequality = None
        self.variable = None
        self.lhs = None
        self.rhs = None
        self.inequality_sign = None

    def generate_question(self, level="easy"):
        self.variable = set_variable()
        self.level = level
        self.lhs, self.rhs = self.generate_equation(level)  # REUSE the existing method!
        self.inequality_sign = self.get_inequality_sign(level)
        self.inequality = f"{self.lhs} {self.inequality_sign} {self.rhs}"
        self.question = self.question_text()
        self.json = self.generate_json()
        return self.question, self.json

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
            if np.random.rand() < 0.3:
                sign1 = random.choice(["<", "≤"])
                sign2 = random.choice([">", "≥"]) 
                return f"{sign1} {self.variable} {sign2}"
            return random.choice(compound_signs)

    def question_text(self):
        templates = [
            f"Solve for {self.variable}: {self.inequality}",
            f"What values of {self.variable} satisfy {self.inequality}?",
            f"Find {self.variable} such that {self.inequality}.",
            f"Solve the inequality {self.inequality} for {self.variable}.",
            f"Determine the solution set for {self.inequality}.",
            f"Find all {self.variable} that make {self.inequality} true."
        ]
        return random.choice(templates)

    def generate_json(self):
        base_json = super().generate_json()
        base_json.update({
            "variables": [self.variable],
            "lhs": [self.lhs],
            "rhs": [self.rhs],
            "inequality_sign": self.inequality_sign
        })
        return base_json
