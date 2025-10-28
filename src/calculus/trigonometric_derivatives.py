from .base import CalculusProblem
import random

class Generate_Trigonometric_Derivative(CalculusProblem):
    def __init__(self):
        super().__init__(problem_type="derivative.trigonometric")
        self.templates = TrigonometricTemplates()

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
            return random.choice(["y", "t", "θ"])

    def generate_expression(self, level):
        """Generate trigonometric expression based on difficulty level"""
        if level == "easy":
            return self.generate_easy_expression()
        elif level == "medium":
            return self.generate_medium_expression()
        else:  # hard
            return self.generate_hard_expression()

    def generate_easy_expression(self):
        """Single trig function: a*sin(bx), a*cos(bx), a*tan(bx)"""
        trig_func = random.choice(["sin", "cos", "tan"])
        outer_coef = random.randint(1, 3)
        inner_coef = random.randint(1, 3)
        
        if outer_coef == 1:
            return f"{trig_func}({inner_coef}{self.variable})"
        else:
            return f"{outer_coef}{trig_func}({inner_coef}{self.variable})"

    def generate_medium_expression(self):
        """Sums of trig functions and trig functions with powers"""
        if random.random() < 0.6:  # 60% sums
            num_terms = random.randint(2, 3)
            terms = []
            
            for _ in range(num_terms):
                trig_func = random.choice(["sin", "cos", "tan"])
                outer_coef = random.randint(1, 3)
                inner_coef = random.randint(1, 3)
                terms.append((trig_func, outer_coef, inner_coef))
            
            return self.format_trig_sum(terms)
        else:  # 40% trig with powers
            trig_func = random.choice(["sin", "cos", "tan"])
            outer_coef = random.randint(1, 3)
            inner_coef = random.randint(1, 3)
            power = random.randint(2, 3)
            
            if outer_coef == 1:
                return f"{trig_func}({inner_coef}{self.variable})^{power}"
            else:
                return f"{outer_coef}{trig_func}({inner_coef}{self.variable})^{power}"

    def generate_hard_expression(self):
        """Products, quotients, chain rule, and mixed operations"""
        problem_type = random.choice(["product", "quotient", "chain", "mixed"])
        
        if problem_type == "product":
            # trig * trig or trig * poly
            func1 = random.choice(["sin", "cos"])
            func2 = random.choice(["sin", "cos", self.variable, f"{self.variable}^2"])
            coef1, inner1 = random.randint(1, 3), random.randint(1, 3)
            coef2, inner2 = random.randint(1, 3), random.randint(1, 3)
            
            left_expr = f"{coef1}{func1}({inner1}{self.variable})" if coef1 != 1 else f"{func1}({inner1}{self.variable})"
            
            if func2 in ["sin", "cos"]:
                right_expr = f"{coef2}{func2}({inner2}{self.variable})" if coef2 != 1 else f"{func2}({inner2}{self.variable})"
            else:
                right_expr = func2
                
            return f"({left_expr}) * ({right_expr})"
            
        elif problem_type == "quotient":
            # trig / trig or trig / poly
            num_func = random.choice(["sin", "cos", "tan"])
            den_func = random.choice(["sin", "cos", self.variable, f"{self.variable}^2"])
            num_coef, num_inner = random.randint(1, 3), random.randint(1, 3)
            den_coef, den_inner = random.randint(1, 3), random.randint(1, 3)
            
            num_expr = f"{num_coef}{num_func}({num_inner}{self.variable})" if num_coef != 1 else f"{num_func}({num_inner}{self.variable})"
            
            if den_func in ["sin", "cos"]:
                den_expr = f"{den_coef}{den_func}({den_inner}{self.variable})" if den_coef != 1 else f"{den_func}({den_inner}{self.variable})"
            else:
                den_expr = den_func
                
            return f"({num_expr}) / ({den_expr})"
            
        elif problem_type == "chain":
            # trig(poly) or poly(trig)
            if random.random() < 0.5:  # trig(poly)
                outer_func = random.choice(["sin", "cos", "tan"])
                inner_coef, inner_power = random.randint(1, 3), random.randint(2, 3)
                return f"{outer_func}({inner_coef}{self.variable}^{inner_power})"
            else:  # poly(trig)
                outer_coef, outer_power = random.randint(1, 3), random.randint(2, 3)
                inner_func = random.choice(["sin", "cos"])
                inner_coef = random.randint(1, 3)
                inner_expr = f"{inner_func}({inner_coef}{self.variable})"
                return f"({outer_coef}{inner_expr})^{outer_power}"
            
        else:  # mixed - multiple operations
            func1, func2 = random.choice(["sin", "cos"]), random.choice(["sin", "cos"])
            coef1, inner1 = random.randint(1, 2), random.randint(1, 2)
            coef2, inner2 = random.randint(1, 2), random.randint(1, 2)
            
            term1 = f"{coef1}{func1}({inner1}{self.variable})" if coef1 != 1 else f"{func1}({inner1}{self.variable})"
            term2 = f"{coef2}{func2}({inner2}{self.variable})" if coef2 != 1 else f"{func2}({inner2}{self.variable})"
            
            return f"{term1} + {term2}"

    def format_trig_sum(self, terms):
        """Format trigonometric sum into a string"""
        parts = []
        for trig_func, outer_coef, inner_coef in terms:
            if outer_coef == 1:
                part = f"{trig_func}({inner_coef}{self.variable})"
            else:
                part = f"{outer_coef}{trig_func}({inner_coef}{self.variable})"
            parts.append(part)
        
        return " + ".join(parts)

    def generate_json(self):
        base_json = super().generate_json()
        base_json.update({
            "variable": self.variable,
            "expression": self.expression
        })
        return base_json


class TrigonometricTemplates:
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
