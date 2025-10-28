from .base import CalculusProblem
import random

class Generate_Polynomial_Derivative(CalculusProblem):
    def __init__(self):
        super().__init__(problem_type="derivative.polynomial")
        self.templates = PolynomialTemplates()

    def generate_question(self, level="easy"):
        self.level = level
        self.variable = self.set_variable()
        self.expression = self.generate_expression(level)
        self.question = self.templates.get_question(self.expression, self.variable)
        self.json = self.generate_json()
        return self.question, self.json

    def set_variable(self):
        """Set the variable for differentiation"""
        if random.random() < 0.8:  # 80% x, 20% other letters
            return "x"
        else:
            return random.choice(["y", "t", "z"])

    def generate_expression(self, level):
        """Generate polynomial expression based on difficulty level"""
        if level == "easy":
            return self.generate_easy_expression()
        elif level == "medium":
            return self.generate_medium_expression()
        else:  # hard
            return self.generate_hard_expression()

    def generate_easy_expression(self):
        """Single term polynomials: ax^n"""
        coef = random.randint(1, 5)
        power = random.randint(2, 5)
        return f"{coef}{self.variable}^{power}"

    def generate_medium_expression(self):
        """Sums of terms, negative and fractional coefficients/powers"""
        if random.random() < 0.7:  # 70% sums with negatives
            num_terms = random.randint(2, 4)
            terms = []
            
            for _ in range(num_terms):
                coef = random.choice([-3, -2, -1, 1, 2, 3, 4])
                power = random.randint(0, 4)
                terms.append((coef, power))
            
            # Ensure at least one term has power > 0 for derivative
            if all(power == 0 for _, power in terms):
                terms[-1] = (terms[-1][0], random.randint(1, 3))
            
            return self.format_polynomial(terms)
        else:  # 30% fractional/negative powers
            coef = random.randint(1, 4)
            power = random.choice([-2, -1, 0.5, 1.5, 2.5])
            return f"{coef}{self.variable}^{power}"

    def generate_hard_expression(self):
        """Multiplications, divisions, chain rules"""
        problem_type = random.choice(["product", "quotient", "chain"])
        
        if problem_type == "product":
            # f(x) * g(x) where both are polynomials
            coef1, power1 = random.randint(1, 3), random.randint(1, 3)
            coef2, power2 = random.randint(1, 3), random.randint(1, 3)
            return f"({coef1}{self.variable}^{power1}) * ({coef2}{self.variable}^{power2})"
            
        elif problem_type == "quotient":
            # f(x) / g(x) where both are polynomials
            num_coef, num_power = random.randint(1, 3), random.randint(1, 3)
            den_coef, den_power = random.randint(1, 3), random.randint(1, 3)
            return f"({num_coef}{self.variable}^{num_power}) / ({den_coef}{self.variable}^{den_power})"
            
        else:  # chain rule
            # f(g(x)) where both are polynomials
            outer_coef, outer_power = random.randint(1, 3), random.randint(2, 3)
            inner_coef, inner_power = random.randint(1, 3), random.randint(1, 2)
            return f"({outer_coef}({inner_coef}{self.variable}^{inner_power}))^{outer_power}"

    def format_polynomial(self, terms):
        """Format polynomial terms into a string"""
        parts = []
        for coef, power in terms:
            if coef == 0:
                continue
            if power == 0:
                parts.append(f"{coef}")
            elif power == 1:
                if coef == 1:
                    parts.append(f"{self.variable}")
                elif coef == -1:
                    parts.append(f"-{self.variable}")
                else:
                    parts.append(f"{coef}{self.variable}")
            else:
                if coef == 1:
                    parts.append(f"{self.variable}^{power}")
                elif coef == -1:
                    parts.append(f"-{self.variable}^{power}")
                else:
                    parts.append(f"{coef}{self.variable}^{power}")
        
        if not parts:
            return "0"
            
        # Join with +, handle negatives
        result = parts[0]
        for part in parts[1:]:
            if part.startswith('-'):
                result += f" - {part[1:]}"
            else:
                result += f" + {part}"
        return result

    def generate_json(self):
        base_json = super().generate_json()
        base_json.update({
            "variable": self.variable,
            "expression": self.expression
        })
        return base_json


class PolynomialTemplates:
    def get_question(self, expression, variable):
        templates = [
            f"Calculate the derivative of f({variable}) = {expression}",
            f"Find f'({variable}) for f({variable}) = {expression}",
            f"Differentiate f({variable}) = {expression}",
            f"Compute the derivative of {expression}",
            f"What is the derivative of {expression}?",
            f"Determine f'({variable}) given f({variable}) = {expression}",
            f"Find the derivative of the function {expression}",
            f"Calculate d/d{variable} of {expression}",
            f"Differentiate the function f({variable}) = {expression}",
            f"What is f'({variable}) when f({variable}) = {expression}?",
            f"Calculate the derivative of y = {expression} where y is a function of {variable}",
            f"Find dy/d{variable} for y = {expression}",
            f"Differentiate y = {expression} with respect to {variable}",
            f"What is dy/d{variable} when y = {expression}?",
            f"Compute the derivative of y with respect to {variable} given y = {expression}"
        ]
        return random.choice(templates)
