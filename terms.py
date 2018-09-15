import collections
import csv

# counts words from troll tweets, returning a counter, and the total word count
def tweet_freqs():
  cnt = collections.Counter()
  total = 0
  for i in range(1, 10):
    with open("./russian-troll-tweets/IRAhandle_tweets_%d.csv" % i) as csvfile:
      reader = csv.reader(csvfile)
      for row in reader:
        cnt.update(str.split(row[2]))
        total += 1
  cnt.subtract(cnt.most_common(10)) # delete words like "to" and "the"
  return cnt, total-10

