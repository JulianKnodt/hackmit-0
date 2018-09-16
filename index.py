from sys import stdin
from bs4 import BeautifulSoup
import scipy.spatial
import sklearn.cluster
import numpy as np
import nltk
import itertools
import csv
import fileinput
import urllib.request
from flask import request, Flask
from flask_cors import CORS
import collections
import csv
import requests
from requests.auth import HTTPBasicAuth
import urllib.parse
import json
from watson_developer_cloud import NaturalLanguageClassifierV1

browndist = nltk.FreqDist(w.lower() for w in nltk.corpus.brown.words(categories="news"))
webdist = nltk.FreqDist(w.lower() for w in nltk.corpus.webtext.words())
sotu = nltk.FreqDist(w.lower() for w in nltk.corpus.state_union.words())
pcs = nltk.FreqDist(w.lower() for w in nltk.corpus.pros_cons.words())

max_iter = 13

# counts words from troll tweets, returning a counter, and the total word count
def tweet_freqs():
  cnt = collections.Counter()
  total = 0
  print("Counting tweets")
  for i in range(1, max_iter):
    with open("./russian-troll-tweets/IRAhandle_tweets_%d.csv" % i) as csvfile:
      reader = csv.reader(csvfile)
      for row in reader:
        cnt.update(str.split(row[2]))
        total += 1
  cnt.subtract(cnt.most_common(10)) # delete words like "to" and "the"
  print("Finished counting")
  return cnt, total-10

cnt, total = tweet_freqs()

def freq(s, dist):
  words = str.split(s)
  return sum([dist.freq(w) for w in words])/len(words)

def csv_freq(s):
  words = str.split(s)
  return sum([cnt[w]/total for w in words])/len(words)

def feature_vector(tw):
  return [freq(tw, browndist), freq(tw, webdist), freq(tw, sotu), freq(tw, pcs), csv_freq(tw)]

def load():
  data = []
  content = []
  visited = set()
  print("Loading data in")
  for i in range(1,max_iter):
    with open("./russian-troll-tweets/IRAhandle_tweets_%d.csv" % i) as csvfile:
      reader = csv.reader(csvfile)
      for row in reader:
        if len(row[2]) == 0:
          continue
        if not (row[2] in visited):
          visited |= set([row[2]])
        else:
          continue
        fv = feature_vector(row[2])
        data.append(fv)
        content.append((row[2], row[7], row[8]))

  return data, content

def main():
  data, content = load()
  tree = scipy.spatial.KDTree(data, leafsize=5000)
  while True:
    print("Please input the url of a tweet")
    result = ""
    userinput = stdin.readline()
    try:
      result += gettweet(userinput)
    except:
      print("Errored while fetching tweet")

    fv = feature_vector(result)
    _, indices = tree.query([fv], k=3)
    for i in indices[0]:
      print(content[i])

def gettweet(url):
  resp = urllib.request.urlopen(url)
  soup = BeautifulSoup(resp.read(), 'html.parser')
  return soup.find(class_="tweet-text").text

data, content = load()
tree = scipy.spatial.KDTree(data, leafsize=10000)

'''
def mean_shift_clustering(tree, indices):
  i = iter(indices)
  left = dict(izip(i, i))
  total = len(indices)
  clusters = {}
  while len(classified) < total:
    rand = d.popitem()
  return clusters
'''

app = Flask(__name__)
CORS(app)

@app.route("/approx")
def sample():
  tweet = request.args.get("tweet")
  if len(tweet) == 0:
    return ""
  _, indices = tree.query(feature_vector(tweet), k=10)
  return "\n".join([content[i][0] for i in indices])


@app.route("/check")
def check():
  tweet = request.args.get("tweet")
  if len(tweet) == 0:
    return ""
  r = requests.get("https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers/b8f3cex446-nlc-797/classify",
    auth=HTTPBasicAuth("6df58a9e-65b2-426c-b872-efbb341e6f52", "NBDJiVjB0P7N"),
    params={"text": urllib.parse.quote(tweet)})
  return r.text

@app.route("/cherk")
def cherk():
  tweet = request.args.get("tweet")
  natural_language_classifier = NaturalLanguageClassifierV1(
    username='6df58a9e-65b2-426c-b872-efbb341e6f52',
      password='NBDJiVjB0P7N')
  classes = natural_language_classifier.classify('b8f3cex446-nlc-797', tweet)
  print(json.dumps(classes, indent=2))

