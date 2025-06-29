"""
NP-Hard Problems
These problems are at least as hard as NP-Complete problems, but may not be in NP
Often these are optimization versions of NP-Complete decision problems
"""

import random
from typing import List, Dict, Tuple, Any
from .base import Problem, ProblemSet

class TSPOptimizationProblem(Problem):
    """Traveling Salesman Problem - find shortest tour"""
    
    def __init__(self):
        super().__init__(
            title="Traveling Salesman Problem",
            description="Find the shortest tour visiting all cities",
            complexity_class="NP-Hard",
            difficulty=5,
            problem_type="optimization"
        )
        self.cities = []
        self.distances = {}
        self.optimal_cost = 0
        self.proposed_tour = []
        self.proposed_cost = 0
        
    def generate_instance(self):
        self.cities = ['A', 'B', 'C', 'D']
        
        distance_matrix = {
            ('A', 'B'): 10, ('A', 'C'): 15, ('A', 'D'): 20,
            ('B', 'C'): 35, ('B', 'D'): 25, ('C', 'D'): 30
        }
        
        self.distances = {}
        for (city1, city2), dist in distance_matrix.items():
            self.distances[(city1, city2)] = dist
            self.distances[(city2, city1)] = dist
            
        # Calculate all possible tours dynamically
        tours = []
        all_permutations = [
            ['A', 'B', 'C', 'D'],
            ['A', 'B', 'D', 'C'], 
            ['A', 'C', 'B', 'D'],
            ['A', 'C', 'D', 'B'],
            ['A', 'D', 'B', 'C'],
            ['A', 'D', 'C', 'B']
        ]
        
        for perm in all_permutations:
            tour = perm + [perm[0]]  # Return to start
            cost = self._calculate_tour_cost(tour)
            tours.append((tour, cost))
        
        self.optimal_cost = min(cost for _, cost in tours)
        
        self.proposed_tour, self.proposed_cost = random.choice(tours)
        
        distance_list = []
        for city1, city2 in distance_matrix.keys():
            distance_list.append(f"{city1}-{city2}: {distance_matrix[(city1, city2)]}")
            
        self.description = f"Cities: {self.cities}\nDistances: {', '.join(distance_list)}\nProposed tour: {' -> '.join(self.proposed_tour)}\nProposed cost: {self.proposed_cost}\nIs this optimal?"
        self.explanation = f"TSP is NP-Hard - harder than NP-Complete problems. The optimal cost is {self.optimal_cost}. Your tour costs {self.proposed_cost}."
        self.hint = "Calculate the total distance and compare to other possible tours"
        
    def check_optimization(self, answer: Any) -> bool:
        if isinstance(answer, bool):
            return answer == (self.proposed_cost == self.optimal_cost)
        elif isinstance(answer, (int, float)):
            return abs(answer - self.optimal_cost) <= 1
        return False
        
    def _calculate_tour_cost(self, tour):
        """Calculate total cost of a tour"""
        total_cost = 0
        for i in range(len(tour) - 1):
            city1, city2 = tour[i], tour[i + 1]
            total_cost += self.distances[(city1, city2)]
        return total_cost
    
    def check_decision(self, answer: bool) -> bool:
        return answer == (self.proposed_cost == self.optimal_cost)

class KnapsackOptimizationProblem(Problem):
    """0/1 Knapsack Problem - maximize value within weight constraint"""
    
    def __init__(self):
        super().__init__(
            title="0/1 Knapsack Problem",
            description="Maximize value of items within weight capacity",
            complexity_class="NP-Hard",
            difficulty=4,
            problem_type="optimization"
        )
        self.items = []
        self.capacity = 0
        self.optimal_value = 0
        self.proposed_items = []
        self.proposed_value = 0
        
    def generate_instance(self):
        self.items = [
            ("Book", 1, 4),
            ("Camera", 3, 7),
            ("Laptop", 4, 9),
            ("Phone", 2, 6)
        ]
        self.capacity = 6
        
        all_subsets = [
            ([], 0, 0),
            (["Book"], 1, 4),
            (["Camera"], 3, 7),
            (["Laptop"], 4, 9),
            (["Phone"], 2, 6),
            (["Book", "Camera"], 4, 11),
            (["Book", "Laptop"], 5, 13),
            (["Book", "Phone"], 3, 10),
            (["Camera", "Phone"], 5, 13),
            (["Book", "Camera", "Phone"], 6, 17)
        ]
        
        valid_subsets = [(items, weight, value) for items, weight, value in all_subsets if weight <= self.capacity]
        self.optimal_value = max(value for _, _, value in valid_subsets)
        
        self.proposed_items, proposed_weight, self.proposed_value = random.choice(valid_subsets)
        
        item_descriptions = []
        for name, weight, value in self.items:
            item_descriptions.append(f"{name} (w:{weight}, v:{value})")
            
        self.description = f"Items: {', '.join(item_descriptions)}\nCapacity: {self.capacity}\nSelected: {self.proposed_items}\nValue: {self.proposed_value}\nIs this optimal?"
        self.explanation = f"0/1 Knapsack is NP-Hard. The optimal value is {self.optimal_value}. Your selection has value {self.proposed_value}."
        self.hint = "Try different combinations that don't exceed the weight capacity"
        
    def check_optimization(self, answer: Any) -> bool:
        if isinstance(answer, bool):
            return answer == (self.proposed_value == self.optimal_value)
        elif isinstance(answer, (int, float)):
            return abs(answer - self.optimal_value) <= 1
        return False
        
    def check_decision(self, answer: bool) -> bool:
        return answer == (self.proposed_value == self.optimal_value)

