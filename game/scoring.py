"""
Scoring system for the complexity theory game
"""

import time
from typing import Dict, List

class ScoreManager:
    """Manages scoring and statistics for the game"""
    
    def __init__(self):
        self.total_score = 0
        self.problems_solved = 0
        self.problems_attempted = 0
        self.score_history = []
        self.complexity_stats = {
            'P': {'solved': 0, 'attempted': 0},
            'NP': {'solved': 0, 'attempted': 0},
            'NP-Complete': {'solved': 0, 'attempted': 0},
            'NP-Hard': {'solved': 0, 'attempted': 0}
        }
        self.difficulty_multipliers = {1: 1.0, 2: 1.5, 3: 2.0, 4: 2.5, 5: 3.0}
        
    def calculate_points(self, complexity_class: str, solve_time: float, difficulty: int) -> int:
        """Calculate points based on complexity class, time, and difficulty"""
        base_points = {
            'P': 100,
            'NP': 200,
            'NP-Complete': 300,
            'NP-Hard': 400
        }
        
        points = base_points.get(complexity_class, 100)
        
        # Apply difficulty multiplier
        points *= self.difficulty_multipliers.get(difficulty, 1.0)
        
        # Time bonus (bonus for solving quickly)
        if solve_time < 10:
            time_bonus = 1.5
        elif solve_time < 30:
            time_bonus = 1.2
        elif solve_time < 60:
            time_bonus = 1.0
        else:
            time_bonus = 0.8
            
        points *= time_bonus
        
        return int(points)
    
    def add_score(self, points: int):
        """Add points to total score"""
        self.total_score += points
        self.score_history.append(points)
        
    def record_attempt(self, complexity_class: str, correct: bool):
        """Record an attempt for statistics"""
        self.problems_attempted += 1
        self.complexity_stats[complexity_class]['attempted'] += 1
        
        if correct:
            self.problems_solved += 1
            self.complexity_stats[complexity_class]['solved'] += 1
    
    def get_total_score(self) -> int:
        """Get total score"""
        return self.total_score
    
    def get_accuracy(self) -> float:
        """Get overall accuracy percentage"""
        if self.problems_attempted == 0:
            return 0.0
        return (self.problems_solved / self.problems_attempted) * 100
    
    def get_complexity_accuracy(self, complexity_class: str) -> float:
        """Get accuracy for specific complexity class"""
        stats = self.complexity_stats[complexity_class]
        if stats['attempted'] == 0:
            return 0.0
        return (stats['solved'] / stats['attempted']) * 100
    
    def get_stats(self) -> Dict:
        """Get comprehensive statistics"""
        return {
            'total_score': self.total_score,
            'problems_solved': self.problems_solved,
            'problems_attempted': self.problems_attempted,
            'overall_accuracy': self.get_accuracy(),
            'complexity_stats': self.complexity_stats,
            'score_history': self.score_history,
            'average_score': sum(self.score_history) / len(self.score_history) if self.score_history else 0
        }
    
    def get_rank(self) -> str:
        """Get player rank based on total score"""
        if self.total_score >= 5000:
            return "Complexity Theory Master"
        elif self.total_score >= 3000:
            return "Algorithm Expert"
        elif self.total_score >= 2000:
            return "Problem Solver"
        elif self.total_score >= 1000:
            return "Novice Theorist"
        else:
            return "Beginner"
    
    def reset_scores(self):
        """Reset all scores and statistics"""
        self.total_score = 0
        self.problems_solved = 0
        self.problems_attempted = 0
        self.score_history = []
        for complexity_class in self.complexity_stats:
            self.complexity_stats[complexity_class] = {'solved': 0, 'attempted': 0}