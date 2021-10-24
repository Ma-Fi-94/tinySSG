yapf -i tinySSG.py
yapf -i test_log.py
yapf -i test_tinySSG.py
mypy tinySSG.py
mypy test_log.py
mypy test_tinySSG.py
py.test --cov-report term-missing --cov=. -v
