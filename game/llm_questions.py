"""
LLM-powered question generation for complexity theory game
"""

import os
import json
import re
import asyncio
import threading
import time
import gzip
from typing import Dict, Any, Optional, List, Deque
from dataclasses import dataclass
from collections import deque
from concurrent.futures import ThreadPoolExecutor

try:
    import anthropic
    from dotenv import load_dotenv
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False

try:
    from .performance_monitor import performance_monitor, PerformanceContext
except ImportError:
    # Fallback if performance monitor is not available
    class PerformanceContext:
        def __init__(self, *args, **kwargs):
            pass
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass
    performance_monitor = None

@dataclass
class LLMQuestion:
    """Data class for LLM-generated questions"""
    question: str
    options: List[str]
    correct_answer: str
    explanation: str
    complexity_class: str
    difficulty: int

class LLMQuestionGenerator:
    """Generates complexity theory questions using Claude AI"""
    
    def __init__(self):
        if not LLM_AVAILABLE:
            raise ImportError("anthropic and python-dotenv packages required for LLM features")
        
        # Load environment variables
        load_dotenv()
        
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable required")
        
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = os.getenv('CLAUDE_MODEL', 'claude-3-haiku-20240307')
        
        self.system_prompt = """You are an expert in computational complexity theory. 
        Generate educational questions about P, NP, NP-Complete, and NP-Hard problems.
        
        Your questions should:
        1. Be factually accurate - verify all statements about complexity classes
        2. Have clear, unambiguous answers with only ONE correct option
        3. Include helpful explanations that are consistent with the correct answer
        4. Be appropriate for computer science students
        5. Use precise technical language
        
        CRITICAL: Ensure all options are technically accurate statements, even if only one is the best answer for the specific question. Avoid creating obviously false statements.
        
        Return responses in valid JSON format only."""
    
    def _clean_json_response(self, response_text: str) -> str:
        """Clean and extract JSON from LLM response"""
        response_text = response_text.strip()
        
        # Try to extract JSON from response if it's wrapped in text
        if '```json' in response_text:
            start = response_text.find('```json') + 7
            end = response_text.find('```', start)
            if end != -1:
                response_text = response_text[start:end].strip()
        elif '```' in response_text:
            start = response_text.find('```') + 3
            end = response_text.find('```', start)
            if end != -1:
                response_text = response_text[start:end].strip()
        
        # Remove control characters
        response_text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', response_text)
        
        # Fix common JSON formatting issues
        response_text = response_text.replace('\n', ' ').replace('\r', ' ')
        response_text = re.sub(r'\s+', ' ', response_text)
        
        return response_text
    
    def _validate_question(self, question_data: Dict, complexity_class: str) -> bool:
        """Validate question for basic correctness"""
        try:
            # Check required fields
            required_fields = ['question', 'options', 'correct_answer', 'explanation']
            for field in required_fields:
                if field not in question_data:
                    return False
            
            # Check correct answer is in options
            if question_data['correct_answer'] not in question_data['options']:
                return False
            
            # Basic fact checking for P problems
            if complexity_class == 'P':
                correct_answer = question_data['correct_answer'].lower()
                # Check for common misconceptions
                if 'no known efficient algorithm' in correct_answer:
                    return False
                if 'exponential time' in correct_answer:
                    return False
                if 'subset of np-complete' in correct_answer:
                    return False
            
            return True
            
        except Exception:
            return False
    
    def generate_question(self, complexity_class: str, difficulty: int = 3) -> Optional[LLMQuestion]:
        """Generate a question for the specified complexity class"""
        try:
            prompt = self._create_prompt(complexity_class, difficulty)
            
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.7,
                system=self.system_prompt,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text
            # Clean response text to handle control characters
            response_text = self._clean_json_response(response_text)
            
            question_data = json.loads(response_text)
            
            # Validate question quality
            if not self._validate_question(question_data, complexity_class):
                print(f"Generated question failed validation for {complexity_class}")
                return None
            
            return LLMQuestion(
                question=question_data['question'],
                options=question_data['options'],
                correct_answer=question_data['correct_answer'],
                explanation=question_data['explanation'],
                complexity_class=complexity_class,
                difficulty=difficulty
            )
            
        except Exception as e:
            print(f"Error generating LLM question: {e}")
            return None
    
    def _create_prompt(self, complexity_class: str, difficulty: int) -> str:
        """Create a prompt for generating questions"""
        difficulty_desc = {
            1: "beginner (basic concepts)",
            2: "easy (simple examples)",
            3: "medium (practical applications)",
            4: "hard (complex analysis)",
            5: "expert (advanced theory)"
        }
        
        examples = {
            'P': "Binary search, sorting algorithms, shortest path (Dijkstra), matrix multiplication",
            'NP': "Verifying Hamiltonian paths, checking graph colorings, verifying subset sums",
            'NP-Complete': "3-SAT, Hamiltonian path, Traveling Salesman (decision), Vertex Cover, Knapsack (decision)",
            'NP-Hard': "Traveling Salesman (optimization), Maximum Clique, Halting Problem"
        }
        
        # Add specific fact checking for complexity classes
        fact_checks = {
            'P': """
FACT CHECK for P problems:
- P problems CAN be solved in polynomial time by deterministic algorithms
- P problems DO have known efficient algorithms (by definition)
- P is a SUBSET of NP, not a superset
- P problems are NOT NP-complete (unless P=NP, which is unproven)
- Examples: sorting, binary search, shortest path, matrix multiplication""",
            'NP': """
FACT CHECK for NP problems:
- NP problems can be VERIFIED in polynomial time
- NP problems may or may not be solvable in polynomial time
- P ⊆ NP (all P problems are also NP)
- NP includes both P and NP-complete problems""",
            'NP-Complete': """
FACT CHECK for NP-Complete problems:
- NP-complete problems are the hardest problems in NP
- Every NP problem reduces to any NP-complete problem
- No known polynomial-time algorithms exist for NP-complete problems
- If any NP-complete problem has polynomial solution, then P=NP""",
            'NP-Hard': """
FACT CHECK for NP-Hard problems:
- At least as hard as NP-complete problems
- May not be in NP themselves (could be undecidable)
- Often optimization versions of NP-complete problems"""
        }
        
        fact_check = fact_checks.get(complexity_class, "")
        
        return f"""Generate a {difficulty_desc.get(difficulty, 'medium')} level question about {complexity_class} problems.
{fact_check}

Examples of {complexity_class} problems: {examples.get(complexity_class, '')}.

The question should test understanding of:
- What {complexity_class} means
- Examples of {complexity_class} problems
- How to identify {complexity_class} problems
- Relationships between complexity classes

IMPORTANT REQUIREMENTS:
1. All options must be technically accurate statements (avoid obviously false claims)
2. Only ONE option should be the best/most complete answer to the question
3. The correct_answer field must exactly match one of the options
4. Explanation must be consistent with the marked correct answer
5. Double-check all complexity theory facts before including them

Format your response as JSON:
{{
    "question": "The question text",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "Option A",
    "explanation": "Detailed explanation of why the answer is correct and why other options are wrong"
}}

Make sure the question is educational and the explanation helps students learn."""

    def generate_conceptual_question(self, topic: str) -> Optional[LLMQuestion]:
        """Generate a conceptual question about complexity theory"""
        try:
            prompt = f"""Generate a conceptual question about {topic} in computational complexity theory.

Topics could include:
- P vs NP problem
- Reductions between problems
- Time and space complexity
- Decidability and undecidability
- Polynomial time algorithms
- NP-completeness proofs

Format as JSON with question, options, correct_answer, and explanation fields."""

            message = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.7,
                system=self.system_prompt,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text
            # Clean response text to handle control characters
            response_text = self._clean_json_response(response_text)
            
            question_data = json.loads(response_text)
            
            return LLMQuestion(
                question=question_data['question'],
                options=question_data['options'],
                correct_answer=question_data['correct_answer'],
                explanation=question_data['explanation'],
                complexity_class="Conceptual",
                difficulty=3
            )
            
        except Exception as e:
            print(f"Error generating conceptual question: {e}")
            return None

    def generate_detailed_explanation(self, question_data: 'LLMQuestion', user_answer: str) -> Optional[str]:
        """Generate a detailed explanation for a question and user's answer"""
        try:
            prompt = f"""You are an expert in computational complexity theory. A student just answered a question about {question_data.complexity_class} problems.

Question: {question_data.question}

Options:
{chr(10).join([f"{i+1}. {opt}" for i, opt in enumerate(question_data.options)])}

Correct Answer: {question_data.correct_answer}
Student's Answer: {user_answer}
Student was: {'CORRECT' if user_answer == question_data.correct_answer else 'INCORRECT'}

Previous explanation: {question_data.explanation}

Please provide a detailed, educational explanation that:
1. Explains WHY the correct answer is correct in depth
2. Explains WHY each incorrect option is wrong
3. Provides additional context about {question_data.complexity_class} problems
4. Uses examples and analogies where helpful
5. Connects to broader complexity theory concepts
6. If student was wrong, gently explains their misconception

Make this explanation comprehensive but accessible to computer science students. Focus on building deep understanding.

IMPORTANT: Return ONLY plain text explanation, NOT JSON format. Do not wrap the response in JSON structure."""

            message = self.client.messages.create(
                model=self.model,
                max_tokens=1500,  # Longer for detailed explanations
                temperature=0.3,  # Lower temperature for more focused explanations
                system=self.system_prompt,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return message.content[0].text.strip()
            
        except Exception as e:
            print(f"Error generating detailed explanation: {e}")
            return None

class OptimizedLLMQuestionBank:
    """Optimized question bank with async generation, memory caching, and background prefetching"""
    
    def __init__(self, cache_file: str = "llm_questions_cache.json", memory_cache_size: int = 50, use_compression: bool = True):
        self.cache_file = cache_file
        self.use_compression = use_compression
        self.disk_cache = self._load_cache()
        self.memory_cache: Dict[str, Deque[LLMQuestion]] = {}
        self.memory_cache_size = memory_cache_size
        self.generator = None
        self.background_executor = ThreadPoolExecutor(max_workers=2)
        self.generation_lock = threading.Lock()
        self.prefetch_running = False
        
        if LLM_AVAILABLE:
            try:
                self.generator = LLMQuestionGenerator()
                self._initialize_memory_cache()
                self._start_background_prefetch()
            except (ImportError, ValueError) as e:
                print(f"LLM features disabled: {e}")
    
    def _load_cache(self) -> Dict[str, List[Dict]]:
        """Load cached questions from file with optional compression"""
        if os.path.exists(self.cache_file):
            try:
                if self.use_compression and self.cache_file.endswith('.gz'):
                    with gzip.open(self.cache_file, 'rt', encoding='utf-8') as f:
                        return json.load(f)
                else:
                    with open(self.cache_file, 'r') as f:
                        return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {}
    
    def _save_cache(self):
        """Save questions to cache file with optional compression"""
        try:
            if self.use_compression and self.cache_file.endswith('.gz'):
                with gzip.open(self.cache_file, 'wt', encoding='utf-8') as f:
                    json.dump(self.disk_cache, f, separators=(',', ':'))
            else:
                with open(self.cache_file, 'w') as f:
                    json.dump(self.disk_cache, f, indent=2)
        except IOError:
            pass
    
    def _initialize_memory_cache(self):
        """Initialize memory cache with existing questions"""
        for cache_key, questions in self.disk_cache.items():
            if questions:
                self.memory_cache[cache_key] = deque(maxlen=self.memory_cache_size)
                # Load up to 5 questions into memory cache
                for question_data in questions[:5]:
                    try:
                        question = LLMQuestion(**question_data)
                        self.memory_cache[cache_key].append(question)
                    except Exception:
                        continue
    
    def _start_background_prefetch(self):
        """Start background prefetching for common question types"""
        if self.prefetch_running:
            return
        
        self.prefetch_running = True
        common_types = [
            ('P', 3), ('NP', 3), ('NP-Complete', 3), ('NP-Hard', 3), ('Conceptual', 3)
        ]
        
        for complexity_class, difficulty in common_types:
            self.background_executor.submit(self._prefetch_questions, complexity_class, difficulty)
    
    def _prefetch_questions(self, complexity_class: str, difficulty: int):
        """Prefetch questions in background thread"""
        cache_key = f"{complexity_class}_{difficulty}"
        
        with self.generation_lock:
            if cache_key not in self.memory_cache:
                self.memory_cache[cache_key] = deque(maxlen=self.memory_cache_size)
            
            current_count = len(self.memory_cache[cache_key])
            target_count = min(10, self.memory_cache_size // 2)  # Keep 10 questions ready
            
            if current_count < target_count:
                questions_to_generate = target_count - current_count
                self._generate_batch_questions(complexity_class, difficulty, questions_to_generate)
    
    def _generate_batch_questions(self, complexity_class: str, difficulty: int, count: int):
        """Generate multiple questions in batch for better efficiency"""
        cache_key = f"{complexity_class}_{difficulty}"
        
        for _ in range(count):
            try:
                if complexity_class == 'Conceptual':
                    if self.generator:
                        question = self.generator.generate_conceptual_question("complexity theory")
                else:
                    question = self.generator.generate_question(complexity_class, difficulty)
                
                if question:
                    self.memory_cache[cache_key].append(question)
                    
                    # Also add to disk cache for persistence
                    if cache_key not in self.disk_cache:
                        self.disk_cache[cache_key] = []
                    
                    question_dict = {
                        'question': question.question,
                        'options': question.options,
                        'correct_answer': question.correct_answer,
                        'explanation': question.explanation,
                        'complexity_class': question.complexity_class,
                        'difficulty': question.difficulty
                    }
                    self.disk_cache[cache_key].append(question_dict)
                    
                    # Limit disk cache size
                    if len(self.disk_cache[cache_key]) > 20:
                        self.disk_cache[cache_key] = self.disk_cache[cache_key][-20:]
            except Exception as e:
                print(f"Error generating question in batch: {e}")
                continue
        
        # Save to disk periodically
        if len(self.disk_cache.get(cache_key, [])) % 5 == 0:
            self._save_cache()

    def get_question_fast(self, complexity_class: str, difficulty: int = 3) -> Optional[LLMQuestion]:
        """Get a question with optimized caching - returns immediately if available"""
        if not self.generator:
            return None
        
        cache_key = f"{complexity_class}_{difficulty}"
        
        with PerformanceContext("get_question_fast", "llm"):
            # Try memory cache first (fastest)
            if cache_key in self.memory_cache and self.memory_cache[cache_key]:
                with PerformanceContext("memory_cache_hit", "cache"):
                    question = self.memory_cache[cache_key].popleft()
                    
                    # Record cache hit
                    if performance_monitor:
                        performance_monitor.record_metric("cache_hits", 1, "cache")
                    
                    # Trigger background refill if running low
                    if len(self.memory_cache[cache_key]) < 3:
                        self.background_executor.submit(self._prefetch_questions, complexity_class, difficulty)
                    
                    return question
            
            # Fallback to disk cache
            if cache_key in self.disk_cache and self.disk_cache[cache_key]:
                with PerformanceContext("disk_cache_hit", "cache"):
                    question_data = self.disk_cache[cache_key].pop(0)
                    self._save_cache()
                    
                    # Record cache hit
                    if performance_monitor:
                        performance_monitor.record_metric("cache_hits", 1, "cache")
                    
                    return LLMQuestion(**question_data)
            
            # Last resort: generate synchronously (with user feedback)
            print("🤖 Generating new question...")
            with PerformanceContext("synchronous_generation", "llm"):
                question = self._generate_question_with_feedback(complexity_class, difficulty)
                
                # Record cache miss
                if performance_monitor:
                    performance_monitor.record_metric("cache_misses", 1, "cache")
                
                if question:
                    # Start background generation for future questions
                    self.background_executor.submit(self._prefetch_questions, complexity_class, difficulty)
                
                return question
    
    def _generate_question_with_feedback(self, complexity_class: str, difficulty: int) -> Optional[LLMQuestion]:
        """Generate question with user feedback"""
        try:
            if complexity_class == 'Conceptual':
                if self.generator:
                    return self.generator.generate_conceptual_question("complexity theory")
                else:
                    return None
            else:
                return self.generator.generate_question(complexity_class, difficulty)
        except Exception as e:
            print(f"Error generating question: {e}")
            return None
    
    def get_question(self, complexity_class: str, difficulty: int = 3) -> Optional[LLMQuestion]:
        """Legacy method - redirects to optimized version"""
        return self.get_question_fast(complexity_class, difficulty)
    
    def is_available(self) -> bool:
        """Check if LLM features are available"""
        return self.generator is not None
    
    def _prune_cache(self, max_questions_per_class: int = 100):
        """Prune old cached questions to reduce memory usage"""
        with self.generation_lock:
            for cache_key in list(self.disk_cache.keys()):
                if len(self.disk_cache[cache_key]) > max_questions_per_class:
                    # Keep only the most recent questions
                    self.disk_cache[cache_key] = self.disk_cache[cache_key][-max_questions_per_class:]
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics for monitoring"""
        memory_cache_count = sum(len(cache) for cache in self.memory_cache.values())
        disk_cache_count = sum(len(questions) for questions in self.disk_cache.values())
        
        return {
            "memory_cache_size": memory_cache_count,
            "disk_cache_size": disk_cache_count,
            "memory_cache_limit": self.memory_cache_size,
            "compression_enabled": self.use_compression,
            "cache_categories": list(self.memory_cache.keys())
        }
    
    def shutdown(self):
        """Clean shutdown of background processes"""
        self.prefetch_running = False
        self.background_executor.shutdown(wait=True)
        self._prune_cache()  # Prune before saving
        self._save_cache()

class LLMQuestionBank:
    """Legacy question bank - kept for backward compatibility"""
    
    def __init__(self, cache_file: str = "llm_questions_cache.json"):
        self.optimized_bank = OptimizedLLMQuestionBank(cache_file)
        self.generator = self.optimized_bank.generator
    
    def get_question(self, complexity_class: str, difficulty: int = 3) -> Optional[LLMQuestion]:
        """Get a question using the optimized bank"""
        return self.optimized_bank.get_question_fast(complexity_class, difficulty)
    
    def is_available(self) -> bool:
        """Check if LLM features are available"""
        return self.optimized_bank.is_available()
    
