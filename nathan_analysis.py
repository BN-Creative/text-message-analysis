# %%
import pandas as pd
import emoji
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns

# %%
HOME = './'
MSGS = HOME + 'intermediate_data/all_msgs.csv'

# %%
msg_df = pd.read_csv(MSGS)
msg_df['datetime'] = pd.to_datetime(msg_df['datetime'])
msg_df['datetime'] = msg_df['datetime'].dt.tz_convert('Etc/GMT-8')
msg_df['datetime'] = msg_df['datetime'].dt.floor('s')

# %%
msg_df.head()

# %% [markdown]
# ## Emoji Analysis

# %%
msg_df['contains_emoji'] = msg_df['content'].apply(lambda x: any(emoji.is_emoji(c) for c in x) if isinstance(x, str) else False)
n_percent = len(msg_df[msg_df['sent_by'] == 'Nathan'][msg_df['contains_emoji']]) / len(msg_df[msg_df['sent_by'] == 'Nathan']) * 100
b_percent = len(msg_df[msg_df['sent_by'] == 'Bernice'][msg_df['contains_emoji']]) / len(msg_df[msg_df['sent_by'] == 'Bernice']) * 100
print(f'Nathan sends an emoji in {n_percent:.2f}% of his messages')
print(f'Bernice sends an emoji in {b_percent:.2f}% of her messages')

# %%
emojis_df = pd.DataFrame(columns=['datetime', 'sent_by', 'emoji'])

for i, row in tqdm(msg_df.iterrows(), total=msg_df.shape[0]):
    if not isinstance(row['content'], str):
        continue

    for c in row['content']:
        if emoji.is_emoji(c):
            emojis_df = pd.concat([emojis_df, pd.DataFrame({
                'datetime': row['datetime'], 
                'sent_by': row['sent_by'], 
                'emoji': c}, index=[0])
                ], ignore_index=True)

# %%
emojis_df.head()

# %%
def counts_and_percentages(emojis_df):
    total = emojis_df.shape[0]
    counts = emojis_df['emoji'].value_counts()
    counts_df = pd.DataFrame({'emoji': counts.index, 'count': counts.values})
    counts_df['percentage'] = 100 * counts_df['count'] / total
    return counts_df

# %%
total_counts_df = counts_and_percentages(emojis_df)

n_emojis_df = emojis_df[emojis_df['sent_by'] == 'Nathan']
n_counts_df = counts_and_percentages(n_emojis_df)

b_emojis_df = emojis_df[emojis_df['sent_by'] == 'Bernice']
b_counts_df = counts_and_percentages(b_emojis_df)

# %%
print('\n\n')
print('--------')

print('total unique emojis: ', len(total_counts_df))
print('total emojis sent: ', total_counts_df['count'].sum())
print(total_counts_df.head(10))

# %%
print('N unique emojis: ', len(n_counts_df))
print(n_counts_df.head(10))

# %%
print('B unique emojis: ', len(b_counts_df))
print(b_counts_df.head(10))

# %%
all_emojis = set(total_counts_df['emoji'])
n_emojis = set(n_counts_df['emoji'])
b_emojis = set(b_counts_df['emoji'])

n_unique_emojis = n_emojis - b_emojis
b_unique_emojis = b_emojis - n_emojis

print(f'Nathan has {len(n_unique_emojis)} unique emojis: {n_unique_emojis}')
print(f'Bernice has {len(b_unique_emojis)} unique emojis: {b_unique_emojis}')

# %%
hearts = emojis_df[emojis_df['emoji'] == '🥰']

# todo: pull out month and bin by month

sns.displot(x='datetime', data=hearts, hue='sent_by', )

# %% [markdown]
# ## Common days and times

# %%
total_days = msg_df['datetime'].dt.date.nunique()
msg_df.count() / total_days

# %%
# Define the order of the days
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

msg_df['datetime'] = pd.to_datetime(msg_df['datetime'])
msg_df['day'] = pd.Categorical(msg_df['datetime'].dt.day_name(), categories=days, ordered=True)
day_counts = msg_df['day'].value_counts().sort_index()
day_counts = day_counts / total_days * 7
day_counts.plot(kind='bar')

# %%
msg_df['hour'] = msg_df['datetime'].dt.hour
hour_counts = msg_df['hour'].value_counts().sort_index()
hour_counts = hour_counts / total_days
hour_counts.plot(kind='bar')


