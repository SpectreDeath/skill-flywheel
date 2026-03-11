#!/bin/bash

# Self-Healing Watchdog Startup Script
# This script helps start and manage the MCP infrastructure watchdog

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WATCHDOG_SCRIPT="$SCRIPT_DIR/watchdog_monitor.py"
TEST_SCRIPT="$SCRIPT_DIR/test_watchdog.py"
LOG_FILE="$SCRIPT_DIR/flywheel_events.log"
WATCHDOG_LOG="$SCRIPT_DIR/watchdog_monitor.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  MCP Infrastructure Self-Healing Watchdog${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo
}

print_usage() {
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo
    echo "Commands:"
    echo "  start           Start the watchdog monitor"
    echo "  test            Run the test suite"
    echo "  status          Check watchdog and service status"
    echo "  logs            Show recent log entries"
    echo "  clean-logs      Clean up old log files"
    echo "  help            Show this help message"
    echo
    echo "Examples:"
    echo "  $0 start        # Start the watchdog"
    echo "  $0 test         # Run tests"
    echo "  $0 logs         # View recent events"
    echo
}

check_prerequisites() {
    # Check if Python is available
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}Error: Python 3 is required but not installed${NC}"
        exit 1
    fi
    
    # Check if watchdog script exists
    if [ ! -f "$WATCHDOG_SCRIPT" ]; then
        echo -e "${RED}Error: watchdog_monitor.py not found in $SCRIPT_DIR${NC}"
        exit 1
    fi
    
    # Check if requests module is available
    if ! python3 -c "import requests" 2>/dev/null; then
        echo -e "${YELLOW}Warning: requests module not found. Installing...${NC}"
        pip3 install requests
    fi
}

start_watchdog() {
    print_header
    echo "Starting MCP Infrastructure Self-Healing Watchdog..."
    echo "Log file: $LOG_FILE"
    echo "Watchdog log: $WATCHDOG_LOG"
    echo
    echo "Press Ctrl+C to stop the watchdog"
    echo "----------------------------------------"
    
    # Start the watchdog
    python3 "$WATCHDOG_SCRIPT"
}

run_tests() {
    print_header
    echo "Running Self-Healing Watchdog Test Suite..."
    echo "----------------------------------------"
    
    # Run the test script
    python3 "$TEST_SCRIPT"
}

check_status() {
    print_header
    echo "Checking MCP Infrastructure Status..."
    echo "----------------------------------------"
    
    # Check if watchdog is running
    if pgrep -f "watchdog_monitor.py" > /dev/null; then
        echo -e "${GREEN}✓ Watchdog is running${NC}"
    else
        echo -e "${YELLOW}⚠ Watchdog is not running${NC}"
    fi
    
    # Check Docker services
    echo
    echo "Docker Services Status:"
    if command -v docker &> /dev/null; then
        docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "(mcp-|watchdog)" || echo "No MCP services found"
    else
        echo "Docker not available"
    fi
    
    # Check log files
    echo
    echo "Log Files Status:"
    if [ -f "$LOG_FILE" ]; then
        event_count=$(wc -l < "$LOG_FILE")
        echo "✓ $LOG_FILE ($event_count events)"
    else
        echo "✗ $LOG_FILE (not found)"
    fi
    
    if [ -f "$WATCHDOG_LOG" ]; then
        echo "✓ $WATCHDOG_LOG"
    else
        echo "✗ $WATCHDOG_LOG (not found)"
    fi
}

show_logs() {
    print_header
    echo "Recent Watchdog Events:"
    echo "----------------------------------------"
    
    if [ -f "$LOG_FILE" ]; then
        echo "Last 10 events from $LOG_FILE:"
        tail -10 "$LOG_FILE" | while IFS= read -r line; do
            if command -v jq &> /dev/null; then
                echo "$line" | jq -r '"\(.timestamp) | \(.event_type) | \(.failed_services // [] | map(.service) | join(", "))"'
            else
                echo "$line"
            fi
        done
    else
        echo "No log file found. Start the watchdog to generate events."
    fi
    
    echo
    if [ -f "$WATCHDOG_LOG" ]; then
        echo "Recent watchdog monitor log entries:"
        tail -5 "$WATCHDOG_LOG"
    fi
}

clean_logs() {
    print_header
    echo "Cleaning up log files..."
    echo "----------------------------------------"
    
    if [ -f "$LOG_FILE" ]; then
        backup_file="${LOG_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
        echo "Backing up $LOG_FILE to $backup_file"
        cp "$LOG_FILE" "$backup_file"
        echo "✓ Backup created"
    fi
    
    # Clear log files
    > "$LOG_FILE"
    > "$WATCHDOG_LOG"
    
    echo "✓ Log files cleaned"
    echo "Note: Old logs are backed up with timestamp"
}

# Main script logic
main() {
    case "${1:-help}" in
        "start")
            check_prerequisites
            start_watchdog
            ;;
        "test")
            check_prerequisites
            run_tests
            ;;
        "status")
            check_status
            ;;
        "logs")
            show_logs
            ;;
        "clean-logs")
            clean_logs
            ;;
        "help"|*)
            print_usage
            ;;
    esac
}

# Run main function with all arguments
main "$@"