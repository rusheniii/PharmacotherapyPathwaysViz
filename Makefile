
all:
	python pharmaPaths.py | jgraph > graph1.eps
	ps2pdf graph1.eps graph1.pdf
	python pharmaPaths.py | jgraph > graph2.eps
	ps2pdf graph2.eps graph2.pdf
	python pharmaPaths.py | jgraph > graph3.eps
	ps2pdf graph3.eps graph3.pdf
	python pharmaPaths.py | jgraph > graph4.eps
	ps2pdf graph4.eps graph4.pdf
	python pharmaPaths.py | jgraph > graph5.eps
	ps2pdf graph5.eps graph5.pdf
