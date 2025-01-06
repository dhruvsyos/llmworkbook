#!/bin/bash

# Define the directory to check
TARGET_DIR=$1

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RESET='\033[0m'

# Initialize error tracking variables
RUFF_STATUS=0
PYLINT_STATUS=0
BLACK_STATUS=0
PIPAUDIT_STATUS=0

# Function for separators
print_separator() {
  echo -e "${YELLOW}\n=========================================================================${RESET}"
}

# Check if directory is provided
if [ -z "$TARGET_DIR" ]; then
  echo -e "${RED}Usage: $0 <directory>${RESET}"
  exit 1
fi

# Check if the directory exists
if [ ! -d "$TARGET_DIR" ]; then
  echo -e "${RED}Error: Directory '$TARGET_DIR' does not exist.${RESET}"
  exit 1
fi

# Run Ruff
print_separator
echo -e "${CYAN}Running Ruff...${RESET}"
ruff "$TARGET_DIR"
if [ $? -ne 0 ]; then
  RUFF_STATUS=1
  echo -e "${RED}Ruff found issues.${RESET}"
else
  echo -e "${GREEN}Ruff passed with no issues.${RESET}"
fi

# Run Black in check mode
print_separator
echo -e "${CYAN}Running Black for code formatting (check only)...${RESET}"
black --check "$TARGET_DIR"
if [ $? -ne 0 ]; then
  BLACK_STATUS=1
  echo -e "${RED}Black found formatting issues.${RESET}"
else
  echo -e "${GREEN}Black passed with no issues.${RESET}"
fi

# Run Pylint
print_separator
echo -e "${CYAN}Running Pylint on Python files in '$TARGET_DIR'...${RESET}"
pylint "$TARGET_DIR"/**/*.py > pylint_report.txt
if [ $? -ne 0 ]; then
  PYLINT_STATUS=1
  echo -e "${RED}Pylint encountered errors. Check pylint_report.txt.${RESET}"
else
  echo -e "${GREEN}Pylint completed successfully. Report saved to pylint_report.txt.${RESET}"
fi

# Run PIP audit
print_separator
echo -e "${CYAN}Running PIP AUDIT to check of any issues...${RESET}"
pip_audit
if [ $? -ne 0 ]; then
  PIPAUDIT_STATUS=1
  echo -e "${RED}PIP Audit found package issues.${RESET}"
else
  echo -e "${GREEN}PIP Audit passed with no issues.${RESET}"
fi

# Summary Report
print_separator
echo -e "${CYAN}Summary of Tool Results:${RESET}"
if [ $RUFF_STATUS -ne 0 ]; then
  echo -e "${RED}- Ruff: Issues found${RESET}"
else
  echo -e "${GREEN}- Ruff: No issues${RESET}"
fi

if [ $BLACK_STATUS -ne 0 ]; then
  echo -e "${RED}- Black: Formatting issues found${RESET}"
else
  echo -e "${GREEN}- Black: No formatting issues${RESET}"
fi

if [ $PYLINT_STATUS -ne 0 ]; then
  echo -e "${RED}- Pylint: Errors found (see pylint_report.txt)${RESET}"
else
  echo -e "${GREEN}- Pylint: No errors${RESET}"
fi

if [ $PIPAUDIT_STATUS -ne 0 ]; then
  echo -e "${RED}- PIP Audit: Package issues found${RESET}"
else
  echo -e "${GREEN}- PIP Audi: No Package issues${RESET}"
fi

# Determine exit status
if [ $RUFF_STATUS -ne 0 ] || [ $PYLINT_STATUS -ne 0 ] || [ $BLACK_STATUS -ne 0 ] || [ $PIPAUDIT_STATUS -ne 0 ]; then
  echo -e "${RED}\nSome tools reported issues. Please review the outputs above.${RESET}"
  exit 1  # Exit with non-zero status
else
  echo -e "${GREEN}\nAll tools passed successfully. No issues found.${RESET}"
  exit 0  # Exit successfully
fi

