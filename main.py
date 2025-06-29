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
from game.llm_questions import LLMQuestionBank

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
        self.llm_questions = LLMQuestionBank()
        
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
                self.play_ai_mode()
            elif choice == '4':
                self.show_theory()
            elif choice == '5':
                self.show_scores()
            elif choice == '6':
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
        
        correct = False  # Default value in case no branch is taken
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
    
    def play_ai_mode(self):
        """AI-powered question mode"""
        if not self.llm_questions.is_available():
            self.ui.show_ai_unavailable()
            return
        
        while True:
            choice = self.ui.show_ai_mode_menu()
            
            if choice == '6':  # Back to main menu
                break
            
            # Map choice to complexity class
            complexity_classes = {
                '1': 'P',
                '2': 'NP', 
                '3': 'NP-Complete',
                '4': 'NP-Hard',
                '5': 'Conceptual'
            }
            
            complexity_class = complexity_classes.get(choice)
            if not complexity_class:
                continue
            
            # Generate and ask questions
            questions_asked = 0
            max_questions = 3
            max_retries = 2
            
            while questions_asked < max_questions:
                retries = 0
                question = None
                
                while retries < max_retries and not question:
                    try:
                        if complexity_class == 'Conceptual':
                            if self.llm_questions.generator:
                                question = self.llm_questions.generator.generate_conceptual_question("complexity theory")
                            else:
                                print("LLM generator not available")
                                break
                        else:
                            difficulty = random.randint(2, 4)  # Medium difficulty range
                            question = self.llm_questions.get_question(complexity_class, difficulty)
                    except Exception as e:
                        print(f"Error generating question: {e}")
                    
                    if not question:
                        retries += 1
                        if retries < max_retries:
                            print(f"Retrying question generation... ({retries}/{max_retries})")
                
                if question:
                    self.solve_llm_question(question)
                    questions_asked += 1
                else:
                    print("Failed to generate question after retries. Skipping to next question.")
                    questions_asked += 1  # Still increment to avoid infinite loop
    
    def solve_llm_question(self, question):
        """Present an LLM question to the user"""
        self.ui.show_llm_question(question)
        
        user_choice = self.ui.get_llm_answer(len(question.options))
        user_answer = question.options[user_choice]
        correct = user_answer == question.correct_answer
        
        result_choice = self.ui.show_llm_result(correct, question, user_answer)
        
        if result_choice == 'detailed':
            self.show_detailed_explanation(question, user_answer)
        
        if correct:
            self.problems_solved += 1
    
    def show_detailed_explanation(self, question, user_answer):
        """Generate and show detailed explanation for LLM question"""
        if not self.llm_questions.generator:
            print("Detailed explanations not available (no LLM generator)")
            return
        
        print("Generating detailed explanation...")
        detailed_explanation = self.llm_questions.generator.generate_detailed_explanation(question, user_answer)
        
        if detailed_explanation:
            self.ui.show_detailed_explanation(detailed_explanation)
        else:
            print("Failed to generate detailed explanation. Please try again later.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    game = ComplexityGame()
    game.start_game()