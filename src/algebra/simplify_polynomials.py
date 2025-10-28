from .base import AlgebraProblem
from .utils import set_variable, coef_term, get_num_range
import numpy as np
import random
import string

class Generate_Simplify_Polynomial(AlgebraProblem):
    def __init__(self):
        super().__init__(problem_type="simplify.polynomial")
        self.expression = None
        self.variable = None

    def generate_question(self, level="easy"):
        self.variable = set_variable()
        self.level = level
        self.expression = self.generate_expression(level)
        self.question = self.question_text()
        self.json = self.generate_json()
        return self.question, self.json

    def generate_expression(self, level):
        """Generate polynomial expression based on difficulty level."""
        if level == "easy":
            return self.generate_easy_expression()
        elif level == "medium":
            return self.generate_medium_expression()
        else:  # hard
            return self.generate_hard_expression()

    def generate_easy_expression(self):
        """Only x and numbers - simple addition/subtraction"""
        num_terms = random.randint(3, 5)
        terms = []
        
        for _ in range(num_terms):
            coef = random.randint(-9, 9)
            while coef == 0:
                coef = random.randint(-9, 9)
            
            # Only x^1 or constants
            power = random.choice([0, 1])
            if power == 0:
                term = str(coef)
            else:
                if coef == 1:
                    term = self.variable
                elif coef == -1:
                    term = f"-{self.variable}"
                else:
                    term = f"{coef}{self.variable}"
            
            terms.append(term)
        
        # Ensure we have some like terms
        if all(term.replace('-', '').replace(self.variable, '') for term in terms if self.variable in term):
            # Add another x term
            coef = random.randint(-9, 9)
            while coef == 0:
                coef = random.randint(-9, 9)
            if coef == 1:
                terms.append(self.variable)
            elif coef == -1:
                terms.append(f"-{self.variable}")
            else:
                terms.append(f"{coef}{self.variable}")
        
        random.shuffle(terms)
        expression = terms[0]
        for term in terms[1:]:
            if term.startswith('-'):
                expression += f" - {term[1:]}"
            else:
                expression += f" + {term}"
        
        return expression

    def generate_medium_expression(self):
        """Added x^2 and multiplications like (x-3)(x+2)"""
        if random.random() < 0.6:  # 60% expanded polynomials
            return self.generate_expanded_polynomial()
        else:  # 40% products to expand
            return self.generate_product_expression()

    def generate_expanded_polynomial(self):
        """Polynomial with x^2 terms"""
        num_terms = random.randint(4, 6)
        terms = []
        
        for _ in range(num_terms):
            coef = random.randint(-6, 6)
            while coef == 0:
                coef = random.randint(-6, 6)
            
            power = random.choice([0, 1, 2])
            if power == 0:
                term = str(coef)
            elif power == 1:
                if coef == 1:
                    term = self.variable
                elif coef == -1:
                    term = f"-{self.variable}"
                else:
                    term = f"{coef}{self.variable}"
            else:  # power == 2
                if coef == 1:
                    term = f"{self.variable}^2"
                elif coef == -1:
                    term = f"-{self.variable}^2"
                else:
                    term = f"{coef}{self.variable}^2"
            
            terms.append(term)
        
        random.shuffle(terms)
        expression = terms[0]
        for term in terms[1:]:
            if term.startswith('-'):
                expression += f" - {term[1:]}"
            else:
                expression += f" + {term}"
        
        return expression

    def generate_product_expression(self):
        """Products like (x-3)(x+2) or 2(x+1)"""
        if random.random() < 0.7:  # 70% binomial products
            # (ax + b)(cx + d)
            a = random.choice([1, 1, 1, 2, 3])  # Mostly 1 for simplicity
            b = random.randint(-5, 5)
            c = random.choice([1, 1, 1, 2])
            d = random.randint(-5, 5)
            
            left = self.format_binomial(a, b)
            right = self.format_binomial(c, d)
            return f"({left})({right})"
        else:  # 30% monomial * binomial
            coef = random.randint(2, 4)
            a = random.choice([1, 1, 2])
            b = random.randint(-4, 4)
            
            binomial = self.format_binomial(a, b)
            return f"{coef}({binomial})"

    def generate_hard_expression(self):
        """Up to x^4 with parameters"""
        if random.random() < 0.5:  # 50% high degree polynomials
            return self.generate_high_degree_polynomial()
        elif random.random() < 0.7:  # 20% with parameters
            return self.generate_parametric_expression()
        else:  # 30% complex products
            return self.generate_complex_product()

    def generate_high_degree_polynomial(self):
        """Polynomials up to x^4"""
        num_terms = random.randint(4, 6)
        terms = []
        powers_used = set()
        
        for _ in range(num_terms):
            coef = random.randint(-5, 5)
            while coef == 0:
                coef = random.randint(-5, 5)
            
            power = random.choice([0, 1, 2, 3, 4])
            powers_used.add(power)
            
            if power == 0:
                term = str(coef)
            elif power == 1:
                if coef == 1:
                    term = self.variable
                elif coef == -1:
                    term = f"-{self.variable}"
                else:
                    term = f"{coef}{self.variable}"
            else:
                if coef == 1:
                    term = f"{self.variable}^{power}"
                elif coef == -1:
                    term = f"-{self.variable}^{power}"
                else:
                    term = f"{coef}{self.variable}^{power}"
            
            terms.append(term)
        
        # Ensure we have at least one high degree term
        if not any(power >= 3 for power in powers_used):
            coef = random.choice([1, -1, 2, -2])
            power = random.choice([3, 4])
            if coef == 1:
                terms.append(f"{self.variable}^{power}")
            elif coef == -1:
                terms.append(f"-{self.variable}^{power}")
            else:
                terms.append(f"{coef}{self.variable}^{power}")
        
        random.shuffle(terms)
        expression = terms[0]
        for term in terms[1:]:
            if term.startswith('-'):
                expression += f" - {term[1:]}"
            else:
                expression += f" + {term}"
        
        return expression

    def generate_parametric_expression(self):
        """Polynomials with symbolic parameters"""
        num_terms = random.randint(3, 5)
        terms = []
        parameters = random.sample(['a', 'b', 'c', 'k', 'm'], 2)
        
        for _ in range(num_terms):
            # Coefficient can be numeric or parametric
            if random.random() < 0.6:
                coef = random.randint(-4, 4)
                while coef == 0:
                    coef = random.randint(-4, 4)
                coef_str = str(coef)
            else:
                coef_str = random.choice(parameters)
            
            power = random.choice([0, 1, 2, 3])
            if power == 0:
                term = coef_str
            elif power == 1:
                term = f"{coef_str}{self.variable}"
            else:
                term = f"{coef_str}{self.variable}^{power}"
            
            terms.append(term)
        
        # Add a product with parameter
        if random.random() < 0.5:
            param = random.choice(parameters)
            a = random.randint(1, 3)
            b = random.randint(-3, 3)
            binomial = self.format_binomial(a, b)
            terms.append(f"{param}({binomial})")
        
        random.shuffle(terms)
        expression = terms[0]
        for term in terms[1:]:
            if term.startswith('-'):
                expression += f" - {term[1:]}"
            else:
                expression += f" + {term}"
        
        return expression

    def generate_complex_product(self):
        """Complex products like (x^2 + 2x - 1)(x - 3)"""
        if random.random() < 0.6:  # 60% quadratic * linear
            # (ax^2 + bx + c)(dx + e)
            a = random.choice([1, 1, 1, 2])
            b = random.randint(-3, 3)
            c = random.randint(-3, 3)
            d = random.choice([1, 1, 2])
            e = random.randint(-3, 3)
            
            left = self.format_quadratic(a, b, c)
            right = self.format_binomial(d, e)
            return f"({left})({right})"
        else:  # 40% three binomials
            a1, b1 = random.randint(1, 2), random.randint(-3, 3)
            a2, b2 = random.randint(1, 2), random.randint(-3, 3)
            a3, b3 = random.randint(1, 2), random.randint(-3, 3)
            
            bin1 = self.format_binomial(a1, b1)
            bin2 = self.format_binomial(a2, b2)
            bin3 = self.format_binomial(a3, b3)
            return f"({bin1})({bin2})({bin3})"

    def format_binomial(self, a, b):
        """Format ax + b as a binomial"""
        if a == 1:
            left_part = self.variable
        else:
            left_part = f"{a}{self.variable}"
        
        if b == 0:
            return left_part
        elif b > 0:
            return f"{left_part} + {b}"
        else:
            return f"{left_part} - {abs(b)}"

    def format_quadratic(self, a, b, c):
        """Format ax^2 + bx + c"""
        parts = []
        
        if a == 1:
            parts.append(f"{self.variable}^2")
        elif a == -1:
            parts.append(f"-{self.variable}^2")
        else:
            parts.append(f"{a}{self.variable}^2")
        
        if b != 0:
            if b == 1:
                parts.append(f"+ {self.variable}")
            elif b == -1:
                parts.append(f"- {self.variable}")
            elif b > 0:
                parts.append(f"+ {b}{self.variable}")
            else:
                parts.append(f"- {abs(b)}{self.variable}")
        
        if c != 0:
            if c > 0:
                parts.append(f"+ {c}")
            else:
                parts.append(f"- {abs(c)}")
        
        return " ".join(parts)

    def question_text(self):
        templates = [
            f"Simplify the expression: {self.expression}",
            f"Simplify: {self.expression}",
            f"Write {self.expression} in simplest form.",
            f"Simplify the following polynomial expression: {self.expression}",
            f"Reduce {self.expression} to its simplest form.",
            f"Express {self.expression} in simplified form.",
            f"Expand and simplify: {self.expression}",
            f"Simplify the polynomial: {self.expression}"
        ]
        return random.choice(templates)

    def generate_json(self):
        base_json = super().generate_json()
        base_json.update({
            "variable": self.variable,
            "expression": self.expression
        })
        return base_json
