PYTHON = python3
PIP = pip3

DEPENDENCIES =	pygame\
				pygame-menu\
				pyyaml\


.PHONY = run, install_dependencies
.DEFAULT_GOAL = install_dependencies

# test:
# 	${PYTHON} -m pytest
	
run:
	${PYTHON} main.py

install_dependencies:
	${PIP} install ${DEPENDENCIES}
