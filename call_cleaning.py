# %%
import pandas as pd

# %%
HOME = './'
IG_CALLS = HOME + 'intermediate_data/ig_calls.csv'
PHONE_CALLS = HOME + 'parsed_data/call_log.csv'

# %%
ig_df = pd.read_csv(IG_CALLS)
phone_df = pd.read_csv(PHONE_CALLS)

# %% [markdown]
# ## End goal
# - datetime (tz US/Pacific)
# - caller
# - duration (in seconds, null if missed)
# - missed

# %%
phone_df['datetime'] = phone_df['date'].apply(lambda x: pd.to_datetime(x, unit='ms'))
phone_df['datetime'] = phone_df['datetime'].dt.tz_localize('UTC').dt.tz_convert('US/Pacific').dt.floor('s')

phone_df.loc[phone_df['missed'], 'duration'] = None

# %%
ig_df['datetime'] = pd.to_datetime(ig_df['timestamp_ms'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('US/Pacific').dt.floor('s')

ig_df['missed'] = ig_df['call_duration'] == 0

ig_df['duration'] = ig_df['call_duration']
ig_df.loc[ig_df['missed'], 'duration'] = None

ig_df['caller'] = ig_df['sender_name'].apply(lambda x: 'Nathan' if x == 'Nathan k' else 'Bernice')

# %%
all_calls = pd.concat([ig_df[['datetime', 'caller', 'duration', 'missed']], phone_df[['datetime', 'caller', 'duration', 'missed']]])
all_calls = all_calls.sort_values('datetime')
all_calls.to_csv(HOME + 'intermediate_data/all_calls.csv', index=False)

# %%
all_calls.head()
