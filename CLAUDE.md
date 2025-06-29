# Claude AI Integration

This project integrates with Claude AI (Anthropic) to generate dynamic questions and detailed explanations for complexity theory learning.

## Features

### AI Question Generation

- **Dynamic Questions**: Generates fresh questions for P, NP, NP-Complete, and NP-Hard problems
- **Conceptual Questions**: Creates broader complexity theory questions
- **Quality Validation**: Automatically validates questions for factual accuracy
- **Caching System**: Stores generated questions locally for performance

### Detailed Explanations

- **On-Demand**: Request detailed explanations after answering questions
- **Personalized**: Explanations adapt based on your specific answer
- **Educational Focus**: Provides deep understanding with examples and analogies
- **Misconception Correction**: Gently explains errors when answers are incorrect

### User Experience

- **Integrated Hints**: Access hints during questions with 'h' option
- **ASCII Visualizations**: Complexity class relationships and algorithm examples
- **Graceful Fallback**: Works without AI when not configured

## Setup Instructions

### 1. Install Dependencies

```bash
pip install anthropic python-dotenv
```

### 2. Configure API Key

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Anthropic API key
ANTHROPIC_API_KEY=your_api_key_here
```

### 3. Get API Key

Visit [Anthropic Console](https://console.anthropic.com/settings/keys) to create an API key.

### 4. Run the Game

```bash
python main.py
```

Select option "3. AI Question Mode" to use Claude-generated questions.

## Technical Details

### Architecture

- **LLMQuestionGenerator**: Core Claude API integration
- **LLMQuestionBank**: Question caching and management
- **Question Validation**: Fact-checking and quality assurance
- **Error Handling**: Robust retry logic and graceful degradation

### Files

- `game/llm_questions.py`: Main AI integration module
- `.env.example`: Environment configuration template
- `llm_questions_cache.json`: Local question cache

### Model Configuration

Default model: `claude-3-haiku-20240307`

To use a different model, set in `.env`:

```bash
CLAUDE_MODEL=claude-3-sonnet-20240229
```

### Quality Assurance

- **Fact-Checking Prompts**: Prevents common misconceptions
- **Answer Validation**: Ensures exactly one correct option
- **JSON Cleaning**: Handles response formatting issues
- **Retry Logic**: Handles API failures gracefully

## Usage Examples

### AI Question Mode

1. Select "3. AI Question Mode" from main menu
2. Choose complexity class (P, NP, NP-Complete, NP-Hard, or Conceptual)
3. Answer 3 generated questions per session
4. Request detailed explanations when needed

### Integration with Existing Features

- AI questions work alongside static tutorial questions
- Hint system ('h' option) works for all question types
- Scoring and statistics track all question types

## Cost Considerations

- Uses Claude Haiku model for cost efficiency
- Question caching reduces API calls
- Detailed explanations use slightly more tokens (1500 vs 1000)
- Typical session: ~10-15 API calls for 3 questions + explanations

## Troubleshooting

### "LLM features disabled"

- Check API key in `.env` file
- Verify `anthropic` package is installed
- Ensure internet connection for API access

### JSON parsing errors

- Automatically handled with response cleaning
- Retries with improved prompts
- Falls back gracefully on repeated failures

### Question quality issues

- Validation system catches common errors
- Fact-checking prompts improve accuracy
- Report issues for continuous improvement

## Development Notes

### Adding New Complexity Classes

1. Add examples to `_create_prompt()` method
2. Add fact-checking rules to `_validate_question()`
3. Update UI menus and mappings

### Improving Question Quality

1. Enhance fact-checking prompts in `_create_prompt()`
2. Add validation rules in `_validate_question()`
3. Adjust system prompts for better accuracy

### Performance Optimization

- Question caching reduces repeated API calls
- Batch generation (3 questions cached per request)
- Local storage prevents re-generation of same questions

## API Usage

The integration uses Anthropic's Claude API with:

- **System Prompts**: Expert complexity theory persona
- **Temperature**: 0.7 for questions, 0.3 for explanations  
- **Max Tokens**: 1000 for questions, 1500 for detailed explanations
- **Model**: claude-3-haiku-20240307 (configurable)

This ensures educational accuracy while maintaining creativity in question generation.
