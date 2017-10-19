from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import nltk

nltk.download(['punkt', 'stopwords','treebank'])

def summarize(text, n):
	sents = sent_tokenize(text)
	words = [word_tokenize(s.lower()) for s in sents]

	freq = _wordFrequency(words)
	rank = defaultdict(int)
	for i,sent in enumerate(words):
		for w in sent:
			rank[i] -= 0.3 #straffer lengre settninger
			if w in freq:
				rank[i] += freq[w]
	index = nlargest(n,rank, key=rank.get)
	return([sents[j] for j in index])


def _wordFrequency(words):
	maxCut = 0.9
	minCut = 0.1
	freq = defaultdict(int)
	stopwordlist = set(stopwords.words('english') +list(punctuation))
	for s in words:
		for w in s:
			if w not in stopwordlist:
				freq[w] += 1
	m = float(max(freq.values()))
	freqkeys = []
	for w in freq.keys():
		freqkeys.append(w)
	for w in freqkeys:
		freq[w] = freq[w]/m
		if freq[w] > maxCut or freq[w] < minCut:
			del freq[w]
	return freq
