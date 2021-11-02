coverage run --parallel --include='./*' --omit="manage.py,BizzVest/*,venv/**" manage.py test
coverage combine
coverage report -m
