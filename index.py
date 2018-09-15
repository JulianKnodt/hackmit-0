import nltk
import csv

def featureVector(tweet):
  

def load():
  with open('./russian-troll-tweets/IRAhandle_tweets_1.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      featureVector(row)

def main():
  load()

if __name__ == "__main__":
  main()
