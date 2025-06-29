#!/usr/bin/env python3
"""
Automated game runner - simulates user playing through the game
"""

import sys
import io
from contextlib import redirect_stdout, redirect_stderr
from problems.p_problems import PProblemSet
from problems.np_problems import NPProblemSet
from problems.npc_problems import NPCompleteProblemSet
from problems.nph_problems import NPHardProblemSet
from game.scoring import ScoreManager
from game.ui import GameUI

class AutomatedGameSession:
    """Simulates an automated game session"""
    
    def __init__(self):
        self.score_manager = ScoreManager()
        self.problem_sets = {
            'P': PProblemSet(),
            'NP': NPProblemSet(),
            'NP-Complete': NPCompleteProblemSet(),
            'NP-Hard': NPHardProblemSet()
        }
        
    def run_complete_session(self):
        """Run a complete automated game session"""
        print("🎮 STARTING AUTOMATED GAME SESSION")
        print("=" * 60)
        
        # Show welcome
        print("\n🌟 WELCOME TO COMPLEXITY THEORY GAME")
        print("Learning P, NP, NP-Complete, and NP-Hard Problems")
        print("-" * 50)
        
        # Tutorial mode for each complexity class
        for complexity_class in ['P', 'NP', 'NP-Complete', 'NP-Hard']:
            self.run_tutorial_section(complexity_class)
        
        # Challenge mode
        self.run_challenge_mode()
        
        # Show final stats
        self.show_final_stats()
        
    def run_tutorial_section(self, complexity_class):
        """Run tutorial for a specific complexity class"""
        print(f"\n📚 TUTORIAL: {complexity_class} PROBLEMS")
        print("=" * 50)
        
        # Show theory
        theories = {
            'P': "Problems solvable in polynomial time O(n^k). Examples: sorting, searching.",
            'NP': "Solutions verifiable in polynomial time. May take exponential time to find.",
            'NP-Complete': "Hardest problems in NP. If any has polynomial solution, P = NP.",
            'NP-Hard': "At least as hard as NP-Complete. Often optimization problems."
        }
        print(f"THEORY: {theories[complexity_class]}")
        print()
        
        # Solve 2 problems from this class
        problem_set = self.problem_sets[complexity_class]
        for i in range(2):
            if i < len(problem_set.problems):
                problem = problem_set.problems[i]
                problem.generate_instance()
                self.solve_problem_automatically(problem, i + 1)
    
    def solve_problem_automatically(self, problem, problem_num):
        """Automatically solve a problem and show the process"""
        print(f"--- Problem {problem_num}: {problem.title} ---")
        print(f"Complexity: {problem.complexity_class} | Difficulty: {'★' * problem.difficulty}")
        print(f"Description: {problem.description}")
        
        # Simulate thinking...
        print("\n🤔 Analyzing problem...")
        
        # For demo purposes, we'll get the correct answer
        if problem.problem_type == 'decision':
            # For demonstration, we'll simulate some correct and some incorrect answers
            import random
            if random.random() > 0.3:  # 70% correct rate
                if hasattr(problem, 'is_sorted'):
                    correct_answer = problem.is_sorted
                elif hasattr(problem, 'exists'):
                    correct_answer = problem.exists
                elif hasattr(problem, 'is_prime'):
                    correct_answer = problem.is_prime
                elif hasattr(problem, 'is_connected'):
                    correct_answer = problem.is_connected
                elif hasattr(problem, 'is_valid'):
                    correct_answer = problem.is_valid
                elif hasattr(problem, 'is_satisfying'):
                    correct_answer = problem.is_satisfying
                elif hasattr(problem, 'is_satisfiable'):
                    correct_answer = problem.is_satisfiable
                elif hasattr(problem, 'has_hamiltonian_path'):
                    correct_answer = problem.has_hamiltonian_path
                elif hasattr(problem, 'has_vertex_cover'):
                    correct_answer = problem.has_vertex_cover
                elif hasattr(problem, 'has_clique'):
                    correct_answer = problem.has_clique
                else:
                    correct_answer = True
                
                user_answer = correct_answer
                is_correct = True
            else:
                # Wrong answer for demonstration
                user_answer = random.choice([True, False])
                is_correct = problem.check_decision(user_answer)
        else:
            user_answer = True
            is_correct = True
        
        print(f"💭 My answer: {'YES' if user_answer else 'NO'}")
        
        # Check answer
        if is_correct:
            print("✅ CORRECT!")
            points = self.score_manager.calculate_points(problem.complexity_class, 20, problem.difficulty)
            self.score_manager.add_score(points)
            print(f"📈 +{points} points!")
        else:
            print("❌ INCORRECT")
            points = 0
            
        self.score_manager.record_attempt(problem.complexity_class, is_correct)
        
        print(f"📖 Explanation: {problem.explanation}")
        print()
    
    def run_challenge_mode(self):
        """Run challenge mode with mixed problems"""
        print("\n🏆 CHALLENGE MODE")
        print("=" * 40)
        print("Facing mixed problems from all complexity classes!")
        print()
        
        import random
        
        # Select 5 random problems
        all_problems = []
        for problem_set in self.problem_sets.values():
            all_problems.extend(problem_set.problems)
        
        selected_problems = random.sample(all_problems, min(5, len(all_problems)))
        
        for i, problem in enumerate(selected_problems, 1):
            problem.generate_instance()
            print(f"🎯 Challenge {i}/5")
            self.solve_problem_automatically(problem, i)
        
        print("🏁 CHALLENGE COMPLETE!")
    
    def show_final_stats(self):
        """Show final game statistics"""
        print("\n📊 FINAL STATISTICS")
        print("=" * 40)
        
        stats = self.score_manager.get_stats()
        
        print(f"🏆 Total Score: {stats['total_score']}")
        print(f"✅ Problems Solved: {stats['problems_solved']}/{stats['problems_attempted']}")
        print(f"🎯 Overall Accuracy: {stats['overall_accuracy']:.1f}%")
        print(f"📈 Average Score: {stats['average_score']:.0f} points per problem")
        
        print(f"\n🎖️  Rank: {self.score_manager.get_rank()}")
        
        print(f"\n📋 Performance by Complexity Class:")
        for complexity_class, class_stats in stats['complexity_stats'].items():
            attempted = class_stats['attempted']
            solved = class_stats['solved']
            if attempted > 0:
                accuracy = (solved / attempted) * 100
                print(f"   {complexity_class}: {solved}/{attempted} ({accuracy:.0f}%)")
        
        print(f"\n🎓 LEARNING COMPLETE!")
        print("You've experienced problems from all complexity classes!")
        print("\nKey takeaways:")
        print("• P problems can be solved quickly")
        print("• NP problems can be verified quickly") 
        print("• NP-Complete problems are the hardest in NP")
        print("• NP-Hard problems are at least as hard as NP-Complete")
        print("• P vs NP remains unsolved - worth $1,000,000!")

def main():
    """Run the automated game session"""
    try:
        session = AutomatedGameSession()
        session.run_complete_session()
        
        print(f"\n" + "=" * 60)
        print("🎮 GAME SESSION COMPLETED SUCCESSFULLY!")
        print("To play interactively: python3 main.py")
        print("To see more examples: python3 demo.py")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error running game: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()