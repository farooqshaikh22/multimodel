#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Setting up Compliance Agent Project...${NC}"

# Create project directory structure
echo "Creating directory structure..."
mkdir -p compliance-agent/src/agents
mkdir -p compliance-agent/src/utils
mkdir -p compliance-agent/data/transcripts
mkdir -p compliance-agent/data/rules
mkdir -p compliance-agent/config
mkdir -p compliance-agent/logs

# Create virtual environment
echo "Creating Python virtual environment..."
python -m venv venv
source venv/bin/activate

# Install requirements
echo "Installing required packages..."
pip install -r requirements.txt

# Create .env file for API keys
echo "Creating .env file..."
cat > compliance-agent/.env << EOL
GROQ_API_KEY=your-groq-api-key-here
EOL

# Make logs directory writable
chmod 755 compliance-agent/logs

echo -e "${GREEN}Setup completed successfully!${NC}"
echo -e "${BLUE}To get started:${NC}"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Add your Groq API key to compliance-agent/.env"
echo "3. Run the compliance checker with: python run.py" 