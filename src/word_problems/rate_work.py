from .base import WordProblem
import random

class Generate_Rate_Work_Problem(WordProblem):
    def __init__(self):
        super().__init__(problem_type="rate_work")
        self.templates = RateWorkTemplates()

    def generate_question(self, level="easy"):
        self.level = level
        self.question, self.lhs, self.rhs, self.variable = self.generate_rate_problem(level)
        self.json = self.generate_json()
        return self.question, self.json

    def generate_rate_problem(self, level):
        if level == "easy":
            return self.generate_easy_rate()
        elif level == "medium":
            return self.generate_medium_rate()
        else:  # hard
            return self.generate_hard_rate()

    def generate_easy_rate(self):
        """Simple rate problems - distance = rate × time"""
        operation = random.choice(["find_speed", "find_distance", "find_time"])
        
        if operation == "find_speed":
            distance = random.randint(100, 500)
            time = random.randint(2, 8)
            variable = "speed"
            
            template = self.templates.get_template("find_speed")
            question = template.format(distance=distance, time=time, variable=variable)
            
            lhs = variable
            rhs = f"{distance} / {time}"
            
        elif operation == "find_distance":
            speed = random.randint(40, 80)
            time = random.randint(2, 6)
            variable = "distance"
            
            template = self.templates.get_template("find_distance")
            question = template.format(speed=speed, time=time, variable=variable)
            
            lhs = variable
            rhs = f"{speed} * {time}"
            
        else:  # find_time
            distance = random.randint(200, 600)
            speed = random.randint(50, 90)
            variable = "time"
            
            template = self.templates.get_template("find_time")
            question = template.format(distance=distance, speed=speed, variable=variable)
            
            lhs = variable
            rhs = f"{distance} / {speed}"
        
        return question, lhs, rhs, variable

    def generate_medium_rate(self):
        """Combined rates and work problems"""
        operation = random.choice(["combined_rates", "work_together", "opposite_directions"])
        
        if operation == "combined_rates":
            rate1 = random.randint(2, 6)
            rate2 = random.randint(2, 6)
            variable = "combined_rate"
            
            template = self.templates.get_template("combined_rates")
            question = template.format(rate1=rate1, rate2=rate2, variable=variable)
            
            lhs = variable
            rhs = f"{rate1} + {rate2}"
            
        elif operation == "work_together":
            time1 = random.randint(3, 8)
            time2 = random.randint(3, 8)
            variable = "time_together"
            
            template = self.templates.get_template("work_together")
            question = template.format(time1=time1, time2=time2, variable=variable)
            
            lhs = f"1 / {variable}"  # Combined rate
            rhs = f"1/{time1} + 1/{time2}"
            
        else:  # opposite_directions
            speed1 = random.randint(40, 70)
            speed2 = random.randint(40, 70)
            time = random.randint(2, 4)
            variable = "distance_apart"
            
            template = self.templates.get_template("opposite_directions")
            question = template.format(speed1=speed1, speed2=speed2, time=time, variable=variable)
            
            lhs = variable
            rhs = f"({speed1} + {speed2}) * {time}"
        
        return question, lhs, rhs, variable

    def generate_hard_rate(self):
        """Complex rate scenarios with multiple phases"""
        operation = random.choice(["sequential_work", "filling_draining", "variable_rates"])
        
        if operation == "sequential_work":
            time1 = random.randint(4, 10)
            time2 = random.randint(4, 10)
            together_time = random.randint(1, 3)
            variable = "time_remaining"
            
            template = self.templates.get_template("sequential_work")
            question = template.format(time1=time1, time2=time2, together_time=together_time, variable=variable)
            
            # Work done together + work done alone = 1 (whole job)
            lhs = f"1 - ({together_time} * (1/{time1} + 1/{time2}))"
            rhs = f"{variable} / {time2}"
            
        elif operation == "filling_draining":
            fill_time = random.randint(4, 8)
            drain_time = random.randint(6, 12)
            variable = "time_to_fill"
            
            template = self.templates.get_template("filling_draining")
            question = template.format(fill_time=fill_time, drain_time=drain_time, variable=variable)
            
            lhs = "1"  # Full tank
            rhs = f"{variable} * (1/{fill_time} - 1/{drain_time})"
            
        else:  # variable_rates
            rate1 = random.randint(3, 7)
            rate2 = random.randint(3, 7)
            time1 = random.randint(2, 5)
            total_work = random.randint(50, 100)
            variable = "total_time"
            
            template = self.templates.get_template("variable_rates")
            question = template.format(rate1=rate1, rate2=rate2, time1=time1, total_work=total_work, variable=variable)
            
            lhs = str(total_work)
            rhs = f"{rate1} * {time1} + {rate2} * ({variable} - {time1})"
        
        return question, lhs, rhs, variable

    def generate_json(self):
        base_json = super().generate_json()
        base_json.update({
            "variable": self.variable,
            "lhs": self.lhs,
            "rhs": self.rhs
        })
        return base_json


