from .base import CalculusProblem
import random

class Generate_Exponential_Derivative(CalculusProblem):
    def __init__(self):
        super().__init__(problem_type="derivative.exponential")
        self.templates = ExponentialTemplates()

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
        """Generate exponential expression based on difficulty level"""
        if level == "easy":
            return self.generate_easy_expression()
        elif level == "medium":
            return self.generate_medium_expression()
        else:  # hard
            return self.generate_hard_expression()

    def generate_easy_expression(self):
        """Single exponential term: a*e^(bx) or a*b^x"""
        if random.random() < 0.7:  # 70% natural exponential
            outer_coef = random.randint(1, 3)
            inner_coef = random.randint(1, 3)
            
            if outer_coef == 1:
                return f"e^({inner_coef}{self.variable})"
            else:
                return f"{outer_coef}e^({inner_coef}{self.variable})"
        else:  # 30% general exponential
            base = random.randint(2, 5)
            outer_coef = random.randint(1, 3)
            inner_coef = random.randint(1, 3)
            
            if outer_coef == 1:
                return f"{base}^({inner_coef}{self.variable})"
            else:
                return f"{outer_coef} * {base}^({inner_coef}{self.variable})"

    def generate_medium_expression(self):
        """Sums of exponentials and exponentials with powers"""
        if random.random() < 0.6:  # 60% sums
            num_terms = random.randint(2, 3)
            terms = []
            
            for _ in range(num_terms):
                if random.random() < 0.7:  # natural exponential
                    outer_coef = random.randint(1, 3)
                    inner_coef = random.randint(1, 3)
                    terms.append(("e", outer_coef, inner_coef))
                else:  # general exponential
                    base = random.randint(2, 4)
                    outer_coef = random.randint(1, 3)
                    inner_coef = random.randint(1, 3)
                    terms.append((base, outer_coef, inner_coef))
            
            return self.format_exponential_sum(terms)
        else:  # 40% exponentials with powers
            if random.random() < 0.7:  # natural exponential
                outer_coef = random.randint(1, 3)
                inner_coef = random.randint(1, 3)
                power = random.randint(2, 3)
                
                if outer_coef == 1:
                    return f"(e^({inner_coef}{self.variable}))^{power}"
                else:
                    return f"{outer_coef}(e^({inner_coef}{self.variable}))^{power}"
            else:  # general exponential
                base = random.randint(2, 4)
                outer_coef = random.randint(1, 3)
                inner_coef = random.randint(1, 3)
                power = random.randint(2, 3)
                
                if outer_coef == 1:
                    return f"({base}^({inner_coef}{self.variable}))^{power}"
                else:
                    return f"{outer_coef}({base}^({inner_coef}{self.variable}))^{power}"

    def generate_hard_expression(self):
        """Products, quotients, chain rule, and mixed operations with exponentials"""
        problem_type = random.choice(["product", "quotient", "chain", "mixed"])
        
        if problem_type == "product":
            # exponential * exponential or exponential * poly/trig
            if random.random() < 0.5:  # exp * exp
                type1 = "e" if random.random() < 0.7 else random.randint(2, 4)
                type2 = "e" if random.random() < 0.7 else random.randint(2, 4)
                coef1, inner1 = random.randint(1, 3), random.randint(1, 3)
                coef2, inner2 = random.randint(1, 3), random.randint(1, 3)
                
                left_expr = self.format_single_exponential(type1, coef1, inner1)
                right_expr = self.format_single_exponential(type2, coef2, inner2)
                return f"({left_expr}) * ({right_expr})"
            else:  # exp * poly/trig
                exp_type = "e" if random.random() < 0.7 else random.randint(2, 4)
                exp_coef, exp_inner = random.randint(1, 3), random.randint(1, 3)
                other_func = random.choice([f"{self.variable}", f"{self.variable}^2", f"sin({self.variable})", f"cos({self.variable})"])
                
                exp_expr = self.format_single_exponential(exp_type, exp_coef, exp_inner)
                return f"({exp_expr}) * ({other_func})"
            
        elif problem_type == "quotient":
            # exponential / exponential or exponential / poly/trig
            if random.random() < 0.5:  # exp / exp
                num_type = "e" if random.random() < 0.7 else random.randint(2, 4)
                den_type = "e" if random.random() < 0.7 else random.randint(2, 4)
                num_coef, num_inner = random.randint(1, 3), random.randint(1, 3)
                den_coef, den_inner = random.randint(1, 3), random.randint(1, 3)
                
                num_expr = self.format_single_exponential(num_type, num_coef, num_inner)
                den_expr = self.format_single_exponential(den_type, den_coef, den_inner)
                return f"({num_expr}) / ({den_expr})"
            else:  # exp / poly or poly / exp
                if random.random() < 0.5:  # exp / poly
                    exp_type = "e" if random.random() < 0.7 else random.randint(2, 4)
                    exp_coef, exp_inner = random.randint(1, 3), random.randint(1, 3)
                    poly = random.choice([f"{self.variable}", f"{self.variable}^2", f"2{self.variable} + 1"])
                    
                    exp_expr = self.format_single_exponential(exp_type, exp_coef, exp_inner)
                    return f"({exp_expr}) / ({poly})"
                else:  # poly / exp
                    poly = random.choice([f"{self.variable}", f"{self.variable}^2", f"3{self.variable} - 2"])
                    exp_type = "e" if random.random() < 0.7 else random.randint(2, 4)
                    exp_coef, exp_inner = random.randint(1, 3), random.randint(1, 3)
                    
                    exp_expr = self.format_single_exponential(exp_type, exp_coef, exp_inner)
                    return f"({poly}) / ({exp_expr})"
            
        elif problem_type == "chain":
            # exponential of function or function of exponential
            if random.random() < 0.5:  # exponential of function
                exp_type = "e" if random.random() < 0.7 else random.randint(2, 4)
                inner_func = random.choice([f"{self.variable}^2", f"sin({self.variable})", f"cos({self.variable})", f"2{self.variable} + 1"])
                
                if exp_type == "e":
                    return f"e^({inner_func})"
                else:
                    return f"{exp_type}^({inner_func})"
            else:  # function of exponential
                outer_func = random.choice([f"{self.variable}^2", f"sin({self.variable})", f"cos({self.variable})"])
                exp_type = "e" if random.random() < 0.7 else random.randint(2, 4)
                exp_inner = random.randint(1, 3)
                
                exp_expr = f"e^({exp_inner}{self.variable})" if exp_type == "e" else f"{exp_type}^({exp_inner}{self.variable})"
                return f"{outer_func.replace(self.variable, exp_expr)}"
            
        else:  # mixed - multiple operations
            term1_type = "e" if random.random() < 0.7 else random.randint(2, 4)
            term2_type = "e" if random.random() < 0.7 else random.randint(2, 4)
            coef1, inner1 = random.randint(1, 2), random.randint(1, 2)
            coef2, inner2 = random.randint(1, 2), random.randint(1, 2)
            
            term1 = self.format_single_exponential(term1_type, coef1, inner1)
            term2 = self.format_single_exponential(term2_type, coef2, inner2)
            
            return f"{term1} + {term2}"

    def format_single_exponential(self, exp_type, outer_coef, inner_coef):
        """Format a single exponential term"""
        if exp_type == "e":
            if outer_coef == 1:
                return f"e^({inner_coef}{self.variable})"
            else:
                return f"{outer_coef}e^({inner_coef}{self.variable})"
        else:
            if outer_coef == 1:
                return f"{exp_type}^({inner_coef}{self.variable})"
            else:
                return f"{outer_coef} * {exp_type}^({inner_coef}{self.variable})"

    def format_exponential_sum(self, terms):
        """Format exponential sum into a string"""
        parts = []
        for exp_type, outer_coef, inner_coef in terms:
            if exp_type == "e":
                if outer_coef == 1:
                    parts.append(f"e^({inner_coef}{self.variable})")
                else:
                    parts.append(f"{outer_coef}e^({inner_coef}{self.variable})")
            else:
                if outer_coef == 1:
                    parts.append(f"{exp_type}^({inner_coef}{self.variable})")
                else:
                    parts.append(f"{outer_coef} * {exp_type}^({inner_coef}{self.variable})")
        
        return " + ".join(parts)

    def generate_json(self):
        base_json = super().generate_json()
        base_json.update({
            "variable": self.variable,
            "expression": self.expression
        })
        return base_json


class ExponentialTemplates:
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
