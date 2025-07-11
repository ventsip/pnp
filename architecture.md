# PnP (Complexity Theory Learning Game) Architecture

## Overview

PnP is an educational game designed to teach computational complexity theory concepts, specifically P, NP, NP-Complete, and NP-Hard problems. The application combines interactive learning with AI-powered question generation to provide a comprehensive learning experience.

## System Architecture

### High-Level Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                        Main Application                         │
│                       (ComplexityGame)                          │
└─────────────────────────┬───────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
    ┌─────────┐    ┌─────────────┐   ┌─────────────┐
    │   UI    │    │   Problems  │   │   AI/LLM    │
    │  Layer  │    │    Layer    │   │   Layer     │
    └─────────┘    └─────────────┘   └─────────────┘
          │               │               │
          ▼               ▼               ▼
    ┌─────────┐    ┌─────────────┐   ┌─────────────┐
    │Scoring &│    │  Problem    │   │  Question   │
    │  Stats  │    │   Cache     │   │    Cache    │
    └─────────┘    └─────────────┘   └─────────────┘
```

## Core Components

### 1. Main Application Layer (`main.py`)

**Class**: `ComplexityGame`

The central orchestrator that manages:

- Game mode selection (Tutorial, Challenge, AI Mode)
- Problem set coordination
- Score tracking and statistics
- Background resource management
- User session flow

**Key Features**:

- Lazy initialization of problem sets
- Background preloading for performance
- Graceful shutdown handling
- Optimized question generation with retry logic

### 2. User Interface Layer (`game/ui.py`)

**Class**: `GameUI`

Handles all user interactions and terminal-based presentation:

- Menu systems and navigation
- Problem presentation
- Answer collection (decision/classification/optimization)
- Results display and explanations
- Loading indicators and progress feedback
- ASCII visualizations of complexity relationships

**Key Features**:

- Hint system integration
- Detailed explanations for AI-generated questions
- Performance metrics display
- Responsive terminal interface

### 3. Problem System (`problems/`)

#### Base Architecture (`problems/base.py`)

**Classes**:

- `Problem`: Abstract base class for all complexity problems
- `OptimizedProblemSet`: Enhanced problem set with caching and background loading
- `ProblemSet`: Legacy compatibility layer

**Key Features**:

- Lazy loading of problem instances
- Thread-safe caching (max 20 problems per set)
- Background preloading with ThreadPoolExecutor
- Instance generation on-demand

#### Problem Types

- **P Problems** (`problems/p_problems.py`): Polynomial-time solvable problems
- **NP Problems** (`problems/np_problems.py`): Nondeterministic polynomial-time problems
- **NP-Complete Problems** (`problems/npc_problems.py`): Complete problems in NP
- **NP-Hard Problems** (`problems/nph_problems.py`): At least as hard as NP-Complete

Each problem type supports:

- Multiple difficulty levels (1-5 stars)
- Different problem formats (decision, classification, optimization)
- Contextual hints and explanations
- Instance generation with varying parameters

### 4. AI/LLM Integration (`game/llm_questions.py`)

#### Question Generation System

**Classes**:

- `LLMQuestionGenerator`: Core Claude AI integration
- `OptimizedLLMQuestionBank`: Advanced caching and prefetching
- `LLMQuestion`: Data structure for AI-generated questions

**Key Features**:

- **Multi-layered Caching**:
  - Memory cache (50 questions, configurable)
  - Disk cache with optional gzip compression
  - Background prefetching for common question types
- **Quality Assurance**:
  - Fact-checking prompts for each complexity class
  - Response validation and JSON cleaning
  - Retry logic for failed generations
- **Performance Optimization**:
  - Async generation with ThreadPoolExecutor
  - Batch question generation
  - Background prefetching for 5 complexity classes

#### AI Features

- **Dynamic Question Generation**: Fresh questions for each complexity class
- **Detailed Explanations**: Context-aware explanations based on user answers
- **Conceptual Questions**: Broader complexity theory concepts
- **Graceful Degradation**: Continues working without AI when unavailable

### 5. Scoring System (`game/scoring.py`)

**Class**: `ScoreManager`

Comprehensive scoring and statistics tracking:

- **Point Calculation**: Based on complexity class, difficulty, and solve time
- **Performance Tracking**: Accuracy by complexity class
- **Rank System**: From "Beginner" to "Complexity Theory Master"
- **Statistics**: Detailed performance analytics

**Scoring Formula**:

```
Points = Base Points × Difficulty Multiplier × Time Bonus
Base Points: P=100, NP=200, NP-Complete=300, NP-Hard=400
Difficulty: 1.0x to 3.0x multiplier
Time Bonus: 1.5x (<10s), 1.2x (<30s), 1.0x (<60s), 0.8x (>60s)
```

### 6. Performance Monitoring (`game/performance_monitor.py`)

**Features**:

- Context-based performance tracking
- Metric collection for cache hits/misses
- Resource usage monitoring
- Performance optimization insights

## Data Flow

### Game Session Flow

1. **Initialization**:
   - Load problem sets (lazy loading)
   - Initialize AI components (if available)
   - Start background prefetching
   - Load cached questions

2. **Mode Selection**:
   - Tutorial: Sequential introduction to each complexity class
   - Challenge: Random mixed problems with scoring
   - AI Mode: Dynamic question generation with Claude AI

3. **Problem Solving**:
   - Problem presentation through UI
   - Answer collection and validation
   - Result display with explanations
   - Score calculation and tracking

4. **AI Question Generation**:
   - Check memory cache first
   - Fallback to disk cache
   - Generate new questions synchronously if needed
   - Background prefetching for future questions

### Caching Strategy

```
Memory Cache (Fast) ──┐
                      ├─── Question Request
