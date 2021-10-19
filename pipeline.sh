yapf -i tinySSG.py
yapf -i test_all.py
mypy tinySSG.py
py.test -v --cov
