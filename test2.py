excluded_words = ["the", "and", "a"]
words = ["the", "cat", "sat", "on", "the", "mat"]

# Using a list comprehension
words = [word for word in words if word not in excluded_words]

# Using the filter() function
words = list(filter(lambda word: word not in excluded_words, words))

print(words)  # Output: ['cat', 'sat', 'on', 'mat']