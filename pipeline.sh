yapf -i tinySSG.py
yapf -i test_all.py
mypy tinySSG.py
py.test --cov-report term-missing --cov=. -v
