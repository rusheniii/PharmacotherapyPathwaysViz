
all:
	python pharmaPaths.py | jgraph > graph1.eps
	python pharmaPaths.py | jgraph > graph2.eps
	python pharmaPaths.py | jgraph > graph3.eps
	python pharmaPaths.py | jgraph > graph4.eps
	python pharmaPaths.py | jgraph > graph5.eps
