from .base import WordProblem
import random

class Generate_Age_Problem(WordProblem):
    def __init__(self):
        super().__init__(problem_type="word_problems.age")
        self.templates = AgeTemplates()

    def generate_question(self, level="easy"):
        self.level = level
        self.question, self.context = self.generate_age_problem(level)
        self.json = self.generate_json()
        return self.question, self.json

    def generate_age_problem(self, level):
        if level == "easy":
            return self.generate_easy_age()
        elif level == "medium":
            return self.generate_medium_age()
        else:  # hard
            return self.generate_hard_age()

    def generate_easy_age(self):
        """Simple age relationships - current ages"""
        person1_age = random.randint(10, 40)
        person2_age = random.randint(10, 40)
        relationship = random.choice(["older", "younger"])
        difference = abs(person1_age - person2_age)
        
        if relationship == "older":
            older, younger = (person1_age, person2_age) if person1_age > person2_age else (person2_age, person1_age)
            template = self.templates.get_template("current_ages_older")
            question = template.format(older=older, younger=younger, diff=difference)
            context = {
                "operation": "current_ages_difference",
                "older_age": older,
                "younger_age": younger,
                "difference": difference,
                "relationship": "older"
            }
        else:
            older, younger = (person1_age, person2_age) if person1_age > person2_age else (person2_age, person1_age)
            template = self.templates.get_template("current_ages_younger")
            question = template.format(older=older, younger=younger, diff=difference)
            context = {
                "operation": "current_ages_difference", 
                "older_age": older,
                "younger_age": younger,
                "difference": difference,
                "relationship": "younger"
            }
        
        return question, context

    def generate_medium_age(self):
        """Age problems involving time shifts - past or future"""
        current_age = random.randint(20, 50)
        years_shift = random.randint(5, 20)
        relationship = random.choice(["past", "future"])
        
        if relationship == "past":
            past_age = current_age - years_shift
            template = self.templates.get_template("time_shift_past")
            question = template.format(current=current_age, years=years_shift, past=past_age)
            context = {
                "operation": "time_shift",
                "current_age": current_age,
                "years_shift": years_shift,
                "shift_direction": "past",
                "other_age": past_age
            }
        else:  # future
            future_age = current_age + years_shift
            template = self.templates.get_template("time_shift_future")
            question = template.format(current=current_age, years=years_shift, future=future_age)
            context = {
                "operation": "time_shift",
                "current_age": current_age,
                "years_shift": years_shift,
                "shift_direction": "future", 
                "other_age": future_age
            }
        
        return question, context

    def generate_hard_age(self):
        """Complex age relationships with multiple people and equations"""
        problem_type = random.choice(["ratio_ages", "sum_ages", "multiple_times"])
        
        if problem_type == "ratio_ages":
            age1 = random.randint(10, 30)
            age2 = random.randint(10, 30)
            ratio_num = random.randint(2, 4)
            ratio_den = random.randint(1, 3)
            
            template = self.templates.get_template("ratio_ages")
            question = template.format(age1=age1, age2=age2, num=ratio_num, den=ratio_den)
            context = {
                "operation": "ratio_ages",
                "age1": age1,
                "age2": age2,
                "ratio_numerator": ratio_num,
                "ratio_denominator": ratio_den
            }
            
        elif problem_type == "sum_ages":
            total_age = random.randint(40, 100)
            num_people = random.randint(2, 4)
            template = self.templates.get_template("sum_ages")
            question = template.format(total=total_age, num=num_people)
            context = {
                "operation": "sum_ages",
                "total_age": total_age,
                "number_people": num_people
            }
            
        else:  # multiple_times
            years_ago = random.randint(5, 15)
            years_later = random.randint(5, 15)
            template = self.templates.get_template("multiple_times")
            question = template.format(ago=years_ago, later=years_later)
            context = {
                "operation": "multiple_time_periods",
                "years_ago": years_ago,
                "years_later": years_later
            }
        
        return question, context

    def generate_json(self):
        base_json = super().generate_json()
        if hasattr(self, 'context'):
            base_json.update(self.context)
        return base_json


