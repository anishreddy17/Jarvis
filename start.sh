#!/bin/bash

# Quick Start Script for Jarvis AI Assistant
# This script helps you get started quickly

echo "=========================================="
echo "Jarvis AI Assistant - Quick Start"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo "✓ Python 3 is installed"

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama is not installed."
    echo "Please install Ollama from: https://ollama.com"
    echo ""
    echo "For Linux/macOS:"
    echo "curl -fsSL https://ollama.com/install.sh | sh"
    echo ""
    read -p "Press Enter after installing Ollama..."
fi

echo "✓ Ollama is installed"

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Ollama is not running."
    echo "Starting Ollama in the background..."
    ollama serve > /dev/null 2>&1 &
    sleep 3
fi

echo "✓ Ollama is running"

# Check if a model is installed
echo "Checking for available models..."
MODELS=$(ollama list 2>/dev/null | grep -v "NAME")

if [ -z "$MODELS" ]; then
    echo "⚠️  No models found. Pulling llama2..."
    ollama pull llama2
else
    echo "✓ Models available:"
    echo "$MODELS"
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip3 install -r requirements.txt > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed"
else
    echo "❌ Failed to install dependencies. Please run: pip3 install -r requirements.txt"
    exit 1
fi

# Check for .env file
if [ ! -f .env ]; then
    echo ""
    echo "⚠️  .env file not found."
    echo "Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit the .env file with your Pinecone credentials:"
    echo "   - PINECONE_API_KEY"
    echo "   - PINECONE_ENVIRONMENT"
    echo ""
    read -p "Press Enter after updating .env file..."
fi

# Run quick test
echo ""
echo "Running quick connectivity test..."
python3 setup_and_test.py quick

echo ""
echo "=========================================="
echo "Setup Complete! 🎉"
echo "=========================================="
echo ""
echo "To start using Jarvis:"
echo ""
echo "1. Terminal 1 - Start the API:"
echo "   python3 api.py"
echo ""
echo "2. Terminal 2 - Start the UI:"
echo "   streamlit run streamlit_app.py"
echo ""
echo "3. Open your browser at:"
echo "   http://localhost:8501"
echo ""
echo "=========================================="
