"""
NP (Nondeterministic Polynomial Time) Problems
These problems can be verified in polynomial time
"""

import random
from typing import List, Tuple, Set
from .base import Problem, ProblemSet

class SubsetSumVerificationProblem(Problem):
    """Verify if a subset sums to target"""
    
    def __init__(self):
        super().__init__(
            title="Subset Sum Verification",
            description="Verify if given subset sums to target value",
            complexity_class="NP",
            difficulty=2,
            problem_type="decision"
        )
        self.numbers = []
        self.target = 0
        self.proposed_subset = []
        self.is_valid = False
        
    def generate_instance(self):
        self.numbers = [random.randint(1, 20) for _ in range(6)]
        
        if random.choice([True, False]):
            subset_size = random.randint(2, 4)
            self.proposed_subset = random.sample(self.numbers, subset_size)
            self.target = sum(self.proposed_subset)
            self.is_valid = True
        else:
            subset_size = random.randint(2, 4)
            self.proposed_subset = random.sample(self.numbers, subset_size)
            self.target = sum(self.proposed_subset) + random.randint(1, 10)
            self.is_valid = False
            
        self.description = f"Numbers: {self.numbers}\nProposed subset: {self.proposed_subset}\nTarget sum: {self.target}\nDoes the subset sum to the target?"
        self.explanation = f"This is NP because verification is easy (O(n)) but finding a subset is hard. The answer is {'YES' if self.is_valid else 'NO'}."
        self.hint = "Add up the numbers in the proposed subset"
        
    def check_decision(self, answer: bool) -> bool:
        return answer == self.is_valid

class HamiltonianPathVerificationProblem(Problem):
    """Verify if a path visits each vertex exactly once"""
    
    def __init__(self):
        super().__init__(
            title="Hamiltonian Path Verification",
            description="Verify if given path visits each vertex exactly once",
            complexity_class="NP",
            difficulty=3,
            problem_type="decision"
        )
        self.vertices = []
        self.edges = []
        self.proposed_path = []
        self.is_valid = False
        
    def generate_instance(self):
        vertex_count = 4
        self.vertices = [chr(65 + i) for i in range(vertex_count)]  # A, B, C, D
        
        self.edges = [
            ('A', 'B'), ('B', 'C'), ('C', 'D'), ('A', 'C'), ('B', 'D')
        ]
        
        # Pre-compute valid Hamiltonian paths for this graph
        valid_paths = [
            ['A', 'C', 'B', 'D'],  # A-C-B-D (uses edges A-C, C-B, B-D)
            ['A', 'B', 'C', 'D'],  # A-B-C-D (uses edges A-B, B-C, C-D) 
            ['D', 'C', 'B', 'A'],  # D-C-B-A (reverse of A-B-C-D)
            ['D', 'B', 'C', 'A']   # D-B-C-A (uses edges D-B, B-C, C-A)
        ]
        
        if random.choice([True, False]):
            # Choose a valid path
            self.proposed_path = random.choice(valid_paths)
            self.is_valid = True
        else:
            # Generate invalid paths
            invalid_paths = [
                ['A', 'B', 'A', 'C'],     # Visits A twice
                ['A', 'D', 'B', 'C'],     # Missing edge A-D  
                ['A', 'B', 'D'],          # Doesn't visit all vertices
                ['A', 'C', 'D', 'B', 'A'] # Too many vertices
            ]
            self.proposed_path = random.choice(invalid_paths)
            self.is_valid = False
            
        self.description = f"Graph vertices: {self.vertices}\nEdges: {self.edges}\nProposed path: {' -> '.join(self.proposed_path)}\nIs this a valid Hamiltonian path?"
        self.explanation = f"This is NP because verifying a Hamiltonian path is polynomial, but finding one is exponential. The answer is {'YES' if self.is_valid else 'NO'}."
        self.hint = "Check: 1) All vertices visited exactly once, 2) All consecutive vertices connected by edges"
        
    def _is_valid_path(self, path):
        if len(set(path)) != len(self.vertices):
            return False
        for i in range(len(path) - 1):
            edge = (path[i], path[i + 1])
            if edge not in self.edges and (edge[1], edge[0]) not in self.edges:
                return False
        return True
        
    def check_decision(self, answer: bool) -> bool:
        return answer == self.is_valid

