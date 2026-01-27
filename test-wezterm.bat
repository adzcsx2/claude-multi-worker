@echo off
echo Testing WezTerm and Claude setup...
echo.

echo 1. WezTerm location:
where wezterm.exe
echo.

echo 2. Claude location:
where claude.exe
echo.

echo 3. Testing Claude directly...
claude.exe --version
echo.

echo 4. Testing WezTerm CLI...
wezterm.exe cli --help
echo.

pause
