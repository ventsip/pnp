import pytest
import sys
import os
from unittest.mock import patch, MagicMock, mock_open
import json

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.llm_questions import LLMQuestion, LLMQuestionGenerator, LLMQuestionBank


class TestLLMQuestion:
    def test_llm_question_creation(self):
        """Test LLMQuestion dataclass creation"""
        question = LLMQuestion(
            question="What is P?",
            options=["Option 1", "Option 2", "Option 3", "Option 4"],
            correct_answer="Option 1",
            explanation="P is polynomial time",
            complexity_class="P",
            difficulty=2
        )
        
        assert question.question == "What is P?"
        assert len(question.options) == 4
        assert question.correct_answer == "Option 1"
        assert question.explanation == "P is polynomial time"
        assert question.complexity_class == "P"
        assert question.difficulty == 2


class TestLLMQuestionGenerator:
    @patch('game.llm_questions.LLM_AVAILABLE', True)
    @patch('game.llm_questions.load_dotenv')
    @patch('os.getenv')
    @patch('game.llm_questions.anthropic.Anthropic')
    def test_init_success(self, mock_anthropic, mock_getenv, mock_load_dotenv):
        """Test successful LLMQuestionGenerator initialization"""
        mock_getenv.side_effect = lambda key, default=None: {
            'ANTHROPIC_API_KEY': 'test_key',
            'CLAUDE_MODEL': 'claude-3-haiku-20240307'
        }.get(key, default)
        
        generator = LLMQuestionGenerator()
        
        mock_load_dotenv.assert_called_once()
        mock_anthropic.assert_called_once_with(api_key='test_key')
        assert generator.model == 'claude-3-haiku-20240307'
    
    @patch('game.llm_questions.LLM_AVAILABLE', False)
    def test_init_no_llm_available(self):
        """Test initialization when LLM packages not available"""
        with pytest.raises(ImportError, match="anthropic and python-dotenv packages required"):
            LLMQuestionGenerator()
    
    @patch('game.llm_questions.LLM_AVAILABLE', True)
    @patch('game.llm_questions.load_dotenv')
    @patch('os.getenv', return_value=None)
    def test_init_no_api_key(self, mock_getenv, mock_load_dotenv):
        """Test initialization without API key"""
        with pytest.raises(ValueError, match="ANTHROPIC_API_KEY environment variable required"):
            LLMQuestionGenerator()
    
    @patch('game.llm_questions.LLM_AVAILABLE', True)
    @patch('game.llm_questions.load_dotenv')
    @patch('os.getenv')
    @patch('game.llm_questions.anthropic.Anthropic')
    def test_create_prompt(self, mock_anthropic, mock_getenv, mock_load_dotenv):
        """Test prompt creation for different complexity classes"""
        mock_getenv.side_effect = lambda key, default=None: {
            'ANTHROPIC_API_KEY': 'test_key',
            'CLAUDE_MODEL': 'claude-3-haiku-20240307'
        }.get(key, default)
        
        generator = LLMQuestionGenerator()
        
        # Test P class prompt
        prompt = generator._create_prompt('P', 2)
        assert 'P problems' in prompt
        assert 'polynomial time' in prompt
        
        # Test NP class prompt
        prompt = generator._create_prompt('NP', 3)
        assert 'NP problems' in prompt
        assert 'verified in polynomial time' in prompt
    
    @patch('game.llm_questions.LLM_AVAILABLE', True)
    @patch('game.llm_questions.load_dotenv')
    @patch('os.getenv')
    @patch('game.llm_questions.anthropic.Anthropic')
    def test_validate_question(self, mock_anthropic, mock_getenv, mock_load_dotenv):
        """Test question validation"""
        mock_getenv.side_effect = lambda key, default=None: {
            'ANTHROPIC_API_KEY': 'test_key',
            'CLAUDE_MODEL': 'claude-3-haiku-20240307'
        }.get(key, default)
        
        generator = LLMQuestionGenerator()
        
        # Test valid question
        valid_question = {
            'question': 'What is P?',
            'options': ['Option 1', 'Option 2', 'Option 3', 'Option 4'],
            'correct_answer': 'Option 1',
            'explanation': 'P is polynomial time',
            'complexity_class': 'P',
            'difficulty': 2
        }
        assert generator._validate_question(valid_question) is True
        
        # Test invalid question (missing field)
        invalid_question = {
            'question': 'What is P?',
            'options': ['Option 1', 'Option 2'],
            'correct_answer': 'Option 1'
        }
        assert generator._validate_question(invalid_question) is False
    
    @patch('game.llm_questions.LLM_AVAILABLE', True)
    @patch('game.llm_questions.load_dotenv')
    @patch('os.getenv')
    @patch('game.llm_questions.anthropic.Anthropic')
    def test_clean_json_response(self, mock_anthropic, mock_getenv, mock_load_dotenv):
        """Test JSON response cleaning"""
        mock_getenv.side_effect = lambda key, default=None: {
            'ANTHROPIC_API_KEY': 'test_key',
            'CLAUDE_MODEL': 'claude-3-haiku-20240307'
        }.get(key, default)
        
        generator = LLMQuestionGenerator()
        
        # Test cleaning JSON with markdown
        dirty_json = '```json\n{"key": "value"}\n```'
        clean_json = generator._clean_json_response(dirty_json)
        assert clean_json == '{"key": "value"}'
        
        # Test cleaning JSON with extra text
        dirty_json = 'Here is the JSON: {"key": "value"} End of response'
        clean_json = generator._clean_json_response(dirty_json)
        assert '{"key": "value"}' in clean_json


class TestLLMQuestionBank:
    @patch('builtins.open', new_callable=mock_open, read_data='{}')
    @patch('os.path.exists', return_value=True)
    def test_init_existing_cache(self, mock_exists, mock_file):
        """Test LLMQuestionBank initialization with existing cache"""
        bank = LLMQuestionBank()
        
        assert bank.cache_file == 'llm_questions_cache.json'
        assert bank.cache == {}
        mock_file.assert_called_once()
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    def test_init_no_cache(self, mock_exists, mock_file):
        """Test LLMQuestionBank initialization without cache file"""
        bank = LLMQuestionBank()
        
        assert bank.cache == {}
        mock_file.assert_not_called()
    
    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    @patch('os.path.exists', return_value=True)
    def test_init_invalid_cache(self, mock_exists, mock_file):
        """Test LLMQuestionBank initialization with invalid cache file"""
        bank = LLMQuestionBank()
        
        assert bank.cache == {}
    
    @patch('game.llm_questions.LLM_AVAILABLE', True)
    @patch('game.llm_questions.LLMQuestionGenerator')
    def test_is_available_with_generator(self, mock_generator_class):
        """Test is_available with working generator"""
        mock_generator_class.return_value = MagicMock()
        bank = LLMQuestionBank()
        
        assert bank.is_available() is True
        assert bank.generator is not None
    
    @patch('game.llm_questions.LLM_AVAILABLE', False)
    def test_is_available_no_llm(self):
        """Test is_available without LLM packages"""
        bank = LLMQuestionBank()
        
        assert bank.is_available() is False
        assert bank.generator is None
    
    @patch('builtins.open', new_callable=mock_open, read_data='{"P_2": [{"question": "test"}]}')
    @patch('os.path.exists', return_value=True)
    def test_get_question_from_cache(self, mock_exists, mock_file):
        """Test getting question from cache"""
        bank = LLMQuestionBank()
        
        # Mock the cache to have a question
        bank.cache = {
            'P_2': [LLMQuestion(
                question="What is P?",
                options=["Option 1", "Option 2", "Option 3", "Option 4"],
                correct_answer="Option 1",
                explanation="P is polynomial time",
                complexity_class="P",
                difficulty=2
            )]
        }
        
        question = bank.get_question('P', 2)
        assert question is not None
        assert question.question == "What is P?"
    
    @patch('builtins.open', new_callable=mock_open, read_data='{}')
    @patch('os.path.exists', return_value=True)
    def test_get_question_no_cache_no_generator(self, mock_exists, mock_file):
        """Test getting question without cache and without generator"""
        bank = LLMQuestionBank()
        bank.generator = None
        
        question = bank.get_question('P', 2)
        assert question is None
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    def test_save_cache(self, mock_exists, mock_file):
        """Test saving cache to file"""
        bank = LLMQuestionBank()
        bank.cache = {'test': 'data'}
        
        bank._save_cache()
        
        mock_file.assert_called_with('llm_questions_cache.json', 'w')
        handle = mock_file()
        handle.write.assert_called()