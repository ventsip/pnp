# Complexity Theory Learning Game

An interactive Python game designed to teach the fundamental concepts of computational complexity theory, specifically P, NP, NP-Complete, and NP-Hard problems.

## 🎯 Learning Objectives

By playing this game, you will:
- Understand the differences between P, NP, NP-Complete, and NP-Hard complexity classes
- Learn to recognize problems from each complexity class
- Practice verifying solutions vs. finding solutions
- Gain intuition about what makes some problems computationally harder than others
- Explore the famous P vs NP question

## 🎮 Game Features

### Game Modes
1. **Tutorial Mode**: Step-by-step introduction to each complexity class with guided examples
2. **Challenge Mode**: Mixed problems with scoring system and time bonuses
3. **Theory Reference**: Educational content explaining complexity theory concepts

### Problem Types
- **P Problems**: Sorting verification, searching, primality testing, graph connectivity
- **NP Problems**: Subset sum verification, Hamiltonian path verification, graph coloring verification
- **NP-Complete Problems**: SAT, 3-SAT, Hamiltonian path decision, vertex cover, clique
- **NP-Hard Problems**: TSP optimization, knapsack optimization, maximum clique, minimum vertex cover

### Scoring System
- Base points by complexity class (P=100, NP=200, NP-Complete=300, NP-Hard=400)
- Difficulty multipliers (1★ to 5★)
- Time bonuses for quick solving
- Achievement ranks based on total score

## 🚀 How to Play

1. **Install and Run**:
   ```bash
   python main.py
   ```

2. **Choose a Mode**:
   - Start with Tutorial Mode to learn the basics
   - Try Challenge Mode to test your knowledge
   - Use Theory Reference for quick reviews

3. **Solve Problems**:
   - Read problem descriptions carefully
   - Use hints when available
   - Submit your answers
   - Learn from explanations

## 📚 Complexity Classes Explained

### P (Polynomial Time)
- Problems solvable in polynomial time O(n^k)
- Examples: Sorting, searching, shortest path
- Considered "easy" problems that computers can solve efficiently

### NP (Nondeterministic Polynomial)
- Solutions can be **verified** in polynomial time
- May take exponential time to **find** solutions
- Examples: Verifying a subset sum, checking a graph coloring
- P ⊆ NP (all P problems are also NP problems)

### NP-Complete
- The hardest problems in NP
- Every NP problem can be reduced to them
- If any NP-Complete problem has a polynomial solution, then P = NP
- Examples: SAT, Hamiltonian Path, Vertex Cover

### NP-Hard
- At least as hard as NP-Complete problems
- May not be in NP themselves (often optimization problems)
- Examples: TSP optimization, Maximum Clique

## 🎯 Educational Value

This game teaches through:
- **Interactive Problem Solving**: Learn by doing, not just reading
- **Immediate Feedback**: Understand mistakes with detailed explanations
- **Progressive Difficulty**: Start simple, build to complex concepts
- **Visual Examples**: Concrete problems make abstract concepts tangible
- **Gamification**: Scoring and achievements motivate continued learning

## 🔬 The P vs NP Question

One of computer science's greatest unsolved problems:
- **If P = NP**: Every problem with quickly verifiable solutions also has quickly findable solutions
- **If P ≠ NP**: Some problems are fundamentally harder to solve than to verify
- **Current Status**: Unsolved (Clay Millennium Prize: $1,000,000)

## 🛠 Technical Details

### Project Structure
```
complexity-game/
├── main.py              # Main game loop
├── problems/
│   ├── base.py          # Base problem classes
│   ├── p_problems.py    # P complexity problems
│   ├── np_problems.py   # NP complexity problems
│   ├── npc_problems.py  # NP-Complete problems
│   └── nph_problems.py  # NP-Hard problems
└── game/
    ├── ui.py            # User interface
    └── scoring.py       # Scoring system
```

### Requirements
- Python 3.7+
- No external dependencies (uses only standard library)

## 🎓 Perfect For

- **Computer Science Students**: Supplement theoretical coursework with hands-on practice
- **Self-Learners**: Understand complexity theory through interactive examples
- **Interview Preparation**: Practice recognizing problem complexity classes
- **Educators**: Use as a teaching tool for complexity theory concepts

## 🏆 Achievement Ranks

- **Beginner** (0-999 points)
- **Novice Theorist** (1000-1999 points)
- **Problem Solver** (2000-2999 points)
- **Algorithm Expert** (3000-4999 points)
- **Complexity Theory Master** (5000+ points)

Start your journey into computational complexity theory today! 🚀