#!/usr/bin/env python3
"""
Complexity Theory Learning Game
A game to teach P, NP, NP-complete, and NP-hard problems
"""

import random
import time
from problems.p_problems import PProblemSet
from problems.np_problems import NPProblemSet
from problems.npc_problems import NPCompleteProblemSet
from problems.nph_problems import NPHardProblemSet
from game.scoring import ScoreManager
from game.ui import GameUI
from game.llm_questions import LLMQuestionBank, OptimizedLLMQuestionBank

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
        # Start preloading problem sets in background
        for problem_set in self.problem_sets.values():
            if hasattr(problem_set, 'start_preloading'):
                problem_set.start_preloading()
        self.complexity_classes = list(self.problem_sets.keys())
        self.ai_mode_mapping = {
            '1': 'P',
            '2': 'NP', 
            '3': 'NP-Complete',
            '4': 'NP-Hard',
            '5': 'Conceptual'
        }
        self.current_level = 1
        self.problems_solved = 0
        # Use optimized LLM question bank with compression
        self.llm_questions = OptimizedLLMQuestionBank(
            cache_file="llm_questions_cache.json.gz",
            use_compression=True
        )
        # Track performance stats
        self.questions_from_cache = 0
        self.total_questions_requested = 0
        
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
                
        # Clean shutdown of background processes
        if hasattr(self.llm_questions, 'shutdown'):
            self.llm_questions.shutdown()
        for problem_set in self.problem_sets.values():
            if hasattr(problem_set, 'shutdown'):
                problem_set.shutdown()
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
        
        for _ in range(5):
            complexity_class = random.choice(self.complexity_classes)
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
        """AI-powered question mode with performance optimizations"""
        if not self.llm_questions.is_available():
            self.ui.show_ai_unavailable()
            return
        
        # Show background generation status
        if hasattr(self.llm_questions, 'prefetch_running'):
            self.ui.show_background_generation_status(self.llm_questions.prefetch_running)
        
        while True:
            choice = self.ui.show_ai_mode_menu()
            
            if choice == '6':  # Back to main menu
                break
            
            complexity_class = self.ai_mode_mapping.get(choice)
            if not complexity_class:
                continue
            
            # Generate and ask questions
            max_questions = 3
            questions_completed = 0
            
            for i in range(max_questions):
                print(f"\n=== Question {i+1} of {max_questions} ===")
                question = self._generate_question_with_retry(complexity_class)
                if question:
                    self.solve_llm_question(question)
                    questions_completed += 1
                else:
                    print("Failed to generate question after retries. Skipping to next question.")
                    
                # Brief pause between questions
                if i < max_questions - 1:
                    time.sleep(0.5)
            
            print(f"\n🎉 Completed {questions_completed} out of {max_questions} questions!")
            
            # Show performance summary
            if self.total_questions_requested > 0:
                self.ui.show_cache_status(self.questions_from_cache, self.total_questions_requested)
                
                # Show detailed cache statistics if available
                if hasattr(self.llm_questions, 'get_cache_stats'):
                    stats = self.llm_questions.get_cache_stats()
                    print(f"\n📊 Cache Details:")
                    print(f"   Memory: {stats['memory_cache_size']}/{stats['memory_cache_limit']} questions")
                    print(f"   Disk: {stats['disk_cache_size']} questions")
                    print(f"   Compression: {'✓' if stats['compression_enabled'] else '✗'}")
    
    def _generate_question_with_retry(self, complexity_class, max_retries=2):
        """Generate a question with optimized retry logic and user feedback"""
        self.total_questions_requested += 1
        
        # Show loading indicator for better UX
        self.ui.show_generating_question(complexity_class)
        
        for attempt in range(max_retries):
            try:
                if complexity_class == 'Conceptual':
                    if self.llm_questions.generator:
                        question = self.llm_questions.generator.generate_conceptual_question("complexity theory")
                        if question:
                            self.questions_from_cache += 1
                        return question
                    else:
                        print("LLM generator not available")
                        return None
                else:
                    difficulty = random.randint(2, 4)  # Medium difficulty range
                    question = self.llm_questions.get_question_fast(complexity_class, difficulty)
                    if question:
                        self.questions_from_cache += 1
                    return question
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"Failed to generate question: {e}")
                    return None
                else:
                    print(f"Retrying question generation... ({attempt + 1}/{max_retries})")
                    time.sleep(1)  # Brief pause before retry
        return None
    
    def solve_llm_question(self, question):
        """Present an LLM question to the user with improved error handling"""
        self.ui.show_llm_question(question)
        
        user_choice = self.ui.get_llm_answer(len(question.options))
        
        # Handle quit signal
        if user_choice == -1:
            print("\n👋 Returning to main menu...")
            return
        
        user_answer = question.options[user_choice]
        
        # Check if correct_answer is the full text or just an option number
        if question.correct_answer in question.options:
            # correct_answer is the full option text
            correct = user_answer == question.correct_answer
        else:
            # correct_answer might be option number (1, 2, 3, 4) or index (0, 1, 2, 3)
            try:
                # Try parsing as 1-based option number
                correct_index = int(question.correct_answer) - 1
                if 0 <= correct_index < len(question.options):
                    correct = user_choice == correct_index
                else:
                    # Try parsing as 0-based index
                    correct_index = int(question.correct_answer)
                    correct = user_choice == correct_index
            except (ValueError, IndexError):
                # Fallback to text comparison
                correct = user_answer == question.correct_answer
        
        result_choice = self.ui.show_llm_result(correct, question, user_answer)
        
        if result_choice == 'detailed':
            self.show_detailed_explanation(question, user_answer)
        
        if correct:
            self.problems_solved += 1
    
    def show_detailed_explanation(self, question, user_answer):
        """Generate and show detailed explanation for LLM question with better UX"""
        if not self.llm_questions.generator:
            print("Detailed explanations not available (no LLM generator)")
            return
        
        # Show loading indicator
        self.ui.show_loading_spinner("Generating detailed explanation", 2.0)
        
        detailed_explanation = self.llm_questions.generator.generate_detailed_explanation(question, user_answer)
        
        if detailed_explanation:
            self.ui.show_detailed_explanation(detailed_explanation)
        else:
            print("Failed to generate detailed explanation. Please try again later.")
            input("Press Enter to continue...")
        
        # Show performance stats if in debug mode
        if self.total_questions_requested > 0:
            self.ui.show_cache_status(self.questions_from_cache, self.total_questions_requested)

if __name__ == "__main__":
    try:
        game = ComplexityGame()
        game.start_game()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n⚠️ An error occurred: {e}")
        print("Please report this issue if it persists.")
    finally:
        # Ensure proper cleanup
        if 'game' in locals():
            if hasattr(game, 'llm_questions') and hasattr(game.llm_questions, 'shutdown'):
                game.llm_questions.shutdown()
            if hasattr(game, 'problem_sets'):
                for problem_set in game.problem_sets.values():
                    if hasattr(problem_set, 'shutdown'):
                        problem_set.shutdown()