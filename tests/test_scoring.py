import pytest
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.scoring import ScoreManager


class TestScoreManager:
    def test_init(self):
        """Test ScoreManager initialization"""
        score_manager = ScoreManager()
        
        assert score_manager.total_score == 0
        assert score_manager.problems_solved == 0
        assert score_manager.problems_attempted == 0
        assert len(score_manager.score_history) == 0
        assert len(score_manager.complexity_stats) == 4
    
    def test_add_score(self):
        """Test adding score"""
        score_manager = ScoreManager()
        
        score_manager.add_score(100)
        assert score_manager.total_score == 100
        assert len(score_manager.score_history) == 1
        assert score_manager.score_history[0] == 100
        
        score_manager.add_score(50)
        assert score_manager.total_score == 150
        assert len(score_manager.score_history) == 2
    
    def test_calculate_points(self):
        """Test points calculation"""
        score_manager = ScoreManager()
        
        # Test basic points calculation
        points = score_manager.calculate_points('P', 10.0, 1)
        assert points > 0
        
        # Test that harder problems give more points
        p_points = score_manager.calculate_points('P', 10.0, 1)
        np_points = score_manager.calculate_points('NP', 10.0, 1)
        assert np_points >= p_points
    
    def test_get_total_score(self):
        """Test getting total score"""
        score_manager = ScoreManager()
        
        assert score_manager.get_total_score() == 0
        
        score_manager.add_score(100)
        assert score_manager.get_total_score() == 100
    
    def test_get_stats(self):
        """Test getting statistics"""
        score_manager = ScoreManager()
        
        stats = score_manager.get_stats()
        assert isinstance(stats, dict)
        assert 'total_score' in stats
        assert 'problems_solved' in stats
        assert 'problems_attempted' in stats
        assert 'overall_accuracy' in stats
        assert 'complexity_stats' in stats
    
    def test_record_attempt(self):
        """Test recording attempts"""
        score_manager = ScoreManager()
        
        # Test correct attempt
        score_manager.record_attempt('P', True)
        assert score_manager.problems_attempted == 1
        assert score_manager.problems_solved == 1
        assert score_manager.complexity_stats['P']['attempted'] == 1
        assert score_manager.complexity_stats['P']['solved'] == 1
        
        # Test incorrect attempt
        score_manager.record_attempt('NP', False)
        assert score_manager.problems_attempted == 2
        assert score_manager.problems_solved == 1
        assert score_manager.complexity_stats['NP']['attempted'] == 1
        assert score_manager.complexity_stats['NP']['solved'] == 0