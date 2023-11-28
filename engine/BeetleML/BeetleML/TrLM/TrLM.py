import numpy as np
import TrLMSentenceSpliter as ss
import re
import random
import json

class Summarizer:
    def __init__(self, document):
        self.document = document
        self.sentences = ss.split_sentences(self.document)
        self.sentence_importance = [len(sentence.split()) for sentence in self.sentences]

    def compute_importance_scores(self):
        return self.sentence_importance

    def compute_baseline(self, importance_scores):
        return np.mean(importance_scores)

    def compute_adaptive_difference(self, importance_scores):
        baseline = self.compute_baseline(importance_scores)
        return [abs(score - baseline) for score in importance_scores]

    def generate_summary(self, threshold=random.choice([0.5, 0.6, 0.7])):
        importance_scores = self.compute_importance_scores()
        adaptive_diff_scores = self.compute_adaptive_difference(importance_scores)
        summary = [self.sentences[i] for i, score in enumerate(adaptive_diff_scores) if score > threshold]
        return summary

class Paraphraser:
    """Paraphrases words in the document"""
    def __init__(self, document):
        self.document = document
        # Define a list of verbs and their corresponding synonyms.
        with open("trlm_verbs.bet", "r") as _verbs:
            _verbs_syn_dict = _verbs.read()        

        self.verb_synonyms = json.loads(_verbs_syn_dict)

    def tokenizer(self):
        # Tokenize the text into words
        words = re.findall(r'\b\w+\b', self.document.lower())  # Convert to lowercase for case-insensitive matching
        return words

    def verbs_identifier(self, words):
        # Identify verbs within the text
        verbs = [word for word in self.tokenizer() if word in self.verb_synonyms]
        return verbs

    def generate_paraphrased(self):
        # Randomly select a synonym and replace the verb
        new_text = self.document
        verbs = self.verbs_identifier(new_text)
        for verb in verbs:
            synonyms = self.verb_synonyms.get(verb, [verb])  # Use the verb itself if no synonyms are available
            random_synonym = random.choice(synonyms)
            new_text = re.sub(r'\b{}\b'.format(verb), random_synonym, new_text, count=1)

        return new_text

# Sample document
samp_text = """ Natural language processing (NLP) is a field of artificial intelligence. It focuses on the interaction between computers and humans through natural language. It is used in various applications such as chatbots, sentiment analysis, and machine translation. NLP algorithms process and analyze text data to derive meaning and enable communication.
"""
# input("Your Text: ")


# Create the TextSummarizer instance
summarizer = Summarizer(samp_text)

print("no of words(before)-> " + str((len(re.findall(r'\b\w+\b', samp_text)))))

# Generate a summary
if (len(re.findall(r'\b\w+\b', samp_text))) < 3:
    summary = f"{summarizer.generate_summary()}"
    _ = "Just Perfect!"

elif (len(re.findall(r'\b\w+\b', samp_text))) < 10:
    summary = f"{summarizer.generate_summary()}"
    _ = "Just Perfect!"

elif (len(re.findall(r'\b\w+\b', samp_text))) < 20:
    summary = f"{summarizer.generate_summary()}"
    _ = "Just Perfect!"

elif (len(re.findall(r'\b\w+\b', samp_text))) > 30:
    summary = summarizer.generate_summary(threshold=1)

elif (len(re.findall(r'\b\w+\b', samp_text))) > 50:
    summary = summarizer.generate_summary(threshold=1)

elif (len(re.findall(r'\b\w+\b', samp_text))) > 75:
    summary = summarizer.generate_summary(threshold=3)

elif (len(re.findall(r'\b\w+\b', samp_text))) > 150:
    summary = summarizer.generate_summary(threshold=10)

elif (len(re.findall(r'\b\w+\b', samp_text))) > 500:
    summary = summarizer.generate_summary(threshold=15)

elif (len(re.findall(r'\b\w+\b', samp_text))) > 750:
    summary = summarizer.generate_summary(threshold=25)

elif (len(re.findall(r'\b\w+\b', samp_text))) > 1000:
    summary = summarizer.generate_summary(threshold=25)

else:
    summary = summarizer.generate_summary()

summary = "\n".join(summary)

# print("Summary:")
# print((summary))




try:
    if _:
        ph = Paraphraser(_)
    else:
        ph = Paraphraser(summary)
except NameError:
    ph = Paraphraser(summary)
    
phed = ph.generate_paraphrased()

# Print the modified text
print("\nRefined: " + phed)
print("no of words(after)-> " + str((len(re.findall(r'\b\w+\b', phed)))))
