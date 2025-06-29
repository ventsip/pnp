"""
NP-Complete Problems
These are the hardest problems in NP - if any NP-Complete problem has a polynomial solution, then P = NP
"""

import random
from typing import List, Dict, Tuple
from .base import Problem, ProblemSet

class SATDecisionProblem(Problem):
    """Boolean Satisfiability - the first proven NP-Complete problem"""
    
    def __init__(self):
        super().__init__(
            title="SAT Decision Problem",
            description="Determine if a boolean formula can be satisfied",
            complexity_class="NP-Complete",
            difficulty=4,
            problem_type="decision"
        )
        self.formula = ""
        self.variables = []
        self.is_satisfiable = False
        
    def generate_instance(self):
        self.variables = ['a', 'b', 'c']
        
        formulas = [
            ("(a OR b) AND (NOT a OR c) AND (NOT b OR NOT c)", True),
            ("(a OR b) AND (NOT a) AND (NOT b)", False),
            ("(a AND b) OR (NOT a AND NOT b)", True),
            ("a AND (NOT a)", False)
        ]
        
        self.formula, self.is_satisfiable = random.choice(formulas)
        
        self.description = f"Formula: {self.formula}\nVariables: {self.variables}\nIs this formula satisfiable?"
        self.explanation = f"SAT is NP-Complete - it's in NP and every NP problem reduces to it. The answer is {'YES' if self.is_satisfiable else 'NO'}."
        self.hint = "Try different true/false assignments to see if any makes the formula true"
        
    def check_decision(self, answer: bool) -> bool:
        return answer == self.is_satisfiable

class ThreeSATDecisionProblem(Problem):
    """3-SAT - SAT with exactly 3 literals per clause"""
    
    def __init__(self):
        super().__init__(
            title="3-SAT Decision Problem", 
            description="Determine if a 3-SAT formula is satisfiable",
            complexity_class="NP-Complete",
            difficulty=4,
            problem_type="decision"
        )
        self.clauses = []
        self.variables = ['x', 'y', 'z']
        self.is_satisfiable = False
        
    def generate_instance(self):
        satisfiable_formulas = [
            (["x", "y", "z"], ["NOT x", "y", "NOT z"], ["x", "NOT y", "z"]),
            (["x", "NOT y", "z"], ["NOT x", "y", "NOT z"], ["x", "y", "NOT z"])
        ]
        
        unsatisfiable_formulas = [
            (["x", "y", "z"], ["NOT x", "NOT y", "NOT z"])  # No assignment can satisfy both clauses
        ]
        
        if random.choice([True, False]):
            self.clauses = list(random.choice(satisfiable_formulas))
            self.is_satisfiable = True
        else:
            self.clauses = list(random.choice(unsatisfiable_formulas))
            self.is_satisfiable = False
            
        clause_strings = []
        for clause in self.clauses:
            clause_strings.append(f"({' OR '.join(clause)})")
            
        self.description = f"3-SAT Formula: {' AND '.join(clause_strings)}\nIs this satisfiable?"
        self.explanation = f"3-SAT is NP-Complete. Every clause must be true. The answer is {'YES' if self.is_satisfiable else 'NO'}."
        self.hint = "Each clause needs at least one true literal"
        
    def check_decision(self, answer: bool) -> bool:
        return answer == self.is_satisfiable

