import numpy as np
import src.d4j_util as d4j_util
from src.SBFL.sbfl.base import SBFL

java_keywords = ['abstract', 'continue', 'for', 'new', 'switch', 'assert', 'default', 'goto', 'package', 'synchronized', 'boolean', 'do', 'if', 'private', 'this', 'break', 'double', 'implements', 'protected', 'throw', 'byte', 'else', 'import', 'public', 'throws', 'case', 'enum', 'instanceof', 'return', 'transient', 'catch', 'extends', 'int', 'short', 'try', 'char', 'final', 'interface', 'static', 'void', 'class', 'finally', 'long', 'strictfp', 'volatile', 'const', 'float', 'native', 'super', 'while']


#complexity based features
def num_keywords(line):
	total = 0
	s = line.strip().split()
	for st in s:
		if st in java_keywords:
			total += 1
	return total

def line_length(line):
	return len(line)

def num_tokens(line):
	s = line.strip().split(" ")
	return len(s)

def num_alphanum(line):
	total = 0
	for char in line:
		if str(char).isalnum():
			total += 1
	return total

def num_operators(line):
	operators = ["+", "-", "*", "/", "**", "%"]
	total = 0
	for o in operators:
		total += line.count(o)
	return total

def num_functions(line):
	return line.count("(") // 2

def assigns_variable(line):
	return "=" in line

def is_comment(line):
	return "//" in line or line.strip()[0] == "*"

complexity_funcs = [num_keywords, line_length, num_tokens, num_alphanum, num_operators, num_functions, assigns_variable, is_comment]
spec_funcs = ['Ochiai', 'Tarantula', 'Jaccard', 'RussellRao', 'Hamann', 'SorensonDice', 'Dice', 'Goodman', 'SimpleMatching', 'Op1', 'Ample', 'Dstar2', 'Ochiai2', 'Hamming', 'Euclid']

def get_full_feature_vector(X, y, filename, simple_model):
	r = simple_model(X)
	s = get_spectrum_features(X, y)
	c = get_complexity_features(X, y)
	return np.hstack((s, c, r))

def get_spectrum_features(X, y):
	result = None
	for sf in spec_funcs:
		sbfl = SBFL(formula=sf)
		s = sbfl.fit_predict(X, y)
		if result is None:
			result = s
		else:
			result = np.vstack((result, s))
	print(result.shape)
	return result


def get_complexity_features(labels, pid, bid):
	result = []
	lines = get_lines_from_labels(labels, pid, bid)
	for line in lines:
		line_result = [f(line) for f in complexity_funcs]
		result.append(line_result)
	return np.array(result)

def get_lines_from_labels(labels, pid, bid):
	p_vid = pid+'_'+bid+'b'
	d4j_util.checkout_project_vid(p_vid)
	program_statements_dict = d4j_util.get_program_statements_dict(p_vid)
	return [program_statements_dict[key] for key in labels]



# def spectrum_preprocess(X, y):
#     X, y = np.array(X), np.array(y)
#     assert np.all(X >= 0)
#     assert np.all(np.isin(y, [0, 1]))

#     X = binarize(X)
#     y = np.array(y)
#     f = np.sum(X[y==0], axis=0)
#     fn = np.sum(y == 0) - f
#     p = np.sum(X[y==1], axis=0)
#     pn = np.sum(y == 1) - p
#     return p, f, fn, pn

# #spectrum based features
# def ochiai(p, f, fn, pn):
# 	den = math.sqrt(total_f * (f + p))
# 	return f / den

# def op2(p, f, fn, pn):
#     return f-p/(p+pn+1)

# def dstar(p, f, fn, pn, star=2):
#     return np.power(f,star)/(p+fn)

# def tarantula(p, f, fn, pn, fn):
#     return (f/(f+fn))/((f/(f+fn))+(p/(p+pn)))

# def jaccard(p, f, fn, pn, fn):
#     return f/(f+fn+p)

# def gp13(p, f, fn, pn):
#     return f*(1 + 1/(2*p+f))
