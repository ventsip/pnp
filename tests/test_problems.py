import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from problems.base import Problem, ProblemSet
from problems.p_problems import PProblemSet, SortingProblem, SearchProblem
from problems.np_problems import NPProblemSet, SubsetSumVerificationProblem, HamiltonianPathVerificationProblem
from problems.npc_problems import NPCompleteProblemSet, SATDecisionProblem, HamiltonianPathDecisionProblem
from problems.nph_problems import NPHardProblemSet, TSPOptimizationProblem, MaxCliqueProblem


class MockProblem(Problem):
    """Mock problem for testing base class"""
    
    def __init__(self):
        super().__init__("Test Problem", "Test Description", "P", 1, "decision")
        self.hint = "Test hint"
        self.explanation = "Test explanation"
        self.correct_decision = True
    
    def generate_instance(self):
        return {"data": "test"}
    
    def check_decision(self, answer: bool) -> bool:
        return answer == self.correct_decision


class MockProblemSet(ProblemSet):
    """Mock problem set for testing base class"""
    
    def __init__(self):
        super().__init__()
        self.initialize_problems()
    
    def initialize_problems(self):
        self.problems = [MockProblem() for _ in range(3)]
        self.tutorial_problems = [MockProblem() for _ in range(2)]


class TestProblem:
    def test_problem_init(self):
        """Test Problem initialization"""
        problem = MockProblem()
        
        assert problem.title == "Test Problem"
        assert problem.description == "Test Description"
        assert problem.complexity_class == "P"
        assert problem.difficulty == 1
        assert problem.problem_type == "decision"
        assert problem.hint == "Test hint"
        assert problem.explanation == "Test explanation"
    
    def test_check_classification(self):
        """Test classification checking"""
        problem = MockProblem()
        
        assert problem.check_classification("P") is True
        assert problem.check_classification("p") is True
        assert problem.check_classification("NP") is False
    
    def test_check_optimization(self):
        """Test optimization checking (default implementation)"""
        problem = MockProblem()
        
        assert problem.check_optimization(100) is False
    
    def test_get_explanation(self):
        """Test getting explanation"""
        problem = MockProblem()
        
        assert problem.get_explanation() == "Test explanation"
    
    def test_get_hint(self):
        """Test getting hint"""
        problem = MockProblem()
        
        assert problem.get_hint() == "Test hint"
    
    def test_check_decision(self):
        """Test decision checking"""
        problem = MockProblem()
        
        assert problem.check_decision(True) is True
        assert problem.check_decision(False) is False


class TestProblemSet:
    def test_problem_set_init(self):
        """Test ProblemSet initialization"""
        problem_set = MockProblemSet()
        
        assert len(problem_set.problems) == 3
        assert len(problem_set.tutorial_problems) == 2
    
    def test_get_random_problem(self):
        """Test getting random problem"""
        problem_set = MockProblemSet()
        
        problem = problem_set.get_random_problem()
        assert isinstance(problem, MockProblem)
        assert problem in problem_set.problems
    
    def test_get_tutorial_problem(self):
        """Test getting tutorial problem"""
        problem_set = MockProblemSet()
        
        # Test valid index
        problem = problem_set.get_tutorial_problem(0)
        assert isinstance(problem, MockProblem)
        assert problem in problem_set.tutorial_problems
        
        # Test invalid index (should return random problem)
        problem = problem_set.get_tutorial_problem(10)
        assert isinstance(problem, MockProblem)


class TestPProblemSet:
    def test_p_problem_set_init(self):
        """Test PProblemSet initialization"""
        problem_set = PProblemSet()
        
        assert len(problem_set.problems) > 0
        assert len(problem_set.tutorial_problems) > 0
        assert all(p.complexity_class == "P" for p in problem_set.problems)
    
    def test_sorting_problem(self):
        """Test SortingProblem"""
        problem = SortingProblem()
        
        assert problem.complexity_class == "P"
        assert problem.problem_type == "decision"
        
        # Test instance generation
        problem.generate_instance()
        assert hasattr(problem, 'numbers')
        assert hasattr(problem, 'is_sorted')
        assert isinstance(problem.numbers, list)
        assert isinstance(problem.is_sorted, bool)
        
        # Test decision checking
        result = problem.check_decision(problem.is_sorted)
        assert isinstance(result, bool)
    
    def test_search_problem(self):
        """Test SearchProblem"""
        problem = SearchProblem()
        
        assert problem.complexity_class == "P"
        assert problem.problem_type == "decision"
        
        # Test instance generation
        problem.generate_instance()
        assert hasattr(problem, 'numbers')
        assert hasattr(problem, 'target')
        assert hasattr(problem, 'exists')
        assert isinstance(problem.numbers, list)
        assert isinstance(problem.target, int)
        assert isinstance(problem.exists, bool)
        
        # Test decision checking
        result = problem.check_decision(problem.exists)
        assert isinstance(result, bool)


