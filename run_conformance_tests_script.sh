#!/bin/bash

UNRECOVERABLE_ERROR_EXIT_CODE=69

# Check if source folder name is provided
if [ -z "$1" ]; then
  printf "Error: No source folder name provided.\n"
  printf "Usage: $0 <source_folder_name> <conformance_tests_folder>\n"
  exit $UNRECOVERABLE_ERROR_EXIT_CODE
fi

# Check if conformance tests folder name is provided
if [ -z "$2" ]; then
  printf "Error: No conformance tests folder name provided.\n"
  printf "Usage: $0 <source_folder_name> <conformance_tests_folder>\n"
  exit $UNRECOVERABLE_ERROR_EXIT_CODE
fi

current_dir=$(pwd)
SOURCE_FOLDER=$1
CONFORMANCE_TESTS_DIR=$2
BUILD_SUBFOLDER=".tmp/$SOURCE_FOLDER"

echo "Current directory: $current_dir"
echo "Source folder: $SOURCE_FOLDER"
echo "Conformance tests: $CONFORMANCE_TESTS_DIR"
echo "--------------------------------"

# Prepare clean build subfolder
if [ -d "$BUILD_SUBFOLDER" ]; then
  rm -rf "$BUILD_SUBFOLDER"
fi
mkdir -p "$BUILD_SUBFOLDER"

# Copy source code to build folder
echo "Copying source code from: $SOURCE_FOLDER to: $BUILD_SUBFOLDER"
cp -R $SOURCE_FOLDER/* "$BUILD_SUBFOLDER/"

echo "Moving to the subfolder: $BUILD_SUBFOLDER"
cd "$BUILD_SUBFOLDER" || exit $UNRECOVERABLE_ERROR_EXIT_CODE

printf "Setting up Python environment for conformance testing...\n"

# Create and activate virtual environment
echo "Creating and activating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install requirements
if [ -f "requirements.txt" ]; then
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "Warning: requirements.txt not found."
fi

# Execute all Python conformance tests
# Note: We run tests from the absolute path of the conformance tests folder
printf "Running Conformance Tests...\n\n"

output=$(python3 -m unittest discover -v -s "$current_dir/$CONFORMANCE_TESTS_DIR" 2>&1)
exit_code=$?

# Echo the test output
echo "$output"

# Check if no tests were discovered
if echo "$output" | grep -q "Ran 0 tests in"; then
    printf "\nError: No conformance tests were discovered in $CONFORMANCE_TESTS_DIR.\n"
    exit 1
fi

# Deactivate venv
deactivate

# Return the exit code of the unittest command
exit $exit_code