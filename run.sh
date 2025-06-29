#!/bin/bash

# Script to set up Python environment and run the complexity theory game

set -e  # Exit on any error

echo "Setting up Python environment..."

# Check if pyenv is available and set Python version
if command -v pyenv &> /dev/null; then
    echo "Using pyenv to set Python version to 3.11..."
    pyenv local 3.11
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -e .

# Check if .env file exists, if not copy from example
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "Copying .env.example to .env..."
        cp .env.example .env
        echo "Please edit .env file to add your ANTHROPIC_API_KEY"
    else
        echo "Creating .env file..."
        cat > .env << 'EOF'
# Add your Anthropic API key here
ANTHROPIC_API_KEY=your_api_key_here

# Optional: Specify Claude model (default: claude-3-haiku-20240307)
# CLAUDE_MODEL=claude-3-sonnet-20240229
EOF
        echo "Please edit .env file to add your ANTHROPIC_API_KEY"
    fi
fi

echo "Setup complete!"
echo "Running the complexity theory game..."
echo ""

# Run the main program
python main.py