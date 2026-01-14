# Project settings
TARGET = Visualizer.py
SRC_DIR = .
BUILD_DIR = build
CACHE_DIR = __pycache__

# Source files (Wildcard mimics your C makefile structure)
SRC = $(wildcard $(SRC_DIR)/*.py)

# Interpreter settings
PYTHON = python3
FLAGS = -B
# -B prevents writing .pyc files (keeps directory clean)

# Detect platform (Windows vs others)
ifeq ($(OS),Windows_NT)
    # Windows typically uses 'python', not 'python3'
    PYTHON = python
    # Windows-specific flags (if needed later)
    PLATFORM_MSG = "Detected Platform: Windows"
else
    # Linux/MacOS usually requires 'python3'
    PYTHON = python3
    PLATFORM_MSG = "Detected Platform: Linux/Unix"
endif

# Default target
all: run

# Run the application (Equivalent to linking/running in C)
run:
	@echo $(PLATFORM_MSG)
	@echo "Running $(TARGET)..."
	$(PYTHON) $(FLAGS) $(SRC_DIR)/$(TARGET)

# Check syntax (Equivalent to compiling .o files without linking)
check: $(SRC)
	@echo "Checking syntax..."
	$(PYTHON) -m py_compile $(SRC)
	@echo "Syntax OK."

# Clean build artifacts
clean:
	rm -rf $(CACHE_DIR)
	rm -rf $(BUILD_DIR)
	@echo "Cleaned all cache and build artifacts."

.PHONY: all run check clean
