#!/usr/bin/env python3
"""
Interactive Demo of the Complexity Theory Learning Game
Simulates a full game session to show all features
"""

from problems.p_problems import PProblemSet
from problems.np_problems import NPProblemSet
from problems.npc_problems import NPCompleteProblemSet
from problems.nph_problems import NPHardProblemSet
from game.scoring import ScoreManager
import time

def simulate_welcome():
    print("=" * 60)
    print("    COMPLEXITY THEORY LEARNING GAME")
    print("    Learn P, NP, NP-Complete, and NP-Hard Problems")
    print("=" * 60)
    print()
    print("Welcome! This game will teach you about computational complexity.")
    print("You'll solve problems from different complexity classes and")
    print("learn what makes some problems harder than others.")
    print()
    print("[Simulated: Press Enter to continue...]")
    print()

def simulate_main_menu():
    print("MAIN MENU")
    print("-" * 20)
    print("1. Tutorial Mode (Learn each complexity class)")
    print("2. Challenge Mode (Mixed problems with scoring)")
    print("3. Theory Reference (Educational content)")
    print("4. View Scores & Statistics")
    print("5. Quit")
    print()
    print("[Simulated choice: 1 - Tutorial Mode]")
    print()

def simulate_tutorial_problem(problem, user_answer, is_correct):
    print(f"PROBLEM: {problem.title}")
    print(f"Complexity Class: {problem.complexity_class}")
    print(f"Difficulty: {'★' * problem.difficulty}")
    print("-" * 50)
    print(problem.description)
    print()
    
    if problem.hint:
        print("[Would you like a hint? y]")
        print(f"HINT: {problem.hint}")
        print()
    
    print(f"[Your answer: {user_answer}]")
    print()
    print("=" * 50)
    if is_correct:
        print("✓ CORRECT!")
    else:
        print("✗ INCORRECT")
    
    print()
    print("EXPLANATION:")
    print(problem.explanation)
    print()
    print("[Press Enter to continue...]")
    print()

def simulate_challenge_mode():
    print("CHALLENGE MODE")
    print("=" * 30)
    print("You will face 5 random problems from all complexity classes.")
    print("Points are awarded based on:")
    print("- Complexity class (P=100, NP=200, NP-C=300, NP-H=400)")
    print("- Problem difficulty (1-5 stars)")
    print("- Speed of solving (time bonus)")
    print()
    print("[Press Enter to begin the challenge...]")
    print()
    
    # Simulate scoring
    score_manager = ScoreManager()
    
    # Simulate 3 problems
    problems_data = [
        ("P", 1, 15, True, "Sorting problem"),
        ("NP-Complete", 4, 45, True, "SAT problem"),
        ("NP-Hard", 5, 30, False, "TSP problem")
    ]
    
    total_score = 0
    for i, (complexity, difficulty, solve_time, correct, desc) in enumerate(problems_data, 1):
        print(f"--- Challenge Problem {i}: {desc} ---")
        if correct:
            points = score_manager.calculate_points(complexity, solve_time, difficulty)
            total_score += points
            print(f"✓ CORRECT! +{points} points")
        else:
            print("✗ INCORRECT! +0 points")
        score_manager.record_attempt(complexity, correct)
        print()
    
    print("CHALLENGE COMPLETE!")
    print("=" * 30)
    print(f"Final Score: {total_score} points")
    print()
    
    if total_score >= 1000:
        print("🏆 EXCELLENT! You're a complexity theory expert!")
    else:
        print("📚 Keep studying! Practice makes perfect!")
    print()

def simulate_theory_reference():
    print("THEORY REFERENCE")
    print("=" * 30)
    print("1. P Problems")
    print("2. NP Problems") 
    print("3. NP-Complete Problems")
    print("4. NP-Hard Problems")
    print("5. P vs NP Question")
    print("6. Back to Main Menu")
    print()
    print("[Simulated choice: 5 - P vs NP Question]")
    print()
    
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
    print("[Press Enter to continue...]")
    print()

def main():
    print("🎮 INTERACTIVE GAME SESSION SIMULATION")
    print("=" * 60)
    
    # Welcome screen
    simulate_welcome()
    
    # Main menu
    simulate_main_menu()
    
    # Tutorial mode
    print("🎓 TUTORIAL MODE - Learning P Problems")
    print("=" * 50)
    print("""
P (Polynomial Time) Problems:
- Can be solved in polynomial time O(n^k)
- Examples: Sorting, searching, shortest path
- These are considered 'easy' problems
- Every computer can solve them efficiently
    """)
    print("[Press Enter to start solving problems...]")
    print()
    
    # Simulate tutorial problems
    p_problems = PProblemSet()
    
    # Problem 1: Sorting
    problem1 = p_problems.problems[0]
    problem1.generate_instance()
    simulate_tutorial_problem(problem1, "yes", True)
    
    # Problem 2: Search
    problem2 = p_problems.problems[1]
    problem2.generate_instance()
    simulate_tutorial_problem(problem2, "no", problem2.check_decision(False))
    
    print("🏆 TUTORIAL COMPLETE!")
    print("You've learned about P problems! Next: NP problems...")
    print()
    
    # Challenge mode
    print("🎯 CHALLENGE MODE SIMULATION")
    print("=" * 50)
    simulate_challenge_mode()
    
    # Theory reference
    print("📚 THEORY REFERENCE SIMULATION")
    print("=" * 50)
    simulate_theory_reference()
    
    print("🎮 GAME SESSION COMPLETE!")
    print("=" * 60)
    print("This demonstrates the full interactive experience.")
    print("Run 'python3 main.py' in a terminal for the real game!")
    print()
    print("Key features shown:")
    print("✓ Tutorial mode with guided learning")
    print("✓ Challenge mode with scoring system")
    print("✓ Theory reference for quick review")
    print("✓ Progressive difficulty and detailed explanations")
    print("✓ Interactive problem solving with hints")

if __name__ == "__main__":
    main()