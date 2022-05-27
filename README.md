# PharmacotherapyPathwaysViz


## Background: 
We are investigating why there is so much difference in care/outcomes across a large healthcare system such as the Department of Veterans Affairs. Using a variety of techniques we have found that prescription patterns of antidepressants vary by region. New York ramps people up on antidepressants fast, but KY/TN go slow. 

## Problem Description: 
I am depicting the prescription of antidepressants using a graph. We call this a process or care pathway. For example a person may start an antidepressant at 10 mg. Then ramp up to 20mg in 4months. Then decide to quit. 

## Installation and Usage
Using Python >= 2.7 type `make` from the current working directory.

The program can also be invoked directly from the command line.

`python pharmaPaths.py <graph1> <graph2>`

`<graph1>` is a weighted directed graph with a title on the first line and delimited by comma. See examples for details

`<graph2>` is a weighted directed graph with a title on the first line and delimited by comma. See examples for details

![Sample Visualization](https://raw.githubusercontent.com/rusheniii/PharmacotherapyPathwaysViz/master/sample_graph.svg)