class MaxCliqueProblem(Problem):
    """Maximum Clique - find largest complete subgraph"""
    
    def __init__(self):
        super().__init__(
            title="Maximum Clique Problem",
            description="Find the largest clique in the graph",
            complexity_class="NP-Hard",
            difficulty=4,
            problem_type="optimization"
        )
        self.vertices = []
        self.edges = []
        self.max_clique_size = 0
        self.proposed_clique = []
        
    def generate_instance(self):
        self.vertices = ['A', 'B', 'C', 'D', 'E']
        self.edges = [
            ('A', 'B'), ('A', 'C'), ('B', 'C'),  # Triangle: A-B-C
            ('D', 'E'), ('A', 'D')               # Additional edges
        ]
        
        self.max_clique_size = 3  # {A, B, C} forms the largest clique
        
        possible_cliques = [
            (['A', 'B', 'C'], True),
            (['A', 'B'], False),
            (['D', 'E'], False),
            (['A', 'D'], False),
            (['A', 'B', 'D'], False)  # Not a clique - B and D not connected
        ]
        
        self.proposed_clique, is_max = random.choice(possible_cliques)
        
        self.description = f"Graph: Vertices {self.vertices}, Edges {self.edges}\nProposed clique: {self.proposed_clique}\nSize: {len(self.proposed_clique)}\nIs this a maximum clique?"
        self.explanation = f"Maximum Clique is NP-Hard. The maximum clique size is {self.max_clique_size}. Your clique has size {len(self.proposed_clique)}."
        self.hint = "A clique means every vertex is connected to every other vertex in the group"
        
    def check_decision(self, answer: bool) -> bool:
        is_valid_clique = self._is_clique(self.proposed_clique)
        is_maximum = len(self.proposed_clique) == self.max_clique_size
        return answer == (is_valid_clique and is_maximum)
        
    def _is_clique(self, vertices):
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                edge = (vertices[i], vertices[j])
                if edge not in self.edges and (edge[1], edge[0]) not in self.edges:
                    return False
        return True

class MinVertexCoverProblem(Problem):
    """Minimum Vertex Cover - find smallest vertex cover"""
    
    def __init__(self):
        super().__init__(
            title="Minimum Vertex Cover Problem",
            description="Find the smallest vertex cover",
            complexity_class="NP-Hard", 
            difficulty=4,
            problem_type="optimization"
        )
        self.vertices = []
        self.edges = []
        self.min_cover_size = 0
        self.proposed_cover = []
        
    def generate_instance(self):
        self.vertices = ['A', 'B', 'C', 'D']
        self.edges = [('A', 'B'), ('B', 'C'), ('C', 'D')]
        
        self.min_cover_size = 2  # {B, C} covers all edges
        
        possible_covers = [
            (['A', 'B', 'C', 'D'], False),  # Size 4, not minimum
            (['B', 'C'], True),             # Size 2, minimum
            (['A', 'C', 'D'], False),       # Size 3, not minimum
            (['A', 'B'], False),            # Size 2 but doesn't cover (C,D)
        ]
        
        self.proposed_cover, is_min = random.choice(possible_covers)
        
        self.description = f"Graph: Vertices {self.vertices}, Edges {self.edges}\nProposed cover: {self.proposed_cover}\nSize: {len(self.proposed_cover)}\nIs this a minimum vertex cover?"
        self.explanation = f"Minimum Vertex Cover is NP-Hard. The minimum cover size is {self.min_cover_size}. Your cover has size {len(self.proposed_cover)}."
        self.hint = "A vertex cover must include at least one endpoint of every edge"
        
    def check_decision(self, answer: bool) -> bool:
        is_valid_cover = self._is_vertex_cover(self.proposed_cover)
        is_minimum = len(self.proposed_cover) == self.min_cover_size
        return answer == (is_valid_cover and is_minimum)
        
    def _is_vertex_cover(self, cover):
        for v1, v2 in self.edges:
            if v1 not in cover and v2 not in cover:
                return False
        return True

class NPHardProblemSet(ProblemSet):
    """Set of NP-Hard problems"""
    
    def __init__(self):
        super().__init__()
        self.initialize_problems()
        
    def initialize_problems(self):
        self.problems = [
            TSPOptimizationProblem(),
            KnapsackOptimizationProblem(),
            MaxCliqueProblem(),
            MinVertexCoverProblem()
        ]
        
        self.tutorial_problems = [
            KnapsackOptimizationProblem(),
            TSPOptimizationProblem()
        ]
        
        for problem in self.problems + self.tutorial_problems:
            problem.generate_instance()