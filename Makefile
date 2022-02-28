all:
	importchecker tinySSG.py
	yapf -i tinySSG.py
	mypy tinySSG.py
	#py.test --cov-report term-missing --cov=. -v

testfile:
	python3 tinySSG.py --file someinputfile.prehtml someinputfile.html

testfolder:
	python3 tinySSG.py --folder ./folder1 prehtml html


go: all testfile testfolder