class AgeTemplates:
    def __init__(self):
        self.operations = {
            "current_ages_older": self._current_ages_older_templates(),
            "current_ages_younger": self._current_ages_younger_templates(),
            "time_shift_past": self._time_shift_past_templates(),
            "time_shift_future": self._time_shift_future_templates(),
            "ratio_ages": self._ratio_ages_templates(),
            "sum_ages": self._sum_ages_templates(),
            "multiple_times": self._multiple_times_templates()
        }
    
    def get_template(self, operation):
        return random.choice(self.operations[operation])

    def _current_ages_older_templates(self):
        return [
            "John is {older} years old. Mary is {younger} years old. How much older is John than Mary?",
            "If Person A is {older} and Person B is {younger}, what is their age difference?",
            "The older person is {older} years, the younger is {younger}. What is the age gap?",
            "Age difference between {older} and {younger} is?",
            "How many years older is someone aged {older} compared to someone aged {younger}?",
            "Calculate the age difference: {older} years vs {younger} years.",
            "What is the gap between ages {older} and {younger}?",
            "If one person is {older} and another is {younger}, how much older is the first?",
            "Determine the age difference between {older} years and {younger} years.",
            "The age of the older person is {older}, the younger is {younger}. Difference?"
        ]

    def _current_ages_younger_templates(self):
        return [
            "Sarah is {younger} years old. Tom is {older} years old. How much younger is Sarah than Tom?",
            "If Person X is {younger} and Person Y is {older}, how much younger is X?",
            "The younger person is {younger} years, the older is {older}. How much younger?",
            "How many years younger is someone aged {younger} compared to someone aged {older}?",
            "Calculate how much younger: {younger} years vs {older} years.",
            "What is the younger gap between ages {younger} and {older}?",
            "If the younger is {younger} and older is {older}, how much younger?",
            "Determine how much younger {younger} is compared to {older}.",
            "The age of the younger person is {younger}, the older is {older}. Younger by?",
            "How much younger is a {younger}-year-old than an {older}-year-old?"
        ]

    def _time_shift_past_templates(self):
        return [
            "John is now {current} years old. How old was he {years} years ago?",
            "If someone is {current} now, what was their age {years} years back?",
            "Current age is {current}. What was the age {years} years in the past?",
            "A person aged {current} now. How old were they {years} years ago?",
            "Calculate the age {years} years ago from current age {current}.",
            "From current age {current}, find the age {years} years before.",
            "If present age is {current}, what was it {years} years earlier?",
            "Determine the past age: {years} years ago from now age {current}.",
            "What age was someone {years} years ago if they are {current} now?",
            "Current age: {current}. Age {years} years in the past?"
        ]

    def _time_shift_future_templates(self):
        return [
            "Mary is now {current} years old. How old will she be in {years} years?",
            "If someone is {current} now, what will their age be in {years} years?",
            "Current age is {current}. What will be the age in {years} years?",
            "A person aged {current} now. How old in {years} years?",
            "Calculate the age in {years} years from current age {current}.",
            "From current age {current}, find the age after {years} years.",
            "If present age is {current}, what will it be in {years} years?",
            "Determine the future age: in {years} years from now age {current}.",
            "What age will someone be in {years} years if they are {current} now?",
            "Current age: {current}. Age in {years} years?"
        ]

    def _ratio_ages_templates(self):
        return [
            "The ratio of John's age to Mary's age is {num}:{den}. If John is {age1} and Mary is {age2}, verify the ratio.",
            "Check if ages {age1} and {age2} are in ratio {num}:{den}.",
            "Are the ages {age1} and {age2} in the ratio {num} to {den}?",
            "Verify that {age1} and {age2} form the ratio {num}:{den}.",
            "Do the ages {age1} and {age2} satisfy the ratio {num}:{den}?",
            "Check the ratio {num}:{den} for ages {age1} and {age2}.",
            "Are {age1} and {age2} in proportion {num}:{den}?",
            "Verify the age ratio {num}:{den} with values {age1} and {age2}.",
            "Do these ages maintain ratio {num}:{den}: {age1} and {age2}?",
            "Check if {age1} and {age2} are in the ratio of {num} to {den}."
        ]

    def _sum_ages_templates(self):
        return [
            "The sum of ages of {num} people is {total}. If they are all different ages, what could their ages be?",
            "Total age of {num} individuals is {total}. Find possible ages.",
            "If {num} people have combined age {total}, what might their ages be?",
            "The ages of {num} people add up to {total}. Determine possible ages.",
            "Sum of {num} ages is {total}. Find age combinations.",
            "Combined age of {num} persons is {total}. What are possible ages?",
            "If total age for {num} people is {total}, find age distribution.",
            "The ages of {num} individuals sum to {total}. Possible values?",
            "{num} people have total age {total}. What could each age be?",
            "Find ages for {num} people with total age {total}."
        ]

    def _multiple_times_templates(self):
        return [
            "John's age {ago} years ago compared to his age in {later} years.",
            "A person's age {ago} years ago and {later} years from now.",
            "The relationship between age {ago} years past and {later} years future.",
            "Compare age {ago} years before with age {later} years after.",
            "Age difference between {ago} years ago and {later} years later.",
            "The age {ago} years in the past vs {later} years in the future.",
            "Connection between age {ago} years back and {later} years ahead.",
            "How age {ago} years ago relates to age in {later} years.",
            "The progression from {ago} years ago to {later} years hence.",
            "Age transformation from {ago} years past to {later} years future."
        ]
