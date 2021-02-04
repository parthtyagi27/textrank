import spacy
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class TextRank:
	def __init__(self, input_src, d=0.85, iterations=30):
		self.d = d
		self.input_src = input_src
		self.nlp = spacy.load("en_core_web_sm")
		self.tokens = list()
		self.dimension = 0
		self.token_list = list()
		self.iterations = iterations
		self.score_vector = None
		self.keywords = list()

	def __preprocess_data(self):
		# self.tokens = nltk.word_tokenize(self.input_src)
		self.doc = self.nlp(self.input_src)
		for token in self.doc:
			if not token.is_stop:
				if token.pos_ == 'NOUN' or token.pos_ == 'ADJ':
					self.tokens.append(token.text.lower())

	def __generate_graph(self):
		self.token_list = list(set(self.tokens))
		self.dimension = len(self.token_list)
		graph = np.zeros((self.dimension, self.dimension))

		for i in range(len(self.tokens) - 1):
			current_index = self.token_list.index(self.tokens[i])
			next_index = self.token_list.index(self.tokens[i + 1])
			# connect consecutive tokens in the graph
			graph[current_index, next_index] =  1 + graph[current_index, next_index]
			graph[next_index, current_index] = 1 + graph[next_index, current_index]

		for i in range(self.dimension):
			graph[i, i] = 0
		
		norm = np.sum(graph, axis = 0)
		graph_normalized = np.divide(graph, norm, where = norm != 0) # this is ignore the 0 element in norm
		return graph_normalized

	def analyze(self, max_limit=10):
		self.__preprocess_data()
		graph = self.__generate_graph()
		self.score_vector = np.ones(self.dimension)

		for step in range(self.iterations):
			self.score_vector = (1 - self.d) + self.d * np.dot(graph, self.score_vector)

		self.score_vector = sorted(self.score_vector, reverse = True)
		for i in range(min(max_limit, self.dimension)):
			self.keywords.append(self.token_list[i])
		return self.keywords

	def generate_cloud(self):
		if len(self.keywords) == 0:
			self.analyze()
		
		word_cloud_input = ''
		word_cloud_input += " ".join(self.keywords)+" "
		print(type(word_cloud_input))
		
		cloud = WordCloud(width = 800, height = 800, background_color = 'white', min_font_size=10).generate(word_cloud_input)
		# plt.figure(figsize = (8, 8), facecolor = None) 
		# plt.imshow(cloud) 
		# plt.axis("off") 
		# plt.tight_layout(pad = 0) 
		# plt.show() 
		return cloud