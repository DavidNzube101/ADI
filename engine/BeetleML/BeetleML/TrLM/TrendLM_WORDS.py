import random

class AdaptiveDifferenceAlgorithm:
    def __init__(self, baseline_values):
        self.baseline_values = baseline_values
        self.adaptive_difference_threshold = sum(baseline_values) / len(baseline_values)

    def is_anomalous(self, word_length):
        deviation = abs(word_length - self.adaptive_difference_threshold)
        return deviation > self.adaptive_difference_threshold

    def generate_meaningful_sentence(self, words):
        meaningful_sentence = []
        for word in words:
            word_length = len(word)
            if not self.is_anomalous(word_length):
                meaningful_sentence.append(word)

        return meaningful_sentence


# Train the algorithm on a dataset of meaningful sentences.
baseline_sentences = [
    "This is a sentence.",
    "This is another sentence.",
    "This is a third sentence."
]

# Convert sentences into lists of word lengths for baseline values.
baseline_values = [len(sentence.split()) for sentence in baseline_sentences]

algorithm = AdaptiveDifferenceAlgorithm(baseline_values)

# Generate a new sentence.
new_words = random.choices(["This", "is", "a", "sentence.", "This", "is", "another", "sentence.", "This", "is", "a", "third", "sentence."], k=10)

# Identify and remove anomalous words from the new sentence.
meaningful_sentence = algorithm.generate_meaningful_sentence(new_words)

# Print the new sentence.
print("Meaningful sentence:", " ".join(meaningful_sentence))
