#!/usr/bin/env python3
"""
Complexity Theory Learning Game
A game to teach P, NP, NP-complete, and NP-hard problems
"""

import random
import time
from typing import List, Dict, Any
from problems.p_problems import PProblemSet
from problems.np_problems import NPProblemSet
from problems.npc_problems import NPCompleteProblemSet
from problems.nph_problems import NPHardProblemSet
from game.scoring import ScoreManager
from game.ui import GameUI

class ComplexityGame:
    def __init__(self):
        self.score_manager = ScoreManager()
        self.ui = GameUI()
        self.problem_sets = {
            'P': PProblemSet(),
            'NP': NPProblemSet(),
            'NP-Complete': NPCompleteProblemSet(),
            'NP-Hard': NPHardProblemSet()
        }
        self.current_level = 1
        self.problems_solved = 0
        
    def start_game(self):
        """Main game loop"""
        self.ui.show_welcome()
        
        while True:
            choice = self.ui.show_main_menu()
            
            if choice == '1':
                self.play_tutorial()
            elif choice == '2':
                self.play_challenge_mode()
            elif choice == '3':
                self.show_theory()
            elif choice == '4':
                self.show_scores()
            elif choice == '5':
                break
                
        self.ui.show_goodbye()
    
    def play_tutorial(self):
        """Tutorial mode - introduces each complexity class"""
        for complexity_class in ['P', 'NP', 'NP-Complete', 'NP-Hard']:
            self.ui.show_complexity_intro(complexity_class)
            problem_set = self.problem_sets[complexity_class]
            
            for i in range(2):  # 2 problems per complexity class
                problem = problem_set.get_tutorial_problem(i)
                self.solve_problem(problem, is_tutorial=True)
    
    def play_challenge_mode(self):
        """Challenge mode - mixed problems with scoring"""
        self.ui.show_challenge_start()
        
        for round_num in range(5):
            complexity_class = random.choice(list(self.problem_sets.keys()))
            problem_set = self.problem_sets[complexity_class]
            problem = problem_set.get_random_problem()
            
            start_time = time.time()
            correct = self.solve_problem(problem, is_tutorial=False)
            solve_time = time.time() - start_time
            
            if correct:
                points = self.score_manager.calculate_points(
                    complexity_class, solve_time, problem.difficulty
                )
                self.score_manager.add_score(points)
                self.problems_solved += 1
        
        self.ui.show_final_score(self.score_manager.get_total_score())
    
    def solve_problem(self, problem, is_tutorial=False):
        """Present a problem to the user and check their solution"""
        self.ui.show_problem(problem)
        
        if problem.problem_type == 'decision':
            answer = self.ui.get_decision_answer()
            correct = problem.check_decision(answer)
        elif problem.problem_type == 'classification':
            answer = self.ui.get_classification_answer()
            correct = problem.check_classification(answer)
        elif problem.problem_type == 'optimization':
            answer = self.ui.get_optimization_answer()
            correct = problem.check_optimization(answer)
        
        self.ui.show_result(correct, problem.get_explanation())
        return correct
    
    def show_theory(self):
        """Show educational content about complexity theory"""
        self.ui.show_theory_menu()
    
    def show_scores(self):
        """Display high scores and statistics"""
        self.ui.show_scores(self.score_manager.get_stats())

if __name__ == "__main__":
    game = ComplexityGame()
    game.start_game()