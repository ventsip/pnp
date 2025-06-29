#!/usr/bin/env python3
"""
Demo of the Complexity Theory Learning Game
Shows examples of problems from each complexity class
"""

from problems.p_problems import PProblemSet
from problems.np_problems import NPProblemSet
from problems.npc_problems import NPCompleteProblemSet
from problems.nph_problems import NPHardProblemSet

def demo_complexity_class(name, problem_set, num_examples=2):
    """Demo problems from a complexity class"""
    print(f"\n{'='*60}")
    print(f"  {name} PROBLEMS")
    print(f"{'='*60}")
    
    for i in range(min(num_examples, len(problem_set.problems))):
        problem = problem_set.problems[i]
        problem.generate_instance()
        
        print(f"\n--- Problem {i+1}: {problem.title} ---")
        print(f"Complexity: {problem.complexity_class}")
        print(f"Difficulty: {'★' * problem.difficulty}")
        print(f"Type: {problem.problem_type}")
        print(f"\nDescription:")
        print(problem.description)
        print(f"\nHint: {problem.hint}")
        print(f"\nExplanation:")
        print(problem.explanation)

def main():
    print("COMPLEXITY THEORY LEARNING GAME - DEMO")
    print("Learn P, NP, NP-Complete, and NP-Hard Problems")
    
    # Initialize problem sets
    p_problems = PProblemSet()
    np_problems = NPProblemSet()
    npc_problems = NPCompleteProblemSet()
    nph_problems = NPHardProblemSet()
    
    # Demo each complexity class
    demo_complexity_class("P (POLYNOMIAL TIME)", p_problems)
    demo_complexity_class("NP (NONDETERMINISTIC POLYNOMIAL)", np_problems)
    demo_complexity_class("NP-COMPLETE", npc_problems)
    demo_complexity_class("NP-HARD", nph_problems)
    
    print(f"\n{'='*60}")
    print("  COMPLEXITY THEORY OVERVIEW")
    print(f"{'='*60}")
    
    print("""
P Problems:
- Can be SOLVED in polynomial time
- Examples: Sorting, searching, shortest path
- These are "easy" problems

NP Problems:
- Solutions can be VERIFIED in polynomial time
- May take exponential time to FIND solutions
- Examples: Checking subset sums, verifying colorings

NP-Complete Problems:
- Hardest problems in NP
- Every NP problem reduces to them
- If any has polynomial solution, then P = NP
- Examples: SAT, Hamiltonian Path, Vertex Cover

NP-Hard Problems:
- At least as hard as NP-Complete
- Often optimization versions of NP-Complete problems
- Examples: TSP optimization, Maximum Clique

THE BIG QUESTION: Does P = NP?
- One of computer science's greatest unsolved problems
- Clay Millennium Prize: $1,000,000
- Most believe P ≠ NP (some problems are fundamentally harder)
    """)
    
    print(f"\n{'='*60}")
    print("To play the full interactive game, run: python3 main.py")
    print("(Note: Interactive mode requires terminal input)")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()