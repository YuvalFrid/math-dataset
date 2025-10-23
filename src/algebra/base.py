class AlgebraProblem:
    """Base class for all algebra problem generators."""
    
    def __init__(self, domain="algebra", problem_type=None):
        self.domain = domain
        self.type = problem_type
        self.question = None
        self.json = None
        self.level = "easy"
    
    def generate_json(self):
        """Generate JSON representation of the problem."""
        return {
            "domain": self.domain,
            "type": self.type,
            "level": self.level,
            "question": self.question
        }
