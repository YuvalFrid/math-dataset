from .base import WordProblem
import random

class Generate_Mixture_Problem(WordProblem):
    def __init__(self):
        super().__init__(problem_type="word_problems.mixture")
        self.templates = MixtureTemplates()

    def generate_question(self, level="easy"):
        self.level = level
        self.question, self.context = self.generate_mixture_problem(level)
        self.json = self.generate_json()
        return self.question, self.json

    def generate_mixture_problem(self, level):
        if level == "easy":
            return self.generate_easy_mixture()
        elif level == "medium":
            return self.generate_medium_mixture()
        else:  # hard
            return self.generate_hard_mixture()

    def generate_easy_mixture(self):
        """Simple mixture problems - basic concentrations"""
        total_volume = random.randint(100, 500)
        concentration = random.randint(10, 40)
        substance = random.choice(["salt", "sugar", "acid", "alcohol"])
        
        template = self.templates.get_template("basic_concentration")
        question = template.format(total=total_volume, conc=concentration, sub=substance)
        
        context = {
            "operation": "basic_concentration",
            "total_volume": total_volume,
            "concentration": concentration,
            "substance": substance,
            "substance_amount": round(total_volume * concentration / 100, 2)
        }
        return question, context

    def generate_medium_mixture(self):
        """Two-component mixture problems"""
        volume1 = random.randint(100, 300)
        volume2 = random.randint(100, 300)
        conc1 = random.randint(10, 30)
        conc2 = random.randint(40, 80)
        substance = random.choice(["salt", "sugar", "acid"])
        
        template = self.templates.get_template("two_component_mixture")
        question = template.format(v1=volume1, c1=conc1, v2=volume2, c2=conc2, sub=substance)
        
        total_volume = volume1 + volume2
        total_substance = (volume1 * conc1/100) + (volume2 * conc2/100)
        final_concentration = round((total_substance / total_volume) * 100, 2)
        
        context = {
            "operation": "two_component_mixture",
            "volume1": volume1,
            "concentration1": conc1,
            "volume2": volume2, 
            "concentration2": conc2,
            "substance": substance,
            "total_volume": total_volume,
            "final_concentration": final_concentration
        }
        return question, context

    def generate_hard_mixture(self):
        """Complex mixture problems with removal/replacement or three components"""
        problem_type = random.choice(["removal_replacement", "three_components", "cost_mixture"])
        
        if problem_type == "removal_replacement":
            initial_volume = random.randint(200, 500)
            initial_conc = random.randint(20, 60)
            remove_volume = random.randint(50, 150)
            substance = random.choice(["salt", "acid"])
            
            template = self.templates.get_template("removal_replacement")
            question = template.format(vol=initial_volume, conc=initial_conc, remove=remove_volume, sub=substance)
            
            context = {
                "operation": "removal_replacement",
                "initial_volume": initial_volume,
                "initial_concentration": initial_conc,
                "removed_volume": remove_volume,
                "substance": substance
            }
            
        elif problem_type == "three_components":
            v1, v2, v3 = random.randint(50, 200), random.randint(50, 200), random.randint(50, 200)
            c1, c2, c3 = random.randint(10, 30), random.randint(40, 60), random.randint(70, 90)
            
            template = self.templates.get_template("three_components")
            question = template.format(v1=v1, c1=c1, v2=v2, c2=c2, v3=v3, c3=c3)
            
            total_volume = v1 + v2 + v3
            total_substance = (v1 * c1/100) + (v2 * c2/100) + (v3 * c3/100)
            final_conc = round((total_substance / total_volume) * 100, 2)
            
            context = {
                "operation": "three_component_mixture",
                "volumes": [v1, v2, v3],
                "concentrations": [c1, c2, c3],
                "total_volume": total_volume,
                "final_concentration": final_conc
            }
            
        else:  # cost_mixture
            price1 = random.randint(2, 8)
            price2 = random.randint(10, 20)
            final_price = random.randint(price1 + 2, price2 - 2)
            total_weight = random.randint(100, 500)
            
            template = self.templates.get_template("cost_mixture")
            question = template.format(p1=price1, p2=price2, fp=final_price, tw=total_weight)
            
            context = {
                "operation": "cost_mixture",
                "price1": price1,
                "price2": price2,
                "final_price": final_price,
                "total_weight": total_weight
            }
        
        return question, context

    def generate_json(self):
        base_json = super().generate_json()
        if hasattr(self, 'context'):
            base_json.update(self.context)
        return base_json