class RateWorkTemplates:
    def __init__(self):
        self.operations = {
            "find_speed": self._find_speed_templates(),
            "find_distance": self._find_distance_templates(),
            "find_time": self._find_time_templates(),
            "combined_rates": self._combined_rates_templates(),
            "work_together": self._work_together_templates(),
            "opposite_directions": self._opposite_directions_templates(),
            "sequential_work": self._sequential_work_templates(),
            "filling_draining": self._filling_draining_templates(),
            "variable_rates": self._variable_rates_templates()
        }
    
    def get_template(self, operation):
        return random.choice(self.operations[operation])

    def _find_speed_templates(self):
        return [
            "A car travels {distance} miles in {time} hours. What is its average speed? Use {variable} for the speed.",
            "If you cover {distance} km in {time} hours, what is your speed in km/h? Let {variable} be the speed.",
            "A train goes {distance} miles in {time} hours. How fast is it going? Use {variable} for the speed.",
            "What speed covers {distance} meters in {time} seconds? Let {variable} be the speed."
        ]

    def _find_distance_templates(self):
        return [
            "A car travels at {speed} mph for {time} hours. How far does it go? Use {variable} for the distance.",
            "If you drive at {speed} km/h for {time} hours, what distance do you cover? Let {variable} be the distance.",
            "Calculate the distance at speed {speed} for time {time}. Use {variable} for the distance.",
            "How far can you go at {speed} m/s for {time} seconds? Let {variable} be the distance."
        ]

    def _find_time_templates(self):
        return [
            "How long does it take to travel {distance} miles at {speed} mph? Use {variable} for the time.",
            "If you need to cover {distance} km at {speed} km/h, how long will it take? Let {variable} be the time.",
            "Calculate the time to go {distance} meters at {speed} m/s. Use {variable} for the time.",
            "A car drives {distance} miles at {speed} mph. How many hours does it take? Let {variable} be the time."
        ]

    def _combined_rates_templates(self):
        return [
            "Two machines work together. One makes {rate1} units/hour, the other {rate2} units/hour. What is their combined rate? Use {variable} for the combined rate.",
            "If pump A fills {rate1} gallons per minute and pump B fills {rate2} gallons per minute, what is their total rate? Let {variable} be the total rate.",
            "Worker A completes {rate1} tasks per hour, Worker B completes {rate2} tasks per hour. What is their combined work rate? Use {variable} for the combined rate."
        ]

    def _work_together_templates(self):
        return [
            "Person A can complete a job in {time1} hours, Person B in {time2} hours. How long working together? Use {variable} for the time together.",
            "Pipe A fills a tank in {time1} hours, Pipe B in {time2} hours. How long to fill together? Let {variable} be the time together.",
            "Worker X finishes a task in {time1} hours, Worker Y in {time2} hours. How long if they work together? Use {variable} for the time together."
        ]

    def _opposite_directions_templates(self):
        return [
            "Two cars start from the same point. One goes east at {speed1} mph, the other west at {speed2} mph. How far apart in {time} hours? Use {variable} for the distance apart.",
            "Car A travels north at {speed1} km/h, Car B south at {speed2} km/h. Starting together, how far apart after {time} hours? Let {variable} be the distance apart.",
            "Two trains leave a station. Train A goes at {speed1} mph, Train B at {speed2} mph in opposite directions. Distance after {time} hours? Use {variable} for the distance."
        ]

    def _sequential_work_templates(self):
        return [
            "Worker A can do a job in {time1} hours, Worker B in {time2} hours. They work together for {together_time} hours, then A leaves. How long for B to finish? Use {variable} for the remaining time.",
            "Two pipes fill a tank. Pipe A takes {time1} hours, Pipe B takes {time2} hours. They work together for {together_time} hours then Pipe A stops. How long for Pipe B to finish? Let {variable} be the remaining time.",
            "Person X completes work in {time1} hours, Person Y in {time2} hours. They work together for {together_time} hours then X leaves. How much longer for Y? Use {variable} for the remaining time."
        ]

    def _filling_draining_templates(self):
        return [
            "Pipe A fills a tank in {fill_time} hours. Pipe B empties it in {drain_time} hours. With both open, how long to fill? Use {variable} for the time to fill.",
            "An inlet pipe fills in {fill_time} hours, an outlet pipe drains in {drain_time} hours. How long to fill with both pipes open? Let {variable} be the time to fill.",
            "One pipe adds water taking {fill_time} hours to fill, another removes water taking {drain_time} hours to empty. Time to fill together? Use {variable} for the time."
        ]

    def _variable_rates_templates(self):
        return [
            "Machine A produces {rate1} units/hour for the first {time1} hours, then {rate2} units/hour. How long to make {total_work} units? Use {variable} for the total time.",
            "A worker starts at {rate1} tasks/hour for {time1} hours, then works at {rate2} tasks/hour. How long to complete {total_work} tasks? Let {variable} be the total time.",
            "A pump flows at {rate1} gallons/hour for {time1} hours, then at {rate2} gallons/hour. Time to fill a {total_work} gallon tank? Use {variable} for the total time."
        ]
