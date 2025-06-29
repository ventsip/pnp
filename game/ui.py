"""
User Interface for the complexity theory game
"""

import os
from typing import Dict, Any
from problems.base import Problem

class GameUI:
    """Handles all user interface interactions"""
    
    def __init__(self):
        self.complexity_descriptions = {
            'P': """
P (Polynomial Time) Problems:
- Can be solved in polynomial time O(n^k)
- Examples: Sorting, searching, shortest path
- These are considered 'easy' problems
- Every computer can solve them efficiently
            """,
            'NP': """
NP (Nondeterministic Polynomial) Problems:
- Solutions can be VERIFIED in polynomial time
- May take exponential time to FIND solutions
- Examples: Checking if a subset sums to target
- P ⊆ NP (all P problems are also NP)
            """,
            'NP-Complete': """
NP-Complete Problems:
- Hardest problems in NP
- Every NP problem reduces to them
- If any NP-Complete problem has polynomial solution, then P = NP
- Examples: SAT, Hamiltonian Path, Vertex Cover
            """,
            'NP-Hard': """
NP-Hard Problems:
- At least as hard as NP-Complete problems
- May not be in NP themselves
- Often optimization versions of NP-Complete problems
- Examples: TSP optimization, Maximum Clique
            """
        }
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_welcome(self):
        """Display welcome message"""
        self.clear_screen()
        print("=" * 60)
        print("    COMPLEXITY THEORY LEARNING GAME")
        print("    Learn P, NP, NP-Complete, and NP-Hard Problems")
        print("=" * 60)
        print()
        print("Welcome! This game will teach you about computational complexity.")
        print("You'll solve problems from different complexity classes and")
        print("learn what makes some problems harder than others.")
        print()
        input("Press Enter to continue...")
    
    def show_main_menu(self) -> str:
        """Display main menu and get user choice"""
        self.clear_screen()
        print("MAIN MENU")
        print("-" * 20)
        print("1. Tutorial Mode (Learn each complexity class)")
        print("2. Challenge Mode (Mixed problems with scoring)")
        print("3. Theory Reference (Educational content)")
        print("4. View Scores & Statistics")
        print("5. Quit")
        print()
        
        while True:
            choice = input("Enter your choice (1-5): ").strip()
            if choice in ['1', '2', '3', '4', '5']:
                return choice
            print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")
    
    def show_complexity_intro(self, complexity_class: str):
        """Show introduction to a complexity class"""
        self.clear_screen()
        print(f"LEARNING: {complexity_class}")
        print("=" * 40)
        print(self.complexity_descriptions[complexity_class])
        print()
        input("Press Enter to start solving problems...")
    
    def show_problem(self, problem: Problem):
        """Display a problem to the user"""
        self.clear_screen()
        print(f"PROBLEM: {problem.title}")
        print(f"Complexity Class: {problem.complexity_class}")
        print(f"Difficulty: {'★' * problem.difficulty}")
        print("-" * 50)
        print(problem.description)
        print()
        
        if problem.hint:
            show_hint = input("Would you like a hint? (y/n): ").lower().strip()
            if show_hint == 'y':
                print(f"HINT: {problem.hint}")
                print()
    
    def get_decision_answer(self) -> bool:
        """Get yes/no answer from user"""
        while True:
            answer = input("Your answer (yes/no or y/n): ").lower().strip()
            if answer in ['yes', 'y', 'true', '1']:
                return True
            elif answer in ['no', 'n', 'false', '0']:
                return False
            else:
                print("Please answer yes/no (or y/n)")
    
    def get_classification_answer(self) -> str:
        """Get complexity class classification from user"""
        print("Which complexity class does this problem belong to?")
        print("1. P")
        print("2. NP") 
        print("3. NP-Complete")
        print("4. NP-Hard")
        
        while True:
            choice = input("Enter choice (1-4): ").strip()
            if choice == '1':
                return 'P'
            elif choice == '2':
                return 'NP'
            elif choice == '3':
                return 'NP-Complete'
            elif choice == '4':
                return 'NP-Hard'
            else:
                print("Please enter 1, 2, 3, or 4")
    
    def get_optimization_answer(self) -> Any:
        """Get optimization answer from user"""
        print("For optimization problems:")
        print("1. Enter 'yes' if the proposed solution is optimal")
        print("2. Enter 'no' if it's not optimal")
        print("3. Or enter the optimal value if you know it")
        
        answer = input("Your answer: ").strip()
        
        # Try to parse as number first
        try:
            return float(answer)
        except ValueError:
            # Parse as yes/no
            if answer.lower() in ['yes', 'y', 'true', '1']:
                return True
            elif answer.lower() in ['no', 'n', 'false', '0']:
                return False
            else:
                return answer
    
    def show_result(self, correct: bool, explanation: str):
        """Show whether answer was correct and explanation"""
        print()
        print("=" * 50)
        if correct:
            print("✓ CORRECT!")
        else:
            print("✗ INCORRECT")
        
        print()
        print("EXPLANATION:")
        print(explanation)
        print()
        input("Press Enter to continue...")
    
    def show_challenge_start(self):
        """Show challenge mode start message"""
        self.clear_screen()
        print("CHALLENGE MODE")
        print("=" * 30)
        print("You will face 5 random problems from all complexity classes.")
        print("Points are awarded based on:")
        print("- Complexity class (P=100, NP=200, NP-C=300, NP-H=400)")
        print("- Problem difficulty (1-5 stars)")
        print("- Speed of solving (time bonus)")
        print()
        input("Press Enter to begin the challenge...")
    
    def show_final_score(self, total_score: int):
        """Show final score after challenge"""
        self.clear_screen()
        print("CHALLENGE COMPLETE!")
        print("=" * 30)
        print(f"Final Score: {total_score} points")
        print()
        
        if total_score >= 2000:
            print("🏆 EXCELLENT! You're a complexity theory expert!")
        elif total_score >= 1500:
            print("🥈 GREAT JOB! You have a solid understanding!")
        elif total_score >= 1000:
            print("🥉 GOOD WORK! Keep practicing!")
        else:
            print("📚 Keep studying! Practice makes perfect!")
        
        print()
        input("Press Enter to return to main menu...")
    
    def show_theory_menu(self):
        """Show theory reference menu"""
        while True:
            self.clear_screen()
            print("THEORY REFERENCE")
            print("=" * 30)
            print("1. P Problems")
            print("2. NP Problems")
            print("3. NP-Complete Problems")
            print("4. NP-Hard Problems")
            print("5. P vs NP Question")
            print("6. Back to Main Menu")
            print()
            
            choice = input("Enter choice (1-6): ").strip()
            
            if choice in ['1', '2', '3', '4']:
                complexity_classes = ['P', 'NP', 'NP-Complete', 'NP-Hard']
                selected_class = complexity_classes[int(choice) - 1]
                
                self.clear_screen()
                print(f"{selected_class} PROBLEMS")
                print("=" * 40)
                print(self.complexity_descriptions[selected_class])
                print()
                input("Press Enter to continue...")
                
            elif choice == '5':
                self.show_p_vs_np_explanation()
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please enter 1-6.")
    
    def show_p_vs_np_explanation(self):
        """Show P vs NP explanation"""
        self.clear_screen()
        print("THE P vs NP QUESTION")
        print("=" * 40)
        print("""
The P vs NP question is one of the most important unsolved problems in 
computer science and mathematics.

P: Problems solvable in polynomial time
NP: Problems verifiable in polynomial time

The question: Does P = NP?

If P = NP:
- Every problem whose solution can be quickly verified can also be quickly solved
- This would revolutionize cryptography, optimization, and many other fields

If P ≠ NP:
- Some problems are fundamentally harder to solve than to verify
- This is what most computer scientists believe

Current status: UNSOLVED
Prize: $1,000,000 (Clay Millennium Prize)

This game helps you understand the difference between these complexity classes!
        """)
        print()
        input("Press Enter to continue...")
    
    def show_scores(self, stats: Dict):
        """Display scores and statistics"""
        self.clear_screen()
        print("SCORES & STATISTICS")
        print("=" * 40)
        print(f"Total Score: {stats['total_score']}")
        print(f"Problems Solved: {stats['problems_solved']}/{stats['problems_attempted']}")
        print(f"Overall Accuracy: {stats['overall_accuracy']:.1f}%")
        print()
        
        print("Performance by Complexity Class:")
        print("-" * 30)
        for complexity_class, class_stats in stats['complexity_stats'].items():
            attempted = class_stats['attempted']
            solved = class_stats['solved']
            accuracy = (solved / attempted * 100) if attempted > 0 else 0
            print(f"{complexity_class}: {solved}/{attempted} ({accuracy:.1f}%)")
        
        print()
        if stats['score_history']:
            print(f"Average Score per Problem: {stats['average_score']:.0f}")
        
        print()
        input("Press Enter to continue...")
    
    def show_goodbye(self):
        """Display goodbye message"""
        self.clear_screen()
        print("Thanks for playing!")
        print("Keep exploring the fascinating world of computational complexity!")
        print()
        print("Remember: P vs NP is still unsolved... maybe you'll solve it someday! 🤔")
        print()