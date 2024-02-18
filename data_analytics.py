import pandas as pd
import nltk
from nltk import ngrams
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
# nltk.download('punkt')
# nltk.download('stopwords')
from collections import Counter
import string


# ---- Set Up ---- #
df = pd.read_csv('intermediate_data/all_msgs.csv')
df = df[df['content'].notna()]

# Clean and tokenize the text data
df['content'] = df['content'].apply(lambda x: ''.join([i for i in str(x).lower() if i not in string.punctuation]))
df['tokens'] = df['content'].apply(word_tokenize)
df['tokens'] = df['content'].apply(lambda x: word_tokenize(x.lower()))
all_words = [word for tokens in df['tokens'] for word in tokens]


# ---- Most Common Words and Phrases ---- #

# Top 10 most common uncommon words
stop_words = set(stopwords.words('english'))
non_stop_words = [word for word in all_words if word not in stop_words and word.isalpha()]
word_counts = Counter(non_stop_words)
top_10_uncommon_words = word_counts.most_common(10)
print("\nThe top 10 most common uncommon words are:")
for word, count in top_10_uncommon_words:
    print(f"'{word}' appears {count} times")

# Top 5 most common phrases
all_ngrams = [ngram for tokens in df['tokens'] for ngram in ngrams(tokens, 5)]
ngram_counts = Counter(all_ngrams)
top_5_phrases = ngram_counts.most_common(5)
print("\nThe top 5 most common phrases are:")
for phrase, count in top_5_phrases:
    print(f"'{' '.join(phrase)}' appears {count} times")

# Number of times we said "I love you"
love_count = df['content'].str.contains('i love you', case=False).sum()
print(f"\nThe phrase 'I love you' appears {love_count} times")

# Top 5 pet names
pet_names = ['honey', 'honeybee', 'baby', 'babe', 'naynay', 'berry', 'beebee', 'pookie bear', 'sweetheart', 'darling', 'my love', 'lovey', 'angel', 'princess', 'prince', 'cutie', 'cutie pie', 'sexy', 'smexy', 'hot', 'hottie']
pet_name_counts = {name: 0 for name in pet_names}
for name in pet_names:
    df[name] = df['content'].str.contains(name, case=False)
    pet_name_counts[name] = df[name].sum()
top_5_pet_names = sorted(pet_name_counts.items(), key=lambda x: x[1], reverse=True)[:5]

print("The top 5 pet names are:")
for name, count in top_5_pet_names:
    print(f"'{name}' appears {count} times")

for name, count in top_5_pet_names:
    print(f"\n'{name}' was said by:")
    for person, count in df[df[name] == True]['sent_by'].value_counts().items():
        print(f"{person} {count} times")


# ---- Who Texts the Most? ---- #

# Average characters per text per person
avg_chars_per_text = df.groupby('sent_by')['content'].apply(lambda x: x.str.len().mean()).to_dict()
print("Average characters per text:")
for person, avg_chars in avg_chars_per_text.items():
    print(person, ": ", avg_chars)

# Number of messages from each person
msg_counts = df['sent_by'].value_counts().to_dict()
print("\nTotal number of messages:")
for person, count in msg_counts.items():
    print(person, ": ", count)

# Total words per person
df['word_count'] = df['content'].apply(lambda x: len(str(x).split()))
total_words_per_person = df.groupby('sent_by')['word_count'].sum().to_dict()
print("\nTotal words per person:")
for person, total_words in total_words_per_person.items():
    print(f"{person}: {total_words} words")

# Total characters per person
df['char_count'] = df['content'].apply(lambda x: len(str(x)))
total_chars_per_person = df.groupby('sent_by')['char_count'].sum().to_dict()
print("\nTotal characters per person:")
for person, total_chars in total_chars_per_person.items():
    print(f"{person}: {total_chars} characters")


# ---- Who Texts First and Last? ---- #
df['datetime'] = pd.to_datetime(df['datetime'])
df = df.sort_values('datetime')
df['time_diff'] = df['datetime'].diff()
threshold = pd.Timedelta(hours=1) # 1 hour threshold between conversations

# Conversation starters
df['is_conversation_start'] = df['time_diff'] > threshold
conversation_starts = df[df['is_conversation_start']]['sent_by'].value_counts()
print("\nNumber of times each person started a conversation:")
for person, count in conversation_starts.items():
    print(f"{person}: {count} times")

# Conversation enders
df['is_conversation_end'] = df['time_diff'].shift(-1) > threshold
conversation_ends = df[df['is_conversation_end']]['sent_by'].value_counts()

print("\nNumber of times each person ended a conversation:")
for person, count in conversation_ends.items():
    print(f"{person}: {count} times")