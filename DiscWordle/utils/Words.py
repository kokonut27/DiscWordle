from english_words import english_words_lower_alpha_set as englishWords

def getWord():
  """
  Retrieves 5 letter word from English Dictionary.
  """
  allWords = []
  for word in englishWords:
    if len(word) == 5:
      allWords.append(word)
  return allWords