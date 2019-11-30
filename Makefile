.PHONY: install-dev-env
install-dev-env:
	pip3.5 install -e .
	pip3.5 install -r requirements-dev.txt
	pip3.5 install -r requirements.txt

.PHONY: create-dev-env
create-dev-env:
	pyenv virtualenv 3.5.4 qsm

.PHONY: activate-dev-env
activate-dev-env:
	pyenv activate qsm