class TestNPProblemSet:
    def test_np_problem_set_init(self):
        """Test NPProblemSet initialization"""
        problem_set = NPProblemSet()
        
        assert len(problem_set.problems) > 0
        assert len(problem_set.tutorial_problems) > 0
        assert all(p.complexity_class == "NP" for p in problem_set.problems)
    
    def test_subset_sum_verification_problem(self):
        """Test SubsetSumVerificationProblem"""
        problem = SubsetSumVerificationProblem()
        
        assert problem.complexity_class == "NP"
        assert problem.problem_type == "decision"
        
        # Test instance generation
        problem.generate_instance()
        assert hasattr(problem, 'numbers')
        assert hasattr(problem, 'target')
        assert hasattr(problem, 'proposed_subset')
        assert hasattr(problem, 'is_valid')
        assert isinstance(problem.numbers, list)
        assert isinstance(problem.target, int)
        assert isinstance(problem.proposed_subset, list)
        assert isinstance(problem.is_valid, bool)
        
        # Test decision checking
        result = problem.check_decision(problem.is_valid)
        assert isinstance(result, bool)
    
    def test_hamiltonian_path_verification_problem(self):
        """Test HamiltonianPathVerificationProblem"""
        problem = HamiltonianPathVerificationProblem()
        
        assert problem.complexity_class == "NP"
        assert problem.problem_type == "decision"
        
        # Test instance generation
        problem.generate_instance()
        assert hasattr(problem, 'vertices')
        assert hasattr(problem, 'edges')
        assert hasattr(problem, 'proposed_path')
        assert hasattr(problem, 'is_valid')
        assert isinstance(problem.vertices, list)
        assert isinstance(problem.edges, list)
        assert isinstance(problem.proposed_path, list)
        assert isinstance(problem.is_valid, bool)
        
        # Test decision checking
        result = problem.check_decision(problem.is_valid)
        assert isinstance(result, bool)


class TestNPCompleteProblemSet:
    def test_npc_problem_set_init(self):
        """Test NPCompleteProblemSet initialization"""
        problem_set = NPCompleteProblemSet()
        
        assert len(problem_set.problems) > 0
        assert len(problem_set.tutorial_problems) > 0
        assert all(p.complexity_class == "NP-Complete" for p in problem_set.problems)
    
    def test_sat_decision_problem(self):
        """Test SATDecisionProblem"""
        problem = SATDecisionProblem()
        
        assert problem.complexity_class == "NP-Complete"
        assert problem.problem_type == "decision"
        
        # Test instance generation
        problem.generate_instance()
        assert hasattr(problem, 'formula')
        assert hasattr(problem, 'variables')
        assert hasattr(problem, 'is_satisfiable')
        assert isinstance(problem.formula, str)
        assert isinstance(problem.variables, list)
        assert isinstance(problem.is_satisfiable, bool)
        
        # Test decision checking
        result = problem.check_decision(problem.is_satisfiable)
        assert isinstance(result, bool)
    
    def test_hamiltonian_path_decision_problem(self):
        """Test HamiltonianPathDecisionProblem"""
        problem = HamiltonianPathDecisionProblem()
        
        assert problem.complexity_class == "NP-Complete"
        assert problem.problem_type == "decision"
        
        # Test instance generation
        problem.generate_instance()
        assert hasattr(problem, 'vertices')
        assert hasattr(problem, 'edges')
        assert hasattr(problem, 'has_hamiltonian_path')
        assert isinstance(problem.vertices, list)
        assert isinstance(problem.edges, list)
        assert isinstance(problem.has_hamiltonian_path, bool)
        
        # Test decision checking
        result = problem.check_decision(problem.has_hamiltonian_path)
        assert isinstance(result, bool)


class TestNPHardProblemSet:
    def test_nph_problem_set_init(self):
        """Test NPHardProblemSet initialization"""
        problem_set = NPHardProblemSet()
        
        assert len(problem_set.problems) > 0
        assert len(problem_set.tutorial_problems) > 0
        assert all(p.complexity_class == "NP-Hard" for p in problem_set.problems)
    
    def test_tsp_optimization_problem(self):
        """Test TSPOptimizationProblem"""
        problem = TSPOptimizationProblem()
        
        assert problem.complexity_class == "NP-Hard"
        assert problem.problem_type == "optimization"
        
        # Test instance generation
        problem.generate_instance()
        assert hasattr(problem, 'cities')
        assert hasattr(problem, 'distances')
        assert hasattr(problem, 'optimal_cost')
        assert hasattr(problem, 'proposed_tour')
        assert hasattr(problem, 'proposed_cost')
        assert isinstance(problem.cities, list)
        assert isinstance(problem.distances, dict)
        assert isinstance(problem.optimal_cost, int)
        assert isinstance(problem.proposed_tour, list)
        assert isinstance(problem.proposed_cost, int)
    
    def test_max_clique_problem(self):
        """Test MaxCliqueProblem"""
        problem = MaxCliqueProblem()
        
        assert problem.complexity_class == "NP-Hard"
        assert problem.problem_type == "optimization"
        
        # Test instance generation
        problem.generate_instance()
        assert hasattr(problem, 'vertices')
        assert hasattr(problem, 'edges')
        assert hasattr(problem, 'max_clique_size')
        assert hasattr(problem, 'proposed_clique')
        assert isinstance(problem.vertices, list)
        assert isinstance(problem.edges, list)
        assert isinstance(problem.max_clique_size, int)
        assert isinstance(problem.proposed_clique, list)
        
        # Test decision checking
        result = problem.check_decision(len(problem.proposed_clique) == problem.max_clique_size)
        assert isinstance(result, bool)