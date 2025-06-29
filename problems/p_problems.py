"""
P (Polynomial Time) Problems
These problems can be solved in polynomial time
"""

import random
from typing import List, Tuple
from .base import Problem, ProblemSet

class SortingProblem(Problem):
    """Is this list sorted?"""
    
    def __init__(self):
        super().__init__(
            title="Sorting Verification",
            description="Determine if a list is sorted in ascending order",
            complexity_class="P",
            difficulty=1,
            problem_type="decision"
        )
        self.numbers = []
        self.is_sorted = False
        
    def generate_instance(self):
        size = random.randint(5, 10)
        if random.choice([True, False]):
            self.numbers = sorted([random.randint(1, 100) for _ in range(size)])
            self.is_sorted = True
        else:
            self.numbers = [random.randint(1, 100) for _ in range(size)]
            self.is_sorted = self.numbers == sorted(self.numbers)
        
        self.description = f"Is this list sorted? {self.numbers}"
        self.explanation = f"This is a P problem because checking if a list is sorted takes O(n) time. The answer is {'YES' if self.is_sorted else 'NO'}."
        self.hint = "Compare each adjacent pair of numbers"
        
    def check_decision(self, answer: bool) -> bool:
        return answer == self.is_sorted

class SearchProblem(Problem):
    """Does this element exist in the list?"""
    
    def __init__(self):
        super().__init__(
            title="Element Search",
            description="Find if a target element exists in a list",
            complexity_class="P",
            difficulty=1,
            problem_type="decision"
        )
        self.numbers = []
        self.target = 0
        self.exists = False
        
    def generate_instance(self):
        self.numbers = [random.randint(1, 50) for _ in range(8)]
        if random.choice([True, False]):
            self.target = random.choice(self.numbers)
            self.exists = True
        else:
            # Generate a number that definitely doesn't exist in the list
            excluded_numbers = set(self.numbers)
            possible_targets = [i for i in range(1, 101) if i not in excluded_numbers]
            if possible_targets:
                self.target = random.choice(possible_targets)
            else:
                self.target = random.randint(101, 150)
            self.exists = False
            
        self.description = f"Does {self.target} exist in {self.numbers}?"
        self.explanation = f"This is a P problem because searching a list takes O(n) time. The answer is {'YES' if self.exists else 'NO'}."
        self.hint = "Check each element one by one"
        
    def check_decision(self, answer: bool) -> bool:
        return answer == self.exists

class PrimeProblem(Problem):
    """Is this number prime?"""
    
    def __init__(self):
        super().__init__(
            title="Primality Testing",
            description="Determine if a number is prime",
            complexity_class="P",
            difficulty=2,
            problem_type="decision"
        )
        self.number = 0
        self.is_prime = False
        
    def generate_instance(self):
        self.number = random.randint(10, 100)
        self.is_prime = self._is_prime(self.number)
        
        self.description = f"Is {self.number} a prime number?"
        self.explanation = f"This is a P problem. Modern algorithms can test primality in polynomial time. The answer is {'YES' if self.is_prime else 'NO'}."
        self.hint = "A prime number has exactly two divisors: 1 and itself"
        
    def _is_prime(self, n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
        
    def check_decision(self, answer: bool) -> bool:
        return answer == self.is_prime

class GraphConnectivityProblem(Problem):
    """Is this graph connected?"""
    
    def __init__(self):
        super().__init__(
            title="Graph Connectivity",
            description="Determine if all vertices in a graph are connected",
            complexity_class="P",
            difficulty=3,
            problem_type="decision"
        )
        self.edges = []
        self.vertices = 0
        self.is_connected = False
        
    def generate_instance(self):
        self.vertices = random.randint(4, 6)
        vertex_names = [chr(65 + i) for i in range(self.vertices)]  # A, B, C, etc.
        
        if random.choice([True, False]):
            self.edges = self._generate_connected_graph(vertex_names)
            self.is_connected = True
        else:
            self.edges = self._generate_disconnected_graph(vertex_names)
            self.is_connected = False
            
        self.description = f"Vertices: {vertex_names}\nEdges: {self.edges}\nIs this graph connected?"
        self.explanation = f"This is a P problem. Graph connectivity can be checked using DFS/BFS in O(V+E) time. The answer is {'YES' if self.is_connected else 'NO'}."
        self.hint = "A graph is connected if you can reach any vertex from any other vertex"
        
    def _generate_connected_graph(self, vertices):
        edges = []
        for i in range(len(vertices) - 1):
            edges.append((vertices[i], vertices[i + 1]))
        
        for _ in range(random.randint(0, 2)):
            v1, v2 = random.sample(vertices, 2)
            if (v1, v2) not in edges and (v2, v1) not in edges:
                edges.append((v1, v2))
        return edges
    
    def _generate_disconnected_graph(self, vertices):
        mid = max(1, len(vertices) // 2)  # Ensure at least one vertex in first group
        group1 = vertices[:mid]
        group2 = vertices[mid:]
        
        edges = []
        # Connect vertices within group1 if it has more than 1 vertex
        if len(group1) > 1:
            for i in range(len(group1) - 1):
                edges.append((group1[i], group1[i + 1]))
        # Connect vertices within group2 if it has more than 1 vertex  
        if len(group2) > 1:
            for i in range(len(group2) - 1):
                edges.append((group2[i], group2[i + 1]))
        
        # Ensure we actually have a disconnected graph by checking groups aren't empty
        # If either group is empty, create a simple disconnected graph
        if len(group1) == 0 or len(group2) == 0:
            # Create two separate components
            if len(vertices) >= 4:
                edges = [(vertices[0], vertices[1]), (vertices[2], vertices[3])]
            else:
                # Just have isolated vertices
                edges = []
                
        return edges
        
    def check_decision(self, answer: bool) -> bool:
        return answer == self.is_connected

class PProblemSet(ProblemSet):
    """Set of P complexity problems"""
    
    def __init__(self):
        super().__init__()
        self.initialize_problems()
        
    def initialize_problems(self):
        self.problems = [
            SortingProblem(),
            SearchProblem(), 
            PrimeProblem(),
            GraphConnectivityProblem()
        ]
        
        self.tutorial_problems = [
            SortingProblem(),
            SearchProblem()
        ]
        
        for problem in self.problems + self.tutorial_problems:
            problem.generate_instance()