@echo off
pylint *.py **/*.py > utilities/results/pylint-results.txt
type utilities\results\pylint-results.txt