Disk Cache (Medium) ──┤
                      │
Live Generation ──────┘
(Slow, with user feedback)
```

## Technical Architecture

### Threading Model

- **Main Thread**: UI and game logic
- **Background Threads**:
  - Problem set preloading (1 thread per set)
  - AI question prefetching (2 threads via ThreadPoolExecutor)
  - Performance monitoring

### Error Handling

- **Graceful Degradation**: AI features disable cleanly when unavailable
- **Retry Logic**: Multiple attempts for question generation
- **Fallback Systems**: Disk cache → memory cache → live generation
- **Resource Cleanup**: Proper shutdown of background processes

### Configuration

**Environment Variables**:

- `ANTHROPIC_API_KEY`: Claude AI API key
- `CLAUDE_MODEL`: AI model selection (default: claude-3-haiku-20240307)

**Files**:

- `.env`: Environment configuration
- `llm_questions_cache.json(.gz)`: Question cache storage
- `pyproject.toml`: Project configuration and dependencies

## Dependencies

### Core Dependencies

- **Python 3.7+**: Base runtime
- **anthropic**: Claude AI integration
- **python-dotenv**: Environment variable management

### Optional Dependencies

- **pytest**: Testing framework
- **black**: Code formatting
- **flake8**: Code linting
- **mypy**: Type checking

## Performance Characteristics

### Optimization Features

1. **Lazy Loading**: Components load only when needed
2. **Background Prefetching**: Common questions pre-generated
3. **Multi-level Caching**: Memory → Disk → Live generation
4. **Compression**: Optional gzip compression for disk cache
5. **Instance Pooling**: Reuse of problem instances where possible

### Scalability Considerations

- **Cache Size Limits**: Configurable memory and disk cache sizes
- **Background Generation**: Non-blocking question generation
- **Resource Management**: Proper cleanup of threads and resources
- **Batch Processing**: Efficient generation of multiple questions

## Educational Design

### Learning Progression

1. **Tutorial Mode**: Structured introduction to each complexity class
2. **Challenge Mode**: Mixed problems to test understanding
3. **AI Mode**: Dynamic, personalized question generation

### Pedagogical Features

- **Hint System**: Context-sensitive help for all problem types
- **Detailed Explanations**: AI-generated explanations tailored to user answers
- **Visual Learning**: ASCII diagrams of complexity relationships
- **Progress Tracking**: Comprehensive statistics and ranking system

## Future Extensibility

The architecture supports easy extension through:

- **Plugin System**: New problem types via base classes
- **AI Model Flexibility**: Configurable AI providers
- **Cache Backends**: Pluggable caching strategies
- **UI Adaptability**: Separation of logic and presentation layers

This modular design enables the system to grow with new complexity theory concepts, different AI providers, and enhanced user interfaces while maintaining performance and educational effectiveness.
