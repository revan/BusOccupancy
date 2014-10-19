BUS_STR = -58
PROB_STR = -85
END = 1940
BUS_TITLE = "April 7th, A Route"
PROB_TITLE = "April 7th, Lecture Hall"

all: bus class

bus: packets unique grid-bus segments vectors
class: grid-class packethist

packets: data/bus.json
	python3 graph.py -t packets data/bus.json -e $(END) -n $(BUS_TITLE) -l True\
	 -r True -s $(BUS_STR) -m True
unique: data/bus.json
	python3 graph.py -t unique data/bus.json -e $(END) -n $(BUS_TITLE) -l True\
	 -r True -s $(BUS_STR) -m True
grid-bus: data/bus.json
	python3 graph.py -t grid data/bus.json -e $(END) -n $(BUS_TITLE) -l True\
	 -r True -s $(BUS_STR) -m True
grid-class: data/class.json
	python3 graph.py -t grid data/class.json -n $(PROB_TITLE) -r True -m True
segments: data/bus.json
	python3 graph.py -t segments data/bus.json -e $(END) -n $(BUS_TITLE) -l True\
	 -r True -m True
vectors: data/bus.json
	python3 graph.py -t vectors data/bus.json -e $(END) -n $(BUS_TITLE) -l True\
	 -r True -m True
packethist: data/class.json
	python3 graph.py -t packethist data/class.json -n $(PROB_TITLE)\
	 -s $(PROB_STR) -r True -m True

report:
	cd doc && lualatex -shell-escape report.tex && biber report && lualatex -shell-escape report.tex && lualatex -shell-escape report.tex
