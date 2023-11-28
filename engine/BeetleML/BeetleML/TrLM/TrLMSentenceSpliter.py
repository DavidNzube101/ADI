import re

def split_sentences(text):
  """Splits a string into sentences.

  Args:
    text: A string to be split.

  Returns:
    A list of strings, where each string is a sentence.
  """

  # Regex pattern to match a full stop at the end of a sentence.
  sentence_end_pattern = r"\.(?=\s[A-Z])"

  # Split the string at each end of sentence.
  sentences = re.split(sentence_end_pattern, text)

  # Return the list of sentences.
  return sentences
