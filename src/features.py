import numpy as np


def get_spectrum_features(X, Y):
	pass

def get_complexity_features(filename):
	lines = []
	with open(filename, 'r') as f:
		lines = f.readlines()

#spectrum based features
def ochiai(p, f, total_f):
	den = math.sqrt(total_f * (f + p))
	return f / den

def jaccard()


#complexity based features
def line_length(line):


def num_tokens(line):


def num_alphanum(line):


def count_functions(line):
	if 

def assigns_variable(line):
	