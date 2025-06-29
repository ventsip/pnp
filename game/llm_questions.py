"""
LLM-powered question generation for complexity theory game
"""

import os
import json
import re
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

try:
    import anthropic
    from dotenv import load_dotenv
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False

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

class LLMQuestionBank:
    """Manages a bank of LLM-generated questions with caching"""
    
    def __init__(self, cache_file: str = "llm_questions_cache.json"):
        self.cache_file = cache_file
        self.cache = self._load_cache()
        self.generator = None
        
        if LLM_AVAILABLE:
            try:
                self.generator = LLMQuestionGenerator()
            except (ImportError, ValueError) as e:
                print(f"LLM features disabled: {e}")
    
    def _load_cache(self) -> Dict[str, List[Dict]]:
        """Load cached questions from file"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {}
    
    def _save_cache(self):
        """Save questions to cache file"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except IOError:
            pass
    
    def get_question(self, complexity_class: str, difficulty: int = 3) -> Optional[LLMQuestion]:
        """Get a question, generating if needed"""
        if not self.generator:
            return None
        
        cache_key = f"{complexity_class}_{difficulty}"
        
        # Try to get from cache first
        if cache_key in self.cache and self.cache[cache_key]:
            question_data = self.cache[cache_key].pop(0)
            self._save_cache()
            return LLMQuestion(**question_data)
        
        # Generate new question
        question = self.generator.generate_question(complexity_class, difficulty)
        if question:
            # Cache additional questions for future use
            self._cache_questions(complexity_class, difficulty, 3)
        
        return question
    
    def _cache_questions(self, complexity_class: str, difficulty: int, count: int):
        """Generate and cache multiple questions"""
        cache_key = f"{complexity_class}_{difficulty}"
        
        if cache_key not in self.cache:
            self.cache[cache_key] = []
        
        for _ in range(count):
            question = self.generator.generate_question(complexity_class, difficulty)
            if question:
                question_dict = {
                    'question': question.question,
                    'options': question.options,
                    'correct_answer': question.correct_answer,
                    'explanation': question.explanation,
                    'complexity_class': question.complexity_class,
                    'difficulty': question.difficulty
                }
                self.cache[cache_key].append(question_dict)
        
        self._save_cache()
    
    def is_available(self) -> bool:
        """Check if LLM features are available"""
        return self.generator is not None