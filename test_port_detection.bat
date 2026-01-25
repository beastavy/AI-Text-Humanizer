@echo off
echo Testing port detection logic...
echo.

set PORT=8501
set MAX_PORT=8520

:CHECK_PORT
netstat -an | findstr :%PORT% >nul
if %errorlevel% equ 0 (
    echo Port %PORT% is in use
    set /a PORT=%PORT%+1
    if %PORT% gtr %MAX_PORT% (
        echo ❌ No available ports found between 8501-8520
        goto END
    )
    goto CHECK_PORT
)

echo ✅ Found available port: %PORT%
echo.

:END
echo Port detection test completed successfully!
pause



