import pandas as pd
import re


# ---- Categorize Instagram Messages ---- #
IG_LOG = 'parsed_data/ig_dms.csv'
ig_df = pd.read_csv(IG_LOG)

# filter out reaction messages
reaction_pattern = r'Reacted (.*?) to your message'
ig_df = ig_df[ig_df['content'].apply(lambda x: not bool(re.search(reaction_pattern, x)) if isinstance(x, str) else True)]

# filter out start call messages
ig_df = ig_df[ig_df['content'].apply(lambda x: 'started an audio call' not in x if isinstance(x, str) else True)]

# filter out add to collection messages
ig_df = ig_df[ig_df['content'].apply(lambda x: 'added to a collection' not in x if isinstance(x, str) else True)]

# make a separate df for calls
ig_calls = ig_df[ig_df['call_duration'].notna()]
ig_df = ig_df[ig_df['call_duration'].isna()]

# make a separate df for shared content
ig_media = ig_df[ig_df['content'].apply(lambda x: 'sent an attachment.' in x if isinstance(x, str) else False)]
ig_df = ig_df[ig_df['content'].apply(lambda x: 'sent an attachment.' not in x if isinstance(x, str) else True)]

ig_media = pd.concat([ig_media, ig_df[ig_df['share_link'].notna()]], ignore_index=True)
ig_df = ig_df[ig_df['share_link'].isna()]

ig_media = pd.concat([ig_media, ig_df[ig_df['share_content_owner'].notna()]], ignore_index=True)
ig_df = ig_df[ig_df['share_content_owner'].isna()]

ig_msgs = ig_df[['sender_name', 'timestamp_ms', 'content', 'reaction']]
ig_calls = ig_calls[['sender_name', 'timestamp_ms', 'content', 'call_duration']]
ig_media = ig_media[['sender_name', 'timestamp_ms', 'content', 'share_link', 'share_text', 'share_content_owner', 'reaction']]

ig_msgs.to_csv('intermediate_data/ig_msgs.csv', index=False)
ig_calls.to_csv('intermediate_data/ig_calls.csv', index=False)
ig_media.to_csv('intermediate_data/ig_media.csv', index=False)


# ---- Categorize SMS Messages ---- #
SMS_LOG = 'parsed_data/sms_conversation.csv'
sms_df = pd.read_csv(SMS_LOG)

# filter out google reactions
reactions_df = sms_df[sms_df['body'].apply(lambda x: '\u200A' in x)]
sms_df = sms_df[sms_df['body'].apply(lambda x: '\u200A' not in x)]

# filter out iMessage reactions
verbs = ['Loved', 'Liked', 'Disliked', 'Laughed at', 'Emphasized', 'Questioned']
message_pattern_format = '{verb} “(.*)”'
media_pattern_format = '{verb} an (.*)'

for verb in verbs:
    message_pattern = message_pattern_format.format(verb=verb)
    media_pattern = media_pattern_format.format(verb=verb)
    reactions_df = pd.concat([reactions_df, sms_df[sms_df['body'].apply(lambda x: bool(re.search(message_pattern, x)))]], ignore_index=True)
    reactions_df = pd.concat([reactions_df, sms_df[sms_df['body'].apply(lambda x: bool(re.search(media_pattern, x)))]], ignore_index=True)
    sms_df = sms_df[sms_df['body'].apply(lambda x: not bool(re.search(message_pattern, x)))]
    sms_df = sms_df[sms_df['body'].apply(lambda x: not bool(re.search(media_pattern, x)))]

reactions_df.to_csv('intermediate_data/sms_reactions.csv', index=False)
sms_df.to_csv('intermediate_data/sms_msgs.csv', index=False)


# ---- Combine Instagram and SMS Messages ---- #
sms_msgs = pd.read_csv('intermediate_data/sms_msgs.csv')
ig_msgs = pd.read_csv('intermediate_data/ig_msgs.csv')

# Rename the columns
sms_msgs = sms_msgs.rename(columns={'date': 'timestamp_ms', 'author': 'sent_by', 'body': 'content'})
ig_msgs = ig_msgs.rename(columns={'sender_name': 'sent_by'})

# Concatenate the two dataframes
all_msgs = pd.concat([sms_msgs, ig_msgs], ignore_index=True)

# Convert timestamp_ms to datetime
all_msgs['datetime'] = pd.to_datetime(all_msgs['timestamp_ms'], unit='ms')

# Replace names in the 'sent_by' column
all_msgs['sent_by'] = all_msgs['sent_by'].replace(['Nathan k', 'Bernice Lau'], ['Nathan', 'Bernice'])

# Save the resulting dataframe
all_msgs[['datetime', 'sent_by', 'content', 'reaction']].to_csv('intermediate_data/all_msgs.csv', index=False)