class GraphColoringVerificationProblem(Problem):
    """Verify if a graph coloring is valid"""
    
    def __init__(self):
        super().__init__(
            title="Graph Coloring Verification",
            description="Verify if vertices are colored with no adjacent vertices sharing colors",
            complexity_class="NP",
            difficulty=3,
            problem_type="decision"
        )
        self.vertices = []
        self.edges = []
        self.coloring = {}
        self.is_valid = False
        
    def generate_instance(self):
        self.vertices = ['A', 'B', 'C', 'D']
        self.edges = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('A', 'D')]
        colors = ['Red', 'Blue', 'Green']
        
        if random.choice([True, False]):
            self.coloring = {
                'A': 'Red', 'B': 'Blue', 'C': 'Red', 'D': 'Blue'
            }
            self.is_valid = True
        else:
            self.coloring = {
                'A': 'Red', 'B': 'Red', 'C': 'Blue', 'D': 'Green'
            }
            self.is_valid = False
            
        self.description = f"Graph edges: {self.edges}\nColoring: {self.coloring}\nIs this a valid 3-coloring (no adjacent vertices same color)?"
        self.explanation = f"This is NP because checking a coloring is polynomial, but finding one is exponential. The answer is {'YES' if self.is_valid else 'NO'}."
        self.hint = "Check each edge - do the connected vertices have different colors?"
        
    def check_decision(self, answer: bool) -> bool:
        valid = True
        for v1, v2 in self.edges:
            if self.coloring[v1] == self.coloring[v2]:
                valid = False
                break
        return answer == valid

class SatisfiabilityVerificationProblem(Problem):
    """Verify if a boolean assignment satisfies a formula"""
    
    def __init__(self):
        super().__init__(
            title="SAT Verification",
            description="Verify if boolean assignment satisfies logical formula",
            complexity_class="NP",
            difficulty=4,
            problem_type="decision"
        )
        self.formula = ""
        self.assignment = {}
        self.is_satisfying = False
        
    def generate_instance(self):
        variables = ['x', 'y', 'z']
        
        if random.choice([True, False]):
            self.formula = "(x OR y) AND (NOT x OR z) AND (NOT y OR NOT z)"
            self.assignment = {'x': True, 'y': False, 'z': True}
            # Verify: (T OR F) AND (F OR T) AND (T OR F) = T AND T AND T = True
            self.is_satisfying = self._evaluate_formula(self.formula, self.assignment)
        else:
            self.formula = "(x OR y) AND (NOT x OR NOT y) AND (x AND y)"
            self.assignment = {'x': True, 'y': True, 'z': False}
            # Verify: (T OR T) AND (F OR F) AND (T AND T) = T AND F AND T = False
            self.is_satisfying = self._evaluate_formula(self.formula, self.assignment)
            
        self.description = f"Formula: {self.formula}\nAssignment: {self.assignment}\nDoes this assignment satisfy the formula?"
        self.explanation = f"This is NP because checking satisfiability is polynomial, but finding a satisfying assignment is exponential. The answer is {'YES' if self.is_satisfying else 'NO'}."
        self.hint = "Substitute the values and evaluate each clause"
        
    def _evaluate_formula(self, formula, assignment):
        """Evaluate a simple boolean formula with given assignment"""
        # Simple evaluator for basic formulas - this is a simplified version
        # For the two formulas we use, we can hardcode the evaluation
        if formula == "(x OR y) AND (NOT x OR z) AND (NOT y OR NOT z)":
            x, y, z = assignment['x'], assignment['y'], assignment['z']
            clause1 = x or y
            clause2 = (not x) or z
            clause3 = (not y) or (not z)
            return clause1 and clause2 and clause3
        elif formula == "(x OR y) AND (NOT x OR NOT y) AND (x AND y)":
            x, y, z = assignment['x'], assignment['y'], assignment['z']
            clause1 = x or y
            clause2 = (not x) or (not y)
            clause3 = x and y
            return clause1 and clause2 and clause3
        else:
            return False
    
    def check_decision(self, answer: bool) -> bool:
        return answer == self.is_satisfying

class NPProblemSet(ProblemSet):
    """Set of NP complexity problems"""
    
    def __init__(self):
        super().__init__()
        self.initialize_problems()
        
    def initialize_problems(self):
        self.problems = [
            SubsetSumVerificationProblem(),
            HamiltonianPathVerificationProblem(),
            GraphColoringVerificationProblem(),
            SatisfiabilityVerificationProblem()
        ]
        
        self.tutorial_problems = [
            SubsetSumVerificationProblem(),
            GraphColoringVerificationProblem()
        ]
        
        for problem in self.problems + self.tutorial_problems:
            problem.generate_instance()