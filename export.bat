@echo off
echo Exporting dependencies to requirements.txt
poetry export -E production -f requirements.txt > requirements.txt
echo Export completed.
