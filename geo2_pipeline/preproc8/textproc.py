import re, sys
from nlp import twokenize

def repetition_filter_token(token):
  if twokenize.Url_RE.search(token):
    return token
  elif token.startswith('#'):
    return token
  elif token.startswith('@'):
    return token
  else: 
    return re.sub(r"([^0-9])\1{2,}", r"\1\1", token, re.U)

def repetition_filter_toks(toks):
  return [repetition_filter_token(tok) for tok in toks]

def do_tokenization(text, lower=True):
  """ASSUME text is already tokenize, and is unicode"""
  if lower:
    text = text.lower()
  toks = text.split()
  rtoks = repetition_filter_toks(toks)
  return rtoks

def test_repetition_filter(text):
  text = text.lower()
  toks = text.split()
  rtoks = repetition_filter_toks(toks)
  if toks==rtoks:
    print "SAME"
  else:
    t1 = u' '.join(toks).encode('utf-8')
    t2 = u' '.join(rtoks).encode('utf-8')
    print "DIFF" + "\n\t" + t1 + "\n\t" + t2

