# Exports environment to requirements.txt
export-conda-env:
	conda env export --no-build	> environment.yml
	utilities\filter_env.bat
	pip freeze > requirements.txt

# Installs requirements.txt
install-requirements:
	pip install -r requirements.txt

create-conda-env:
	conda env create -f environment.yml

export-folder-structure:
	python utilities/folder_structure.py

prepare-commit:
	make export-conda-env
	make export-folder-structure
#	black .
	isort .
#	flake8 . --ignore=E402 || exit /b 0
	utilities\pylint.bat
#	utilities\pytest.bat
	git add *
