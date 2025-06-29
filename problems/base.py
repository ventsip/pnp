"""
Base classes for complexity theory problems
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class Problem(ABC):
    """Base class for all complexity theory problems"""
    
    def __init__(self, title: str, description: str, complexity_class: str, 
                 difficulty: int = 1, problem_type: str = 'decision'):
        self.title = title
        self.description = description
        self.complexity_class = complexity_class
        self.difficulty = difficulty  # 1-5 scale
        self.problem_type = problem_type  # 'decision', 'classification', 'optimization'
        self.hint = ""
        self.explanation = ""
        
    @abstractmethod
    def generate_instance(self):
        """Generate a specific instance of this problem"""
        pass
    
    @abstractmethod
    def check_decision(self, answer: bool) -> bool:
        """Check if decision answer is correct"""
        pass
    
    def check_classification(self, answer: str) -> bool:
        """Check if complexity classification is correct"""
        return answer.upper() == self.complexity_class.upper()
    
    def check_optimization(self, answer: Any) -> bool:
        """Check if optimization answer is correct"""
        return False  # Override in subclasses
    
    def get_explanation(self) -> str:
        """Return explanation of the problem and solution"""
        return self.explanation
    
    def get_hint(self) -> str:
        """Return hint for solving the problem"""
        return self.hint

class ProblemSet(ABC):
    """Base class for problem sets"""
    
    def __init__(self):
        self.problems = []
        self.tutorial_problems = []
        
    @abstractmethod
    def initialize_problems(self):
        """Initialize the problem set"""
        pass
    
    def get_random_problem(self) -> Problem:
        """Get a random problem from the set"""
        import random
        return random.choice(self.problems)
    
    def get_tutorial_problem(self, index: int) -> Problem:
        """Get a specific tutorial problem"""
        if index < len(self.tutorial_problems):
            return self.tutorial_problems[index]
        return self.get_random_problem()