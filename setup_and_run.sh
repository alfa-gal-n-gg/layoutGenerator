#!/bin/bash

# Define colors for the rainbow banner
RED='\033[0;31m'
ORANGE='\033[0;33m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Function to print the rainbow banner
print_banner() {
    echo -e "${RED}G${ORANGE}A${YELLOW}L ${GREEN}T${CYAN}O${BLUE}P ${MAGENTA}G${NC}"
    echo -e "----------------------------------------------------------------------"
    echo -e "${RED}G${ORANGE}A${YELLOW}L ${GREEN}T${CYAN}O${BLUE}P ${MAGENTA}G${NC}"
}

# Print the banner
print_banner

# Define the virtual environment directory
VENV_DIR=".venv"

# Function to install packages with the correct pip command
install_packages() {
    if command -v pip &> /dev/null; then
        echo -e "${CYAN}Installing packages with pip...${NC}"
        pip install -r requirements.txt
    elif command -v pip3 &> /dev/null; then
        echo -e "${CYAN}pip not found, using pip3...${NC}"
        pip3 install -r requirements.txt
    else
        echo -e "${RED}pip is not installed. Please install pip or pip3 and try again.${NC}"
        exit 1
    fi
}

# Check if the virtual environment already exists
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${CYAN}Creating virtual environment...${NC}"
    if command -v python3 &> /dev/null; then
        python3 -m venv $VENV_DIR
    elif command -v python &> /dev/null; then
        python -m venv $VENV_DIR
    else
        echo -e "${RED}Python is not installed. Please install Python and try again.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}Virtual environment already exists. Skipping creation.${NC}"
fi

# Activate the virtual environment
echo -e "${CYAN}Activating virtual environment...${NC}"
source $VENV_DIR/bin/activate

# Install required packages
echo -e "${CYAN}Installing required packages...${NC}"
install_packages

# Run the Streamlit app
echo -e "${CYAN}Running Streamlit app...${NC}"
streamlit run app.py

# Deactivate the virtual environment after exiting Streamlit
deactivate
