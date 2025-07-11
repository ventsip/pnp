"""
Base classes for complexity theory problems
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import random
import threading
from concurrent.futures import ThreadPoolExecutor

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

class OptimizedProblemSet(ABC):
    """Optimized problem set with lazy loading and instance caching"""
    
    def __init__(self):
        self._problems = None
        self._tutorial_problems = None
        self._problem_cache = {}
        self._cache_lock = threading.Lock()
        self._max_cache_size = 20
        self._preload_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="preload")
        self._preload_started = False
        
    @property
    def problems(self) -> List[Problem]:
        """Lazy-loaded problems list"""
        if self._problems is None:
            self._problems = []
            self.initialize_problems()
        return self._problems
    
    @property
    def tutorial_problems(self) -> List[Problem]:
        """Lazy-loaded tutorial problems list"""
        if self._tutorial_problems is None:
            self._tutorial_problems = []
            self.initialize_tutorial_problems()
        return self._tutorial_problems
        
    @abstractmethod
    def initialize_problems(self):
        """Initialize the problem set"""
        pass
    
    def initialize_tutorial_problems(self):
        """Initialize tutorial problems - can be overridden"""
        # Default: use first few problems as tutorial
        if len(self.problems) > 0:
            self._tutorial_problems = self.problems[:2]
    
    def get_random_problem(self) -> Problem:
        """Get a random problem from the set with caching"""
        cache_key = f"random_{random.randint(0, 1000)}"
        
        with self._cache_lock:
            if cache_key in self._problem_cache:
                problem = self._problem_cache[cache_key]
                problem.generate_instance()
                return problem
        
        problem = random.choice(self.problems)
        problem.generate_instance()
        
        # Cache the problem instance
        with self._cache_lock:
            if len(self._problem_cache) < self._max_cache_size:
                self._problem_cache[cache_key] = problem
        
        return problem
    
    def get_tutorial_problem(self, index: int) -> Problem:
        """Get a specific tutorial problem with caching"""
        cache_key = f"tutorial_{index}"
        
        with self._cache_lock:
            if cache_key in self._problem_cache:
                problem = self._problem_cache[cache_key]
                problem.generate_instance()
                return problem
        
        if index < len(self.tutorial_problems):
            problem = self.tutorial_problems[index]
        else:
            problem = self.get_random_problem()
        
        problem.generate_instance()
        
        # Cache the problem instance
        with self._cache_lock:
            if len(self._problem_cache) < self._max_cache_size:
                self._problem_cache[cache_key] = problem
        
        return problem
    
    def start_preloading(self):
        """Start preloading problems in the background"""
        if not self._preload_started:
            self._preload_started = True
            self._preload_executor.submit(self._preload_problems)
    
    def _preload_problems(self):
        """Preload problems and tutorial problems"""
        try:
            # Trigger lazy loading
            _ = self.problems
            _ = self.tutorial_problems
        except Exception:
            # Silently fail if preloading fails
            pass
    
    def clear_cache(self):
        """Clear the problem cache"""
        with self._cache_lock:
            self._problem_cache.clear()
    
    def shutdown(self):
        """Clean shutdown of background processes"""
        self._preload_executor.shutdown(wait=True)

class ProblemSet(OptimizedProblemSet):
    """Legacy problem set class for backward compatibility"""
    
    def __init__(self):
        super().__init__()
        # Keep old interface for existing code
        self.problems = []
        self.tutorial_problems = []
    
    def initialize_problems(self):
        """Initialize the problem set - must be implemented by subclasses"""
        pass
    
    @property
    def problems(self) -> List[Problem]:
        """Return problems list"""
        return super().problems
    
    @problems.setter
    def problems(self, value: List[Problem]):
        """Set problems list"""
        self._problems = value
    
    @property
    def tutorial_problems(self) -> List[Problem]:
        """Return tutorial problems list"""
        return super().tutorial_problems
    
    @tutorial_problems.setter
    def tutorial_problems(self, value: List[Problem]):
        """Set tutorial problems list"""
        self._tutorial_problems = value