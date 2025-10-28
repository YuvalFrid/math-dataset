from .base import CalculusProblem
import random

class Generate_Logarithmic_Derivative(CalculusProblem):
    def __init__(self):
        super().__init__(problem_type="derivative.logarithmic")
        self.templates = LogarithmicTemplates()

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
        """Generate logarithmic expression based on difficulty level"""
        if level == "easy":
            return self.generate_easy_expression()
        elif level == "medium":
            return self.generate_medium_expression()
        else:  # hard
            return self.generate_hard_expression()

    def generate_easy_expression(self):
        """Single logarithmic term: a*ln(bx) or a*log_c(bx)"""
        if random.random() < 0.7:  # 70% natural log
            outer_coef = random.randint(1, 3)
            inner_coef = random.randint(1, 3)
            
            if outer_coef == 1:
                return f"ln({inner_coef}{self.variable})"
            else:
                return f"{outer_coef}ln({inner_coef}{self.variable})"
        else:  # 30% general log
            base = random.randint(2, 5)
            outer_coef = random.randint(1, 3)
            inner_coef = random.randint(1, 3)
            
            if outer_coef == 1:
                return f"log_{base}({inner_coef}{self.variable})"
            else:
                return f"{outer_coef}log_{base}({inner_coef}{self.variable})"

    def generate_medium_expression(self):
        """Sums of logs and logs with powers"""
        if random.random() < 0.6:  # 60% sums
            num_terms = random.randint(2, 3)
            terms = []
            
            for _ in range(num_terms):
                if random.random() < 0.7:  # natural log
                    outer_coef = random.randint(1, 3)
                    inner_coef = random.randint(1, 3)
                    terms.append(("ln", outer_coef, inner_coef))
                else:  # general log
                    base = random.randint(2, 4)
                    outer_coef = random.randint(1, 3)
                    inner_coef = random.randint(1, 3)
                    terms.append((f"log_{base}", outer_coef, inner_coef))
            
            return self.format_logarithmic_sum(terms)
        else:  # 40% logs with powers
            if random.random() < 0.7:  # natural log
                outer_coef = random.randint(1, 3)
                inner_coef = random.randint(1, 3)
                power = random.randint(2, 3)
                
                if outer_coef == 1:
                    return f"(ln({inner_coef}{self.variable}))^{power}"
                else:
                    return f"{outer_coef}(ln({inner_coef}{self.variable}))^{power}"
            else:  # general log
                base = random.randint(2, 4)
                outer_coef = random.randint(1, 3)
                inner_coef = random.randint(1, 3)
                power = random.randint(2, 3)
                
                if outer_coef == 1:
                    return f"(log_{base}({inner_coef}{self.variable}))^{power}"
                else:
                    return f"{outer_coef}(log_{base}({inner_coef}{self.variable}))^{power}"

    def generate_hard_expression(self):
        """Products, quotients, chain rule, and mixed operations with logarithms"""
        problem_type = random.choice(["product", "quotient", "chain", "mixed"])
        
        if problem_type == "product":
            # log * log or log * poly/trig
            if random.random() < 0.5:  # log * log
                type1 = "ln" if random.random() < 0.7 else f"log_{random.randint(2, 4)}"
                type2 = "ln" if random.random() < 0.7 else f"log_{random.randint(2, 4)}"
                coef1, inner1 = random.randint(1, 3), random.randint(1, 3)
                coef2, inner2 = random.randint(1, 3), random.randint(1, 3)
                
                left_expr = self.format_single_logarithmic(type1, coef1, inner1)
                right_expr = self.format_single_logarithmic(type2, coef2, inner2)
                return f"({left_expr}) * ({right_expr})"
            else:  # log * poly/trig
                log_type = "ln" if random.random() < 0.7 else f"log_{random.randint(2, 4)}"
                log_coef, log_inner = random.randint(1, 3), random.randint(1, 3)
                other_func = random.choice([f"{self.variable}", f"{self.variable}^2", f"sin({self.variable})", f"cos({self.variable})"])
                
                log_expr = self.format_single_logarithmic(log_type, log_coef, log_inner)
                return f"({log_expr}) * ({other_func})"
            
        elif problem_type == "quotient":
            # log / log or log / poly/trig
            if random.random() < 0.5:  # log / log
                num_type = "ln" if random.random() < 0.7 else f"log_{random.randint(2, 4)}"
                den_type = "ln" if random.random() < 0.7 else f"log_{random.randint(2, 4)}"
                num_coef, num_inner = random.randint(1, 3), random.randint(1, 3)
                den_coef, den_inner = random.randint(1, 3), random.randint(1, 3)
                
                num_expr = self.format_single_logarithmic(num_type, num_coef, num_inner)
                den_expr = self.format_single_logarithmic(den_type, den_coef, den_inner)
                return f"({num_expr}) / ({den_expr})"
            else:  # log / poly or poly / log
                if random.random() < 0.5:  # log / poly
                    log_type = "ln" if random.random() < 0.7 else f"log_{random.randint(2, 4)}"
                    log_coef, log_inner = random.randint(1, 3), random.randint(1, 3)
                    poly = random.choice([f"{self.variable}", f"{self.variable}^2", f"2{self.variable} + 1"])
                    
                    log_expr = self.format_single_logarithmic(log_type, log_coef, log_inner)
                    return f"({log_expr}) / ({poly})"
                else:  # poly / log
                    poly = random.choice([f"{self.variable}", f"{self.variable}^2", f"3{self.variable} - 2"])
                    log_type = "ln" if random.random() < 0.7 else f"log_{random.randint(2, 4)}"
                    log_coef, log_inner = random.randint(1, 3), random.randint(1, 3)
                    
                    log_expr = self.format_single_logarithmic(log_type, log_coef, log_inner)
                    return f"({poly}) / ({log_expr})"
            
        elif problem_type == "chain":
            # log of function or function of log
            if random.random() < 0.5:  # log of function
                log_type = "ln" if random.random() < 0.7 else f"log_{random.randint(2, 4)}"
                inner_func = random.choice([f"{self.variable}^2", f"sin({self.variable})", f"cos({self.variable})", f"2{self.variable} + 1", f"e^({self.variable})"])
                
                if log_type == "ln":
                    return f"ln({inner_func})"
                else:
                    return f"{log_type}({inner_func})"
            else:  # function of log
                outer_func = random.choice([f"{self.variable}^2", f"sin({self.variable})", f"cos({self.variable})"])
                log_type = "ln" if random.random() < 0.7 else f"log_{random.randint(2, 4)}"
                log_inner = random.randint(1, 3)
                
                log_expr = f"ln({log_inner}{self.variable})" if log_type == "ln" else f"{log_type}({log_inner}{self.variable})"
                return f"{outer_func.replace(self.variable, log_expr)}"
            
        else:  # mixed - multiple operations
            term1_type = "ln" if random.random() < 0.7 else f"log_{random.randint(2, 4)}"
            term2_type = "ln" if random.random() < 0.7 else f"log_{random.randint(2, 4)}"
            coef1, inner1 = random.randint(1, 2), random.randint(1, 2)
            coef2, inner2 = random.randint(1, 2), random.randint(1, 2)
            
            term1 = self.format_single_logarithmic(term1_type, coef1, inner1)
            term2 = self.format_single_logarithmic(term2_type, coef2, inner2)
            
            return f"{term1} + {term2}"

    def format_single_logarithmic(self, log_type, outer_coef, inner_coef):
        """Format a single logarithmic term"""
        if log_type == "ln":
            if outer_coef == 1:
                return f"ln({inner_coef}{self.variable})"
            else:
                return f"{outer_coef}ln({inner_coef}{self.variable})"
        else:
            if outer_coef == 1:
                return f"{log_type}({inner_coef}{self.variable})"
            else:
                return f"{outer_coef}{log_type}({inner_coef}{self.variable})"

    def format_logarithmic_sum(self, terms):
        """Format logarithmic sum into a string"""
        parts = []
        for log_type, outer_coef, inner_coef in terms:
            if log_type == "ln":
                if outer_coef == 1:
                    parts.append(f"ln({inner_coef}{self.variable})")
                else:
                    parts.append(f"{outer_coef}ln({inner_coef}{self.variable})")
            else:
                if outer_coef == 1:
                    parts.append(f"{log_type}({inner_coef}{self.variable})")
                else:
                    parts.append(f"{outer_coef}{log_type}({inner_coef}{self.variable})")
        
        return " + ".join(parts)

    def generate_json(self):
        base_json = super().generate_json()
        base_json.update({
            "variable": self.variable,
            "expression": self.expression
        })
        return base_json


class LogarithmicTemplates:
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
