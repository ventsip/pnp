import pytest
import sys
import os
from unittest.mock import patch, MagicMock, mock_open
from io import StringIO

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import ComplexityGame
from game.llm_questions import LLMQuestion


class TestComplexityGameIntegration:
    """Integration tests for the main game flow"""
    
    @patch('builtins.input', side_effect=['6'])  # Exit immediately
    @patch('sys.stdout', new_callable=StringIO)
    def test_start_game_exit_immediately(self, mock_stdout, mock_input):
        """Test starting game and exiting immediately"""
        game = ComplexityGame()
        game.start_game()
        
        output = mock_stdout.getvalue()
        assert "COMPLEXITY THEORY LEARNING GAME" in output
        assert "MAIN MENU" in output
        assert "Thanks for playing" in output
    
    @patch('builtins.input', side_effect=['4', '6'])  # View theory then exit
    @patch('sys.stdout', new_callable=StringIO)
    def test_show_theory_flow(self, mock_stdout, mock_input):
        """Test showing theory section"""
        game = ComplexityGame()
        game.start_game()
        
        output = mock_stdout.getvalue()
        assert "COMPLEXITY THEORY" in output
    
    @patch('builtins.input', side_effect=['5', '6'])  # View scores then exit
    @patch('sys.stdout', new_callable=StringIO)
    def test_show_scores_flow(self, mock_stdout, mock_input):
        """Test showing scores section"""
        game = ComplexityGame()
        game.start_game()
        
        output = mock_stdout.getvalue()
        assert "STATISTICS" in output
    
    @patch('builtins.input', side_effect=['1'])  # Tutorial mode
    @patch('sys.stdout', new_callable=StringIO)
    @patch.object(ComplexityGame, 'solve_problem', return_value=True)
    def test_tutorial_mode_flow(self, mock_solve, mock_stdout, mock_input):
        """Test tutorial mode flow"""
        game = ComplexityGame()
        
        # Run just one complexity class to avoid long execution
        original_problem_sets = game.problem_sets
        game.problem_sets = {'P': original_problem_sets['P']}
        
        game.play_tutorial()
        
        # Should have called solve_problem for tutorial problems
        assert mock_solve.call_count >= 2  # At least 2 problems per class
        output = mock_stdout.getvalue()
        assert "P (Polynomial Time) Problems" in output
    
    @patch('builtins.input', side_effect=['P'])  # Classification answer
    @patch('sys.stdout', new_callable=StringIO)
    def test_solve_problem_classification(self, mock_stdout, mock_input):
        """Test solving classification problem"""
        game = ComplexityGame()
        
        # Create a mock problem
        problem = MagicMock()
        problem.problem_type = 'classification'
        problem.check_classification.return_value = True
        problem.get_explanation.return_value = "Test explanation"
        
        result = game.solve_problem(problem, is_tutorial=True)
        
        assert result is True
        problem.check_classification.assert_called_once_with('P')
        output = mock_stdout.getvalue()
        assert "Correct!" in output
    
    @patch('builtins.input', side_effect=['yes'])  # Decision answer
    @patch('sys.stdout', new_callable=StringIO)
    def test_solve_problem_decision(self, mock_stdout, mock_input):
        """Test solving decision problem"""
        game = ComplexityGame()
        
        # Create a mock problem
        problem = MagicMock()
        problem.problem_type = 'decision'
        problem.check_decision.return_value = False
        problem.get_explanation.return_value = "Test explanation"
        
        result = game.solve_problem(problem, is_tutorial=False)
        
        assert result is False
        problem.check_decision.assert_called_once_with('yes')
        output = mock_stdout.getvalue()
        assert "Incorrect!" in output
    
    @patch('builtins.input', side_effect=['100'])  # Optimization answer
    @patch('sys.stdout', new_callable=StringIO)
    def test_solve_problem_optimization(self, mock_stdout, mock_input):
        """Test solving optimization problem"""
        game = ComplexityGame()
        
        # Create a mock problem
        problem = MagicMock()
        problem.problem_type = 'optimization'
        problem.check_optimization.return_value = True
        problem.get_explanation.return_value = "Test explanation"
        
        result = game.solve_problem(problem, is_tutorial=True)
        
        assert result is True
        problem.check_optimization.assert_called_once_with(100)
    
    @patch('builtins.input', side_effect=['3', '6'])  # AI mode then back
    @patch('sys.stdout', new_callable=StringIO)
    def test_ai_mode_unavailable(self, mock_stdout, mock_input):
        """Test AI mode when LLM is unavailable"""
        game = ComplexityGame()
        game.llm_questions.generator = None  # Simulate unavailable LLM
        
        game.start_game()
        
        output = mock_stdout.getvalue()
        assert "LLM features are disabled" in output
    
    @patch('builtins.input', side_effect=['1', '1'])  # P problems, option 1
    @patch('sys.stdout', new_callable=StringIO)
    def test_solve_llm_question_correct(self, mock_stdout, mock_input):
        """Test solving LLM question correctly"""
        game = ComplexityGame()
        
        # Create a mock LLM question
        question = LLMQuestion(
            question="What is P?",
            options=["Polynomial time", "Non-polynomial", "Exponential", "Unknown"],
            correct_answer="Polynomial time",
            explanation="P stands for polynomial time",
            complexity_class="P",
            difficulty=2
        )
        
        with patch.object(game.ui, 'show_llm_result', return_value='continue'):
            game.solve_llm_question(question)
        
        assert game.problems_solved == 1
        output = mock_stdout.getvalue()
        assert "What is P?" in output
    
    @patch('builtins.input', side_effect=['2'])  # Wrong option
    @patch('sys.stdout', new_callable=StringIO)
    def test_solve_llm_question_incorrect(self, mock_stdout, mock_input):
        """Test solving LLM question incorrectly"""
        game = ComplexityGame()
        initial_solved = game.problems_solved
        
        # Create a mock LLM question
        question = LLMQuestion(
            question="What is P?",
            options=["Polynomial time", "Non-polynomial", "Exponential", "Unknown"],
            correct_answer="Polynomial time",
            explanation="P stands for polynomial time",
            complexity_class="P",
            difficulty=2
        )
        
        with patch.object(game.ui, 'show_llm_result', return_value='continue'):
            game.solve_llm_question(question)
        
        # Problems solved should not increase for incorrect answer
        assert game.problems_solved == initial_solved
    
    @patch('builtins.input', side_effect=['1'])  # Option 1
    @patch('sys.stdout', new_callable=StringIO)
    def test_solve_llm_question_with_detailed_explanation(self, mock_stdout, mock_input):
        """Test solving LLM question and requesting detailed explanation"""
        game = ComplexityGame()
        
        # Mock the generator for detailed explanation
        mock_generator = MagicMock()
        mock_generator.generate_detailed_explanation.return_value = "Detailed explanation here"
        game.llm_questions.generator = mock_generator
        
        question = LLMQuestion(
            question="What is P?",
            options=["Polynomial time", "Non-polynomial", "Exponential", "Unknown"],
            correct_answer="Polynomial time",
            explanation="P stands for polynomial time",
            complexity_class="P",
            difficulty=2
        )
        
        with patch.object(game.ui, 'show_llm_result', return_value='detailed'):
            with patch.object(game, 'show_detailed_explanation') as mock_show_detailed:
                game.solve_llm_question(question)
                mock_show_detailed.assert_called_once_with(question, "Polynomial time")
    
    def test_generate_question_with_retry_success(self):
        """Test successful question generation with retry"""
        game = ComplexityGame()
        
        # Mock successful question generation
        mock_question = LLMQuestion(
            question="Test question",
            options=["A", "B", "C", "D"],
            correct_answer="A",
            explanation="Test explanation",
            complexity_class="P",
            difficulty=2
        )
        
        with patch.object(game.llm_questions, 'get_question', return_value=mock_question):
            result = game._generate_question_with_retry('P')
            assert result == mock_question
    
    def test_generate_question_with_retry_failure(self):
        """Test failed question generation with retry"""
        game = ComplexityGame()
        
        with patch.object(game.llm_questions, 'get_question', side_effect=Exception("API Error")):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                result = game._generate_question_with_retry('P')
                assert result is None
                output = mock_stdout.getvalue()
                assert "Failed to generate question" in output
    
    @patch('builtins.input', side_effect=['1', '2', '3', '4', '5'])  # Different complexity classes
    @patch('sys.stdout', new_callable=StringIO)
    def test_ai_mode_complexity_class_mapping(self, mock_stdout, mock_input):
        """Test AI mode complexity class mapping"""
        game = ComplexityGame()
        
        # Test each mapping
        assert game.ai_mode_mapping['1'] == 'P'
        assert game.ai_mode_mapping['2'] == 'NP'
        assert game.ai_mode_mapping['3'] == 'NP-Complete'
        assert game.ai_mode_mapping['4'] == 'NP-Hard'
        assert game.ai_mode_mapping['5'] == 'Conceptual'
    
    def test_challenge_mode_scoring(self):
        """Test challenge mode scoring integration"""
        game = ComplexityGame()
        
        # Mock a problem and simulate solving it
        mock_problem = MagicMock()
        mock_problem.difficulty = 3
        
        with patch.object(game, 'solve_problem', return_value=True):
            with patch.object(game.problem_sets['P'], 'get_random_problem', return_value=mock_problem):
                with patch('time.time', side_effect=[0, 5]):  # 5 second solve time
                    # Simulate one round of challenge mode
                    complexity_class = 'P'
                    problem_set = game.problem_sets[complexity_class]
                    problem = problem_set.get_random_problem()
                    
                    start_time = 0
                    correct = game.solve_problem(problem, is_tutorial=False)
                    solve_time = 5
                    
                    if correct:
                        points = game.score_manager.calculate_points(
                            complexity_class, solve_time, problem.difficulty
                        )
                        game.score_manager.add_score(points)
                        game.problems_solved += 1
                    
                    assert game.score_manager.get_total_score() > 0
                    assert game.problems_solved == 1