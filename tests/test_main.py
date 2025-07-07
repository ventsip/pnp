import pytest
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import ComplexityGame
from game.scoring import ScoreManager
from game.ui import GameUI


class TestComplexityGame:
    def test_init(self):
        """Test ComplexityGame initialization"""
        game = ComplexityGame()
        
        assert isinstance(game.score_manager, ScoreManager)
        assert isinstance(game.ui, GameUI)
        assert len(game.problem_sets) == 4
        assert 'P' in game.problem_sets
        assert 'NP' in game.problem_sets
        assert 'NP-Complete' in game.problem_sets
        assert 'NP-Hard' in game.problem_sets
        assert game.complexity_classes == list(game.problem_sets.keys())
        assert len(game.ai_mode_mapping) == 5
        assert game.current_level == 1
        assert game.problems_solved == 0
    
    def test_ai_mode_mapping(self):
        """Test AI mode mapping is correct"""
        game = ComplexityGame()
        
        expected_mapping = {
            '1': 'P',
            '2': 'NP', 
            '3': 'NP-Complete',
            '4': 'NP-Hard',
            '5': 'Conceptual'
        }
        assert game.ai_mode_mapping == expected_mapping
    
    def test_complexity_classes_cached(self):
        """Test complexity classes are cached correctly"""
        game = ComplexityGame()
        
        # Should be the same as problem_sets keys
        assert set(game.complexity_classes) == set(game.problem_sets.keys())
        assert isinstance(game.complexity_classes, list)
    
    def test_generate_question_with_retry_conceptual(self):
        """Test question generation with retry for conceptual questions"""
        game = ComplexityGame()
        
        # Test with no generator (should return None)
        result = game._generate_question_with_retry('Conceptual')
        assert result is None
    
    def test_generate_question_with_retry_regular(self):
        """Test question generation with retry for regular complexity classes"""
        game = ComplexityGame()
        
        # Test with valid complexity class
        result = game._generate_question_with_retry('P')
        # Should either return a question or None (depends on LLM availability)
        assert result is None or hasattr(result, 'question')