"""
User Interface for the complexity theory game
"""

import os
import sys
import time
import threading
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
        print("3. AI Question Mode (LLM-generated questions)")
        print("4. Theory Reference (Educational content)")
        print("5. View Scores & Statistics")
        print("6. Quit")
        print()
        
        while True:
            choice = input("Enter your choice (1-6): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6']:
                return choice
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, or 6.")
    
    def show_complexity_intro(self, complexity_class: str):
        """Show introduction to a complexity class"""
        self.clear_screen()
        print(f"LEARNING: {complexity_class}")
        print("=" * 40)
        print(self.complexity_descriptions[complexity_class])
        print()
        self.show_complexity_relationships()
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
        
        self.current_problem_hint = problem.hint if problem.hint else None
    
    def get_decision_answer(self) -> bool:
        """Get yes/no answer from user"""
        while True:
            hint_text = "/h for hint" if hasattr(self, 'current_problem_hint') and self.current_problem_hint else ""
            prompt = f"Your answer (yes/no or y/n{'/h' if hint_text else ''}): "
            answer = input(prompt).lower().strip()
            
            if answer in ['yes', 'y', 'true', '1']:
                return True
            elif answer in ['no', 'n', 'false', '0']:
                return False
            elif answer == 'h' and hasattr(self, 'current_problem_hint') and self.current_problem_hint:
                print(f"HINT: {self.current_problem_hint}")
                print()
            else:
                help_text = "Please answer yes/no (or y/n" + ("/h for hint" if hint_text else "") + ")"
                print(help_text)
    
    def get_classification_answer(self) -> str:
        """Get complexity class classification from user"""
        print("Which complexity class does this problem belong to?")
        print("1. P")
        print("2. NP") 
        print("3. NP-Complete")
        print("4. NP-Hard")
        
        while True:
            hint_text = "/h for hint" if hasattr(self, 'current_problem_hint') and self.current_problem_hint else ""
            prompt = f"Enter choice (1-4{'/h' if hint_text else ''}): "
            choice = input(prompt).strip()
            
            if choice == '1':
                return 'P'
            elif choice == '2':
                return 'NP'
            elif choice == '3':
                return 'NP-Complete'
            elif choice == '4':
                return 'NP-Hard'
            elif choice == 'h' and hasattr(self, 'current_problem_hint') and self.current_problem_hint:
                print(f"HINT: {self.current_problem_hint}")
                print()
            else:
                help_text = "Please enter 1, 2, 3, or 4" + (" or h for hint" if hint_text else "")
                print(help_text)
    
    def get_optimization_answer(self) -> Any:
        """Get optimization answer from user"""
        print("For optimization problems:")
        print("1. Enter 'yes' if the proposed solution is optimal")
        print("2. Enter 'no' if it's not optimal")
        print("3. Or enter the optimal value if you know it")
        
        while True:
            hint_text = " or h for hint" if hasattr(self, 'current_problem_hint') and self.current_problem_hint else ""
            answer = input(f"Your answer{hint_text}: ").strip()
            
            if answer.lower() == 'h' and hasattr(self, 'current_problem_hint') and self.current_problem_hint:
                print(f"HINT: {self.current_problem_hint}")
                print()
                continue
            
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
        if 'complexity_stats' in stats:
            for complexity_class, class_stats in stats['complexity_stats'].items():
                attempted = class_stats['attempted']
                solved = class_stats['solved']
                accuracy = (solved / attempted * 100) if attempted > 0 else 0
                print(f"{complexity_class}: {solved}/{attempted} ({accuracy:.1f}%)")
        else:
            print("No complexity class statistics available")
        
        print()
        if 'score_history' in stats and stats['score_history']:
            print(f"Average Score per Problem: {stats['average_score']:.0f}")
        
        print()
        input("Press Enter to continue...")
    
    def show_complexity_relationships(self):
        """Show ASCII visualization of complexity class relationships"""
        print("COMPLEXITY CLASS RELATIONSHIPS:")
        print("=" * 50)
        print("""
┌─────────────────────────────────────────────────────────┐
│                       NP-HARD                           │
│  ┌─────────────────────────────────────────────────┐    │
│  │                    NP                           │    │
│  │  ┌─────────────────────────────────────────┐    │    │
│  │  │                 NP-COMPLETE             │    │    │
│  │  │  ┌─────────────────────────────────┐    │    │    │
│  │  │  │               P                 │    │    │    │
│  │  │  └─────────────────────────────────┘    │    │    │
│  │  └─────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘

ALGORITHMS BY COMPLEXITY CLASS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

P Problems (Efficiently Solvable):
• Binary Search        O(log n)
  Problem: Find target in sorted array
  Type: Search problem
  
• Merge Sort           O(n log n)  
  Problem: Sort array of elements
  Type: Sorting problem
  
• Dijkstra's Algorithm O(V² + E)
  Problem: Find shortest path in weighted graph
  Type: Graph optimization problem
  
• Matrix Multiplication O(n³)
  Problem: Multiply two n×n matrices
  Type: Algebraic computation problem

NP Problems (Solution Verifiable in Polynomial Time):
• Subset Sum Verification
  Problem: Given set and sum, verify if subset exists
  Type: Decision problem (checking solutions)
  
• Graph Coloring Verification
  Problem: Verify if graph can be colored with k colors
  Type: Graph decision problem
  
• Hamiltonian Path Verification
  Problem: Verify if path visits each vertex exactly once
  Type: Graph traversal decision problem
  
• Boolean Satisfiability (SAT) Verification
  Problem: Verify if boolean formula can be satisfied
  Type: Logic decision problem

NP-Complete Problems (Hardest in NP):
• 3-SAT (Boolean Satisfiability)
  Problem: Can boolean formula with 3 literals per clause be satisfied?
  Type: Logic decision problem (first proven NP-Complete)
  
• Hamiltonian Path/Cycle
  Problem: Does path/cycle visiting each vertex once exist?
  Type: Graph traversal decision problem
  
• Traveling Salesman (Decision Version)
  Problem: Is there tour visiting all cities within cost limit?
  Type: Graph optimization decision problem
  
• Vertex Cover
  Problem: Can k vertices cover all edges in graph?
  Type: Graph covering decision problem
  
• Knapsack Problem
  Problem: Can items fit in knapsack with value ≥ target?
  Type: Combinatorial optimization decision problem

NP-Hard Problems (At Least as Hard as NP-Complete):
• Traveling Salesman (Optimization)
  Problem: Find shortest tour visiting all cities
  Type: Graph optimization problem (not just yes/no)
  
• Maximum Clique
  Problem: Find largest complete subgraph
  Type: Graph optimization problem
  
• Minimum Vertex Cover
  Problem: Find smallest set of vertices covering all edges
  Type: Graph optimization problem
  
• Halting Problem
  Problem: Will given program halt on given input?
  Type: Undecidable problem (not even in NP)
        """)
    
    def show_goodbye(self):
        """Display goodbye message"""
        self.clear_screen()
        print("Thanks for playing!")
        print("Keep exploring the fascinating world of computational complexity!")
        print()
        print("Remember: P vs NP is still unsolved... maybe you'll solve it someday! 🤔")
        print()
    
    def show_llm_question(self, question_data: 'LLMQuestion'):
        """Display an LLM-generated question"""
        self.clear_screen()
        print(f"AI GENERATED QUESTION")
        print(f"Complexity Class: {question_data.complexity_class}")
        print(f"Difficulty: {'★' * question_data.difficulty}")
        print("=" * 50)
        print(question_data.question)
        print()
        
        for i, option in enumerate(question_data.options, 1):
            print(f"{i}. {option}")
        print()
    
    def get_llm_answer(self, num_options: int) -> int:
        """Get answer choice for LLM question with improved UX"""
        while True:
            try:
                choice = input(f"Enter your choice (1-{num_options}) or 'q' to quit: ").strip().lower()
                
                if choice == 'q' or choice == 'quit':
                    return -1  # Signal to quit
                
                choice_num = int(choice)
                if 1 <= choice_num <= num_options:
                    return choice_num - 1  # Return 0-based index
                else:
                    print(f"Please enter a number between 1 and {num_options}")
            except ValueError:
                print("Please enter a valid number or 'q' to quit")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                return -1
    
    def show_llm_result(self, correct: bool, question_data: 'LLMQuestion', user_answer: str):
        """Show result of LLM question"""
        print()
        print("=" * 50)
        if correct:
            print("✓ CORRECT!")
        else:
            print("✗ INCORRECT")
            print(f"Your answer: {user_answer}")
            print(f"Correct answer: {question_data.correct_answer}")
        
        print()
        print("EXPLANATION:")
        print(question_data.explanation)
        print()
        
        # Offer detailed explanation
        while True:
            choice = input("Would you like a detailed explanation? (y/n): ").lower().strip()
            if choice in ['y', 'yes']:
                return 'detailed'
            elif choice in ['n', 'no']:
                return 'continue'
            else:
                print("Please answer y or n")
    
    def show_detailed_explanation(self, explanation: str):
        """Show detailed AI-generated explanation"""
        self.clear_screen()
        print("DETAILED EXPLANATION")
        print("=" * 50)
        print(explanation)
        print()
        input("Press Enter to continue...")
    
    def show_ai_mode_menu(self):
        """Show AI question mode menu"""
        self.clear_screen()
        print("AI QUESTION MODE")
        print("=" * 30)
        print("Generate questions using Claude AI!")
        print()
        print("1. P Problems")
        print("2. NP Problems")
        print("3. NP-Complete Problems")
        print("4. NP-Hard Problems")
        print("5. Mixed Conceptual Questions")
        print("6. Back to Main Menu")
        print()
        
        while True:
            choice = input("Enter choice (1-6): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6']:
                return choice
            print("Invalid choice. Please enter 1-6.")
    
    def show_ai_unavailable(self):
        """Show message when AI features are not available"""
        self.clear_screen()
        print("AI FEATURES UNAVAILABLE")
        print("=" * 30)
        print("AI question generation requires:")
        print("1. anthropic library installed")
        print("2. ANTHROPIC_API_KEY environment variable set")
        print()
        print("To enable AI features:")
        print("1. pip install anthropic python-dotenv")
        print("2. Copy .env.example to .env")
        print("3. Add your Anthropic API key to .env")
        print()
        input("Press Enter to return to main menu...")
    
    def show_loading_spinner(self, message: str = "Loading", duration: float = 2.0):
        """Show an animated loading spinner"""
        spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        start_time = time.time()
        i = 0
        
        while time.time() - start_time < duration:
            sys.stdout.write(f'\r{spinner_chars[i % len(spinner_chars)]} {message}...')
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        
        sys.stdout.write('\r' + ' ' * (len(message) + 10) + '\r')
        sys.stdout.flush()
    
    def show_generating_question(self, complexity_class: str = ""):
        """Show question generation progress"""
        if complexity_class:
            message = f"🤖 Generating {complexity_class} question"
        else:
            message = "🤖 Generating question"
        
        print(message + "...")
        self.show_loading_spinner("Thinking", 1.5)
    
    def show_background_generation_status(self, active: bool = True):
        """Show background generation status"""
        if active:
            print("📚 Background question generation active")
        else:
            print("📚 Background question generation paused")
    
    def show_cache_status(self, cached_count: int, total_requested: int):
        """Show cache performance info"""
        cache_hit_rate = (cached_count / total_requested * 100) if total_requested > 0 else 0
        print(f"📊 Cache performance: {cached_count}/{total_requested} ({cache_hit_rate:.1f}% hit rate)")
    
    def get_answer_with_timeout(self, prompt: str, timeout: float = 30.0) -> str:
        """Get user input with timeout capability"""
        result = [None]
        
        def get_input():
            try:
                result[0] = input(prompt)
            except (EOFError, KeyboardInterrupt):
                result[0] = "quit"
        
        thread = threading.Thread(target=get_input)
        thread.daemon = True
        thread.start()
        thread.join(timeout)
        
        if thread.is_alive():
            print("\n⏰ Input timed out. Using default value.")
            return "quit"
        
        return result[0] if result[0] is not None else "quit"