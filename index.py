import numpy
import nltk
import csv

brown = nltk.corpus.brown

fdist = nltk.FreqDist(w.lower() for w in brown.words(categories="news"))
print(fdist)

def tfidf(w, freqs, count):
  return freqs[w], count

def freq(s, corpus):
  return sum([tfidf(w, corpus) for w in str.split(s)])

def feature_vector(tweet):
  return [tweet[10], tweet[2], tweet[13]]

def load():
  with open('./russian-troll-tweets/IRAhandle_tweets_1.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      featureVector(row)

def main():
  load()

if __name__ == "__main__":
  "out"
  #main()
