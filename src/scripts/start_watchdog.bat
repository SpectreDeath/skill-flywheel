@echo off
REM Self-Healing Watchdog Startup Script for Windows
REM This script helps start and manage the MCP infrastructure watchdog

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "WATCHDOG_SCRIPT=%SCRIPT_DIR%watchdog_monitor.py"
set "TEST_SCRIPT=%SCRIPT_DIR%test_watchdog.py"
set "LOG_FILE=%SCRIPT_DIR%flywheel_events.log"
set "WATCHDOG_LOG=%SCRIPT_DIR%watchdog_monitor.log"

echo ========================================
echo   MCP Infrastructure Self-Healing Watchdog
echo ========================================
echo.

REM Check command line arguments
if "%1"=="" goto help
if "%1"=="start" goto start
if "%1"=="test" goto test
if "%1"=="status" goto status
if "%1"=="logs" goto logs
if "%1"=="clean-logs" goto clean
if "%1"=="help" goto help

:start
echo Starting MCP Infrastructure Self-Healing Watchdog...
echo Log file: %LOG_FILE%
echo Watchdog log: %WATCHDOG_LOG%
echo.
echo Press Ctrl+C to stop the watchdog
echo ----------------------------------------
python "%WATCHDOG_SCRIPT%"
goto end

:test
echo Running Self-Healing Watchdog Test Suite...
echo ----------------------------------------
python "%TEST_SCRIPT%"
goto end

:status
echo Checking MCP Infrastructure Status...
echo ----------------------------------------
REM Check if watchdog is running
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe" >NUL
if "%ERRORLEVEL%"=="0" (
    echo ✓ Watchdog is running
) else (
    echo ⚠ Watchdog is not running
)

echo.
echo Log Files Status:
if exist "%LOG_FILE%" (
    for %%A in ("%LOG_FILE%") do set /A event_count=%%~zA
    echo ✓ %LOG_FILE% (exists)
) else (
    echo ✗ %LOG_FILE% (not found)
)

if exist "%WATCHDOG_LOG%" (
    echo ✓ %WATCHDOG_LOG% (exists)
) else (
    echo ✗ %WATCHDOG_LOG% (not found)
)
goto end

:logs
echo Recent Watchdog Events:
echo ----------------------------------------
if exist "%LOG_FILE%" (
    echo Last 10 events from %LOG_FILE%:
    for /f "skip=1 tokens=*" %%a in ('type "%LOG_FILE%" ^| tail -10') do (
        echo %%a
    )
) else (
    echo No log file found. Start the watchdog to generate events.
)
goto end

:clean
echo Cleaning up log files...
echo ----------------------------------------
if exist "%LOG_FILE%" (
    set "backup_file=%LOG_FILE%.backup.%date:~-4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
    set "backup_file=!backup_file: =0!"
    echo Backing up %LOG_FILE% to !backup_file!
    copy "%LOG_FILE%" "!backup_file!" >nul
    echo ✓ Backup created
)

echo Clearing log files...
echo. > "%LOG_FILE%"
echo. > "%WATCHDOG_LOG%"
echo ✓ Log files cleaned
echo Note: Old logs are backed up with timestamp
goto end

:help
echo Usage: %0 [COMMAND] [OPTIONS]
echo.
echo Commands:
echo   start           Start the watchdog monitor
echo   test            Run the test suite
echo   status          Check watchdog and service status
echo   logs            Show recent log entries
echo   clean-logs      Clean up old log files
echo   help            Show this help message
echo.
echo Examples:
echo   %0 start        Start the watchdog
echo   %0 test         Run tests
echo   %0 logs         View recent events
goto end

:end
endlocal