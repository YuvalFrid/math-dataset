from .base import WordProblem
import random

class Generate_Percentage_Problem(WordProblem):
    def __init__(self):
        super().__init__(problem_type="percentages")
        self.templates = PercentageTemplates()

    def generate_question(self, level="easy"):
        self.level = level
        self.question, self.lhs, self.rhs, self.variable = self.generate_percentage_problem(level)
        self.json = self.generate_json()
        return self.question, self.json

    def generate_percentage_problem(self, level):
        if level == "easy":
            return self.generate_easy_percentage()
        elif level == "medium":
            return self.generate_medium_percentage()
        else:  # hard
            return self.generate_hard_percentage()

    def generate_easy_percentage(self):
        """Basic percentage of a number - find the part"""
        number = random.randint(10, 200)
        percentage = random.choice([10, 15, 20, 25, 30, 40, 50, 60, 75, 80, 90])
        variable = random.choice(["amount", "discount", "tax", "result", "value"])
        
        template = self.templates.get_template("percentage_of")
        question = template.format(number=number, percentage=percentage, variable=variable)
        
        lhs = variable
        rhs = f"{number} * {percentage}/100"
        
        return question, lhs, rhs, variable

    def generate_medium_percentage(self):
        """Percentage increase/decrease - find new value"""
        number = random.randint(50, 500)
        percentage = random.randint(5, 95)
        change_type = random.choice(["increase", "decrease"])
        variable = random.choice(["new_price", "new_salary", "new_population", "final_value"])
        
        template = self.templates.get_percentage_change_template(change_type)
        question = template.format(number=number, percentage=percentage, variable=variable)
        
        lhs = variable
        if change_type == "increase":
            rhs = f"{number} * (1 + {percentage}/100)"
        else:
            rhs = f"{number} * (1 - {percentage}/100)"
        
        return question, lhs, rhs, variable

    def generate_hard_percentage(self):
        """Reverse percentage or multiple changes"""
        if random.random() < 0.6:  # 60% reverse percentage
            return self.generate_reverse_percentage()
        else:  # 40% multiple changes
            return self.generate_multiple_changes()

    def generate_reverse_percentage(self):
        """Find original value given final value and percentage change"""
        final_value = random.randint(100, 1000)
        percentage = random.randint(10, 50)
        change_type = random.choice(["increase", "decrease"])
        variable = random.choice(["original_price", "original_value", "starting_amount"])
        
        template = self.templates.get_reverse_percentage_template(change_type)
        question = template.format(final_value=final_value, percentage=percentage, variable=variable)
        
        lhs = variable
        if change_type == "increase":
            rhs = f"{final_value} / (1 + {percentage}/100)"
        else:
            rhs = f"{final_value} / (1 - {percentage}/100)"
        
        return question, lhs, rhs, variable

    def generate_multiple_changes(self):
        """Multiple percentage changes in sequence"""
        number = random.randint(100, 500)
        p1 = random.randint(10, 30)
        p2 = random.randint(10, 30)
        variable = random.choice(["final_price", "result", "total"])
        
        template = self.templates.get_multiple_change_template()
        question = template.format(number=number, p1=p1, p2=p2, variable=variable)
        
        lhs = variable
        rhs = f"{number} * (1 + {p1}/100) * (1 - {p2}/100)"  # Increase then decrease
        
        return question, lhs, rhs, variable

    def generate_json(self):
        base_json = super().generate_json()
        base_json.update({
            "variable": self.variable,
            "lhs": self.lhs,
            "rhs": self.rhs
        })
        return base_json


class PercentageTemplates:
    def __init__(self):
        self.operations = {
            "percentage_of": self._percentage_of_templates(),
            "percentage_increase": self._percentage_change_templates("increase"),
            "percentage_decrease": self._percentage_change_templates("decrease"),
            "reverse_percentage": self._reverse_percentage_templates(),
            "multiple_changes": self._multiple_change_templates()
        }
    
    def get_template(self, operation):
        return random.choice(self.operations[operation])
    
    def get_percentage_change_template(self, change_type):
        return self.get_template(f"percentage_{change_type}")
    
    def get_reverse_percentage_template(self, change_type):
        templates = self.operations["reverse_percentage"]
        return random.choice([t for t in templates if change_type in t or "changed" in t])
    
    def get_multiple_change_template(self):
        return self.get_template("multiple_changes")

    def _percentage_of_templates(self):
        return [
            "What is {percentage}% of {number}? Let {variable} be the answer.",
            "Calculate {percentage}% of {number}. Use {variable} for the result.",
            "Find {percentage}% of {number}. Call the answer {variable}.",
            "A shirt costs ${number}. There's a {percentage}% discount. How much is taken off? Let {variable} be the discount amount.",
            "In a class of {number} students, {percentage}% are absent. How many are absent? Use {variable} for the number absent.",
            "The sales tax is {percentage}%. How much tax on a ${number} purchase? Let {variable} be the tax amount."
        ]

    def _percentage_change_templates(self, change_type):
        change_words = {
            "increase": ["increase", "raise", "growth", "go up", "rise"],
            "decrease": ["decrease", "reduction", "drop", "go down", "fall", "discount"]
        }
        words = change_words[change_type]
        
        templates = []
        for word in words:
            templates.extend([
                f"A price of ${number} has a {word} of {percentage}%. What is the new price? Use {variable} for the new price.",
                f"A salary of ${number} gets a {word} of {percentage}%. What is the new salary? Let {variable} be the new salary.",
                f"A population of {number} has a {word} of {percentage}%. What is the new population? Call it {variable}.",
                f"After a {word} of {percentage}%, a value becomes what? It was originally {number}. Use {variable} for the new value.",
                f"If something {word}s by {percentage}% from {number}, what is the result? Let {variable} be the final amount."
            ])
        return templates

    def _reverse_percentage_templates(self):
        return [
            "After a {percentage}% increase, the price is ${final_value}. What was the original price? Use {variable} for the original price.",
            "A number increased by {percentage}% is now {final_value}. What was it originally? Let {variable} be the original value.",
            "If something becomes {final_value} after a {percentage}% increase, what was it before? Use {variable} for the original amount.",
            "After a {percentage}% discount, the price is ${final_value}. What was the original price? Let {variable} be the original price.",
            "A number decreased by {percentage}% is now {final_value}. What was it originally? Use {variable} for the original value.",
            "The price ${final_value} includes a {percentage}% tax. What is the pre-tax price? Let {variable} be the pre-tax price."
        ]

    def _multiple_change_templates(self):
        return [
            "A price of ${number} increases by {p1}% then decreases by {p2}%. What is the final price? Use {variable} for the final price.",
            "A number goes up by {p1}% then down by {p2}%. Starting from {number}, what is the result? Let {variable} be the final value.",
            "First increase {number} by {p1}%, then decrease the result by {p2}%. What is the final value? Use {variable} for the answer.",
            "A product costs ${number}. The price rises by {p1}% then falls by {p2}%. What is the new price? Let {variable} be the new price."
        ]
