# Fast dictionary lookup with defaults
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1

# Flatten a nested list with comprehension
flattened = [item for sublist in matrix for item in sublist]