class HamiltonianPathDecisionProblem(Problem):
    """Hamiltonian Path - visit each vertex exactly once"""
    
    def __init__(self):
        super().__init__(
            title="Hamiltonian Path Decision",
            description="Determine if graph has a Hamiltonian path",
            complexity_class="NP-Complete", 
            difficulty=4,
            problem_type="decision"
        )
        self.vertices = []
        self.edges = []
        self.has_hamiltonian_path = False
        
    def generate_instance(self):
        self.vertices = ['A', 'B', 'C', 'D']
        
        graphs_with_path = [
            [('A', 'B'), ('B', 'C'), ('C', 'D'), ('A', 'D')],
            [('A', 'B'), ('B', 'C'), ('C', 'D'), ('B', 'D'), ('A', 'C')]
        ]
        
        graphs_without_path = [
            [('A', 'B'), ('C', 'D')],  # Two disconnected components
            [('A', 'B')]               # Missing vertices C and D completely
        ]
        
        if random.choice([True, False]):
            self.edges = random.choice(graphs_with_path)
            self.has_hamiltonian_path = True
        else:
            self.edges = random.choice(graphs_without_path)
            self.has_hamiltonian_path = False
            
        self.description = f"Graph: Vertices {self.vertices}, Edges {self.edges}\nDoes this graph have a Hamiltonian path?"
        self.explanation = f"Hamiltonian path is NP-Complete. Must visit each vertex exactly once. The answer is {'YES' if self.has_hamiltonian_path else 'NO'}."
        self.hint = "Try to trace a path that visits A, B, C, D each exactly once"
        
    def check_decision(self, answer: bool) -> bool:
        return answer == self.has_hamiltonian_path

class VertexCoverDecisionProblem(Problem):
    """Vertex Cover - select vertices to cover all edges"""
    
    def __init__(self):
        super().__init__(
            title="Vertex Cover Decision",
            description="Determine if graph has vertex cover of given size",
            complexity_class="NP-Complete",
            difficulty=3,
            problem_type="decision"
        )
        self.vertices = []
        self.edges = []
        self.k = 0
        self.has_vertex_cover = False
        
    def generate_instance(self):
        self.vertices = ['A', 'B', 'C', 'D']
        self.edges = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('A', 'D')]
        
        if random.choice([True, False]):
            self.k = 2
            self.has_vertex_cover = True  # {A, C} or {B, D} covers all edges
        else:
            self.k = 1  
            self.has_vertex_cover = False  # No single vertex covers all edges
            
        self.description = f"Graph: Vertices {self.vertices}, Edges {self.edges}\nIs there a vertex cover of size ≤ {self.k}?"
        self.explanation = f"Vertex Cover is NP-Complete. A vertex cover includes at least one endpoint of every edge. The answer is {'YES' if self.has_vertex_cover else 'NO'}."
        self.hint = "A vertex cover must include at least one vertex from each edge"
        
    def check_decision(self, answer: bool) -> bool:
        return answer == self.has_vertex_cover

class CliqueProblem(Problem):
    """Clique - find complete subgraph"""
    
    def __init__(self):
        super().__init__(
            title="Clique Decision Problem",
            description="Determine if graph has clique of given size",
            complexity_class="NP-Complete",
            difficulty=4,
            problem_type="decision"
        )
        self.vertices = []
        self.edges = []
        self.k = 0
        self.has_clique = False
        
    def generate_instance(self):
        self.vertices = ['A', 'B', 'C', 'D']
        
        if random.choice([True, False]):
            self.edges = [('A', 'B'), ('B', 'C'), ('A', 'C'), ('C', 'D')]
            self.k = 3
            self.has_clique = True  # {A, B, C} forms a 3-clique
        else:
            self.edges = [('A', 'B'), ('B', 'C'), ('C', 'D')]
            self.k = 3
            self.has_clique = False  # No 3-clique exists
            
        self.description = f"Graph: Vertices {self.vertices}, Edges {self.edges}\nIs there a clique of size ≥ {self.k}?"
        self.explanation = f"Clique is NP-Complete. A k-clique has all possible edges between k vertices. The answer is {'YES' if self.has_clique else 'NO'}."
        self.hint = "A clique means every vertex is connected to every other vertex in the group"
        
    def check_decision(self, answer: bool) -> bool:
        return answer == self.has_clique

class NPCompleteProblemSet(ProblemSet):
    """Set of NP-Complete problems"""
    
    def __init__(self):
        super().__init__()
        self.initialize_problems()
        
    def initialize_problems(self):
        self.problems = [
            SATDecisionProblem(),
            ThreeSATDecisionProblem(),
            HamiltonianPathDecisionProblem(),
            VertexCoverDecisionProblem(),
            CliqueProblem()
        ]
        
        self.tutorial_problems = [
            SATDecisionProblem(),
            VertexCoverDecisionProblem()
        ]
        
        for problem in self.problems + self.tutorial_problems:
            problem.generate_instance()