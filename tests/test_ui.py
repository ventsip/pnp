import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from io import StringIO

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.ui import GameUI
from problems.base import Problem


class MockProblem(Problem):
    def __init__(self):
        super().__init__()
        self.question = "Test question"
        self.options = ["Option 1", "Option 2", "Option 3", "Option 4"]
        self.correct_answer = "Option 1"
        self.explanation = "Test explanation"
        self.complexity_class = "P"
        self.difficulty = 1
        self.problem_type = "classification"
    
    def check_classification(self, answer):
        return answer == self.correct_answer


class TestGameUI:
    def test_init(self):
        """Test GameUI initialization"""
        ui = GameUI()
        
        assert len(ui.complexity_descriptions) == 4
        assert 'P' in ui.complexity_descriptions
        assert 'NP' in ui.complexity_descriptions
        assert 'NP-Complete' in ui.complexity_descriptions
        assert 'NP-Hard' in ui.complexity_descriptions
    
    @patch('os.system')
    def test_clear_screen_unix(self, mock_system):
        """Test clear screen on Unix systems"""
        ui = GameUI()
        
        with patch('os.name', 'posix'):
            ui.clear_screen()
            mock_system.assert_called_with('clear')
    
    @patch('os.system')
    def test_clear_screen_windows(self, mock_system):
        """Test clear screen on Windows systems"""
        ui = GameUI()
        
        with patch('os.name', 'nt'):
            ui.clear_screen()
            mock_system.assert_called_with('cls')
    
    @patch('sys.stdout', new_callable=StringIO)
    @patch('game.ui.GameUI.clear_screen')
    def test_show_welcome(self, mock_clear, mock_stdout):
        """Test welcome message display"""
        ui = GameUI()
        ui.show_welcome()
        
        mock_clear.assert_called_once()
        output = mock_stdout.getvalue()
        assert "COMPLEXITY THEORY LEARNING GAME" in output
        assert "Welcome" in output
    
    @patch('builtins.input', return_value='1')
    @patch('sys.stdout', new_callable=StringIO)
    def test_show_main_menu(self, mock_stdout, mock_input):
        """Test main menu display and input"""
        ui = GameUI()
        choice = ui.show_main_menu()
        
        assert choice == '1'
        output = mock_stdout.getvalue()
        assert "MAIN MENU" in output
        assert "Tutorial Mode" in output
        assert "Challenge Mode" in output
        assert "AI Question Mode" in output
    
    @patch('builtins.input', return_value='2')
    @patch('sys.stdout', new_callable=StringIO)
    def test_show_ai_mode_menu(self, mock_stdout, mock_input):
        """Test AI mode menu display and input"""
        ui = GameUI()
        choice = ui.show_ai_mode_menu()
        
        assert choice == '2'
        output = mock_stdout.getvalue()
        assert "AI QUESTION MODE" in output
        assert "P Problems" in output
        assert "NP Problems" in output
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_show_complexity_intro(self, mock_stdout):
        """Test complexity class introduction display"""
        ui = GameUI()
        ui.show_complexity_intro('P')
        
        output = mock_stdout.getvalue()
        assert "P (Polynomial Time) Problems" in output
        assert "polynomial time" in output
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_show_problem(self, mock_stdout):
        """Test problem display"""
        ui = GameUI()
        problem = MockProblem()
        ui.show_problem(problem)
        
        output = mock_stdout.getvalue()
        assert "Test question" in output
        assert "Option 1" in output
        assert "Option 2" in output
    
    @patch('builtins.input', return_value='1')
    def test_get_classification_answer(self, mock_input):
        """Test getting classification answer"""
        ui = GameUI()
        answer = ui.get_classification_answer()
        
        assert answer is not None
    
    @patch('builtins.input', return_value='yes')
    def test_get_decision_answer(self, mock_input):
        """Test getting decision answer"""
        ui = GameUI()
        answer = ui.get_decision_answer()
        
        assert answer == 'yes'
    
    @patch('builtins.input', return_value='100')
    def test_get_optimization_answer(self, mock_input):
        """Test getting optimization answer"""
        ui = GameUI()
        answer = ui.get_optimization_answer()
        
        assert answer == 100
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_show_result_correct(self, mock_stdout):
        """Test showing correct result"""
        ui = GameUI()
        ui.show_result(True, "Great job!")
        
        output = mock_stdout.getvalue()
        assert "Correct!" in output
        assert "Great job!" in output
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_show_result_incorrect(self, mock_stdout):
        """Test showing incorrect result"""
        ui = GameUI()
        ui.show_result(False, "Try again!")
        
        output = mock_stdout.getvalue()
        assert "Incorrect!" in output
        assert "Try again!" in output
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_show_final_score(self, mock_stdout):
        """Test showing final score"""
        ui = GameUI()
        ui.show_final_score(1500)
        
        output = mock_stdout.getvalue()
        assert "FINAL SCORE" in output
        assert "1500" in output
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_show_scores(self, mock_stdout):
        """Test showing statistics"""
        ui = GameUI()
        stats = {
            'total_score': 1000,
            'problems_solved': 5,
            'problems_attempted': 8,
            'overall_accuracy': 62.5
        }
        ui.show_scores(stats)
        
        output = mock_stdout.getvalue()
        assert "STATISTICS" in output
        assert "1000" in output
        assert "62.5%" in output
    
    @patch('builtins.input', return_value='1')
    def test_get_llm_answer(self, mock_input):
        """Test getting LLM answer"""
        ui = GameUI()
        answer = ui.get_llm_answer(4)
        
        assert answer == 0  # Should return 0-based index
    
    @patch('builtins.input', return_value='n')
    @patch('sys.stdout', new_callable=StringIO)
    def test_show_llm_result(self, mock_stdout, mock_input):
        """Test showing LLM result"""
        ui = GameUI()
        mock_question = MagicMock()
        mock_question.explanation = "Test explanation"
        
        result = ui.show_llm_result(True, mock_question, "Option 1")
        
        assert result == 'continue'
        output = mock_stdout.getvalue()
        assert "Correct!" in output