from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from matplotlib import pyplot


'''
PCA of potential orb conversation with plot of projections developed to better understand word relationships and for the 
report 
'''
class PcAnalysis:

	sentences = []

	def __init__(self):
		self.sentences = []
	def analysis(self):
		# define training data
		sentences = [['this', 'is', 'the', 'first', 'sentence', 'for', 'word2vec'],
					['Hi','i','am','ORB','how','can','1','help?'],
					['Hi','ORB','i ','want ','to','travel','on','a','train '],
					['From','Norwich'],
					['to','London'],
					['at','7','am','please'],
					['and', 'the', 'final', 'sentence']]
		# train model
		model = Word2Vec(sentences, min_count=1)
		# fit a 2D PCA model to the vectors
		X = model[model.wv.vocab]
		pca = PCA(n_components=2)
		result = pca.fit_transform(X)
		# create a scatter plot of the projection
		pyplot.scatter(result[:, 0], result[:, 1])
		words = list(model.wv.vocab)
		for i, word in enumerate(words):
			pyplot.annotate(word, xy=(result[i, 0], result[i, 1]))
		pyplot.show()

def main():
    print("running principle component analysis")

if __name__ == "__main__":
	analysisValue = PcAnalysis()
	analysisValue.analysis()
	main()

