import nltk
import sys
import os
import numpy as np
import string
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# important constants
d = 0.85
iterations = 30

# read file
input_file = open(sys.argv[1])

# tokenize
tokens = nltk.word_tokenize(input_file.read())
# get rid of punctuation
tokens = [token for token in tokens if token.isalpha()]
print(tokens)
print(len(tokens))

# define syntactic filters and apply them
filters = ["JJ", "NN", "NNP", "NNS", "RB", "RBR"]
tokens = [word for (word, pos) in nltk.pos_tag(tokens) if pos in filters] 

# lowercase all words
tokens = [token.lower() for token in tokens]
print(tokens)

# create a list of unique tokens
token_list = list(set(tokens))
dimension = len(token_list)
print(dimension)
print(token_list)

# init graph
graph = np.zeros((dimension, dimension))
print(graph.shape)

# run through the filtered tokens until the last token
for i in range(len(tokens) - 1):
	print(tokens[i])
	current_index = token_list.index(tokens[i])
	next_index = token_list.index(tokens[i + 1])
	# connect consecutive tokens in the graph
	graph[current_index, next_index] =  1 + graph[current_index, next_index]
	graph[next_index, current_index] = 1 + graph[next_index, current_index]

# remove all values in the diagonal -> ensure no token has an edge to itself
for i in range(dimension):
	graph[i, i] = 0

norm = np.sum(graph, axis = 0)
print(norm)
graph_normalized = np.divide(graph, norm, where = norm != 0) # this is ignore the 0 element in norm

print(token_list)
print(graph_normalized)

score_vector = np.ones(dimension)


for step in range(iterations):
	score_vector = (1 - d) + d * np.dot(graph_normalized, score_vector)

score_vector = sorted(score_vector, reverse = True)
print(score_vector)

for i in range(dimension):
	print(str(token_list[i]) + " = " + str(score_vector[i]))

final_words = list()
for i in range(min(dimension, 50)):
	final_words.append(token_list[i])
print(final_words)