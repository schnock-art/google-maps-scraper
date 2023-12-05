@echo off
pytest --cov-report term-missing --cov > utilities/results/pytest-results.txt
type utilities\results\pytest-results.txt
