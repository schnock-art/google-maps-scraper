@echo off
setlocal enabledelayedexpansion

REM The name of the original and temporary files
set "ENV_FILE=environment.yml"
set "TEMP_FILE=temp_env.yml"
set "EXCLUDE_FILE=utilities\excluded_libraries.txt"

REM Copy original environment file to a temporary one
copy /Y "%ENV_FILE%" "%TEMP_FILE%"

REM Iterate over each line in the exclude file
for /F "tokens=*" %%i in (%EXCLUDE_FILE%) do (
    REM Use findstr to filter out the matching lines and update the temporary file
    findstr /v /c:"%%i" "%TEMP_FILE%" > "%TEMP_FILE%.new"
    move /Y "%TEMP_FILE%.new" "%TEMP_FILE%"
)

REM Create a new env file without the filtered libraries
set "ENV_FILE=environment_filtered.yml"
move /Y "%TEMP_FILE%" "%ENV_FILE%"