class MixtureTemplates:
    def __init__(self):
        self.operations = {
            "basic_concentration": self._basic_concentration_templates(),
            "two_component_mixture": self._two_component_mixture_templates(),
            "removal_replacement": self._removal_replacement_templates(),
            "three_components": self._three_components_templates(),
            "cost_mixture": self._cost_mixture_templates()
        }
    
    def get_template(self, operation):
        return random.choice(self.operations[operation])

    def _basic_concentration_templates(self):
        return [
            "A {total}ml solution contains {conc}% {sub}. How much {sub} is in the solution?",
            "What amount of {sub} is in {total}ml of {conc}% solution?",
            "Calculate the {sub} content in {total}ml at {conc}% concentration.",
            "How much {sub} in a {total}ml mixture that is {conc}% {sub}?",
            "A {conc}% {sub} solution has volume {total}ml. {sub} quantity?",
            "Find the {sub} mass in {total}ml of {conc}% solution.",
            "Determine {sub} amount in {total}ml with {conc}% concentration.",
            "What weight of {sub} in {total}ml of {conc}% mixture?",
            "Calculate {sub} content: {total}ml solution, {conc}% strength.",
            "How many grams of {sub} in {total}ml of {conc}% solution?"
        ]

    def _two_component_mixture_templates(self):
        return [
            "Mix {v1}ml of {c1}% {sub} with {v2}ml of {c2}% {sub}. What is the final concentration?",
            "Combine {v1}ml at {c1}% and {v2}ml at {c2}% {sub}. Final concentration?",
            "What concentration when mixing {v1}ml {c1}% {sub} and {v2}ml {c2}% {sub}?",
            "Blend {v1}ml of {c1}% {sub} solution with {v2}ml of {c2}% {sub} solution. Resulting strength?",
            "Mix {v1}ml ({c1}%) and {v2}ml ({c2}%) {sub} solutions. Final percentage?",
            "Combine {v1}ml {c1}% and {v2}ml {c2}% {sub}. What is the mixture concentration?",
            "Two solutions: {v1}ml at {c1}% and {v2}ml at {c2}% {sub}. Mixed concentration?",
            "Blending {v1}ml of {c1}% with {v2}ml of {c2}% {sub}. Final strength?",
            "What is the concentration after mixing {v1}ml {c1}% and {v2}ml {c2}% {sub}?",
            "Mix {v1}ml ({c1}%) and {v2}ml ({c2}%) {sub}. Determine final concentration."
        ]

    def _removal_replacement_templates(self):
        return [
            "A {vol}ml {sub} solution is {conc}%. If {remove}ml is removed and replaced with pure solvent, what happens?",
            "From {vol}ml of {conc}% {sub}, {remove}ml is taken out and replaced. Calculate new concentration.",
            "A {vol}ml {conc}% {sub} solution has {remove}ml removed and replaced. Find new strength.",
            "Remove {remove}ml from {vol}ml of {conc}% {sub} and replace with solvent. New concentration?",
            "Take out {remove}ml from {vol}ml {conc}% {sub} and add pure solvent. Resulting percentage?",
            "A {vol}ml {conc}% {sub} mixture: remove {remove}ml, replace with solvent. Final concentration?",
            "From {vol}ml {conc}% {sub}, discard {remove}ml and add solvent. New strength?",
            "Remove and replace {remove}ml from {vol}ml of {conc}% {sub}. What concentration now?",
            "Take {remove}ml out of {vol}ml {conc}% {sub}, replace with pure liquid. Final percentage?",
            "A {sub} solution: {vol}ml at {conc}%. After removing {remove}ml and replacing, concentration?"
        ]

    def _three_components_templates(self):
        return [
            "Mix {v1}ml of {c1}% solution, {v2}ml of {c2}% solution, and {v3}ml of {c3}% solution. What is the final concentration?",
            "Combine three solutions: {v1}ml at {c1}%, {v2}ml at {c2}%, and {v3}ml at {c3}%. Overall concentration?",
            "Blend {v1}ml ({c1}%), {v2}ml ({c2}%), and {v3}ml ({c3}%). What is the mixture strength?",
            "Three components: {v1}ml {c1}%, {v2}ml {c2}%, {v3}ml {c3}%. Mixed concentration?",
            "Mix together {v1}ml of {c1}%, {v2}ml of {c2}%, and {v3}ml of {c3}%. Final percentage?",
            "Combine {v1}ml at {c1}%, {v2}ml at {c2}%, {v3}ml at {c3}%. Resulting concentration?",
            "Blend three solutions: {v1}ml {c1}%, {v2}ml {c2}%, {v3}ml {c3}%. What strength?",
            "Mix {v1}ml ({c1}%), {v2}ml ({c2}%), {v3}ml ({c3}%). Determine final concentration.",
            "Three-part mixture: {v1}ml {c1}%, {v2}ml {c2}%, {v3}ml {c3}%. Overall percentage?",
            "Combine {v1}ml of {c1}%, {v2}ml of {c2}%, and {v3}ml of {c3}%. Final mixture strength?"
        ]

    def _cost_mixture_templates(self):
        return [
            "Mix two items costing ${p1}/kg and ${p2}/kg to get a mixture worth ${fp}/kg. For {tw}kg total, find the ratio.",
            "Blend materials at ${p1}/kg and ${p2}/kg to make {tw}kg worth ${fp}/kg. What proportions?",
            "Combine ${p1}/kg and ${p2}/kg components for {tw}kg mixture at ${fp}/kg. Find the mix ratio.",
            "Two ingredients: ${p1}/kg and ${p2}/kg. Make {tw}kg at ${fp}/kg. Determine amounts.",
            "Mix ${p1}/kg and ${p2}/kg to produce {tw}kg worth ${fp}/kg. Calculate the blend.",
            "Blend ${p1}/kg and ${p2}/kg materials for {tw}kg at ${fp}/kg. Find the combination.",
            "Combine ${p1}/kg and ${p2}/kg to get {tw}kg mixture priced at ${fp}/kg. Ratio?",
            "Two components: ${p1}/kg and ${p2}/kg. Create {tw}kg at ${fp}/kg. Mixture proportions?",
            "Mix ${p1}/kg and ${p2}/kg for {tw}kg total worth ${fp}/kg. What is the blend?",
            "Blend ${p1}/kg and ${p2}/kg to make {tw}kg costing ${fp}/kg. Determine the mix."
        ]
