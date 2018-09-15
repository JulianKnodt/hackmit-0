import scipy.spatial
import numpy as np
import nltk
import csv
import fileinput

browndist = nltk.FreqDist(w.lower() for w in nltk.corpus.brown.words(categories="news"))
webdist = nltk.FreqDist(w.lower() for w in nltk.corpus.webtext.words())
sotu = nltk.FreqDist(w.lower() for w in nltk.corpus.state_union.words())

def freq(s, dist):
  words = str.split(s)
  return sum([dist.freq(w) for w in words])/len(words)

def feature_vector(cntn):
  return [freq(cntn, browndist), freq(cntn, webdist), freq(cntn, sotu)]

def load():
  data = []
  content = []
  for i in range(1,10):
    with open("./russian-troll-tweets/IRAhandle_tweets_%d.csv" % i) as csvfile:
      reader = csv.reader(csvfile)
      for row in reader:
        fv = feature_vector(row[2])
        data.append(fv)
        content.append((row[2], row[7], row[8])
  return scipy.spatial.KDTree(data, leafsize=5000), content

def main():
  tree, content = load()
  while True:
    print("Please input a sample tweet")
    result = ""
    for line in fileinput.input():
      result += line
    fv = feature_vector(result)
    _, indices = tree.query([fv], k=3)
    for i in indices[0]:
      print(content[i])

if __name__ == "__main__":
  main()

