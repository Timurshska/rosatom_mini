# Makefile
.PHONY: all

all: compiling

compiling:
	python prompt.py
	python prompt_experiments/razmetka_to_file.py
	python my_metric.py
	python prompt_experiments/painting.py
