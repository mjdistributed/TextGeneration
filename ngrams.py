import string
from collections import Counter, defaultdict
from pandas import DataFrame
import operator

import sys  

# necessary to handle unicode while reading text file
reload(sys)  
sys.setdefaultencoding('utf8')

""" Definitions:
path: file path
text: string containing file contents
words: list of strings
"""

def get_key(n_gram):
  """ obtain unique identifier for n-gram """
  return string.join(n_gram, ' ')


def clean(text):
  ## todo - better cleaning
  return text.decode('unicode_escape').encode('ascii','ignore').replace('\n', '').lower()

def get_ngram_counts(text, n):
  """ returns a counter of all n-grams in file """
  cleaned = clean(text)
  # TODO: split also so that punctuation is its own 'word'
  words = cleaned.split(' ')
  counter = Counter()
  for start_idx in range(len(words) - n):
    end_idx = start_idx + n
    target = words[start_idx:end_idx]
    n_gram = get_key(target)
    counter.update({ n_gram: 1})
  return counter

def get_probability_df(count_dict):
  df = DataFrame.from_dict(count_dict.items())
  df.columns = ['n-gram', 'probability']
  df['probability'] = df['probability'] / sum(df['probability'])
  return df

def transition_matrix(path, n):
  with open(path, 'r') as myfile:
    text = myfile.read()
    return transition_matrix_for_text(text, n)
  raise Exception("should never get here")

def n_grams_for_text(text, n):
  n_grams = get_ngram_counts(text, n)
  df = get_probability_df(n_grams)
  return df

def counts_to_probabilities(transition_matrix):
  return {k: {counter_k: float(counter_v) / sum(v.values()) for counter_k, counter_v in v.items()} for k, v in transition_matrix.items()}

def transition_matrix_for_text(text, n):
  cleaned = clean(text)
  # TODO: split also so that punctuation is its own 'word'
  words = cleaned.split(' ')
  transition_matrix = defaultdict(Counter)
  for ngram_start_idx in range(len(words) - (n + 1)):
    next_token_idx = ngram_start_idx + n
    next_token = words[next_token_idx]
    n_gram = get_key(words[ngram_start_idx:next_token_idx])
    transition_matrix[n_gram].update({ next_token : 1 })
  return counts_to_probabilities(transition_matrix)

def smooth_transitions(transition_matrix):
  # to avoid getting 'stuck' in our walk, will need to smooth transition matrix such that each transition from 
  # every n-gram to every other token is possible, though unlikely
  return None

def random_walk(n_gram_probs, transition_matrix, num_steps):
  # choose a random starting point based on the likelihood of n-gram occurrence

  # for each step, move to the next token based on the likelihood of transition, and update our current state
  return None

test_text = 'hello i am hello i testing some stuff omg this is wild omg this is wild'
# probs = n_grams_for_text('hello i am testing some stuff omg this is wild omg this is wild', 2)
# probs = n_grams('neuromancer.txt', 2)
# probs.set_index('n-gram')
# print(sorted(probs.to_dict(outtype='records'), key=lambda x: x['probability'], reverse=True)[:10])

print(transition_matrix('neuromancer.txt', 2))