import xml.etree.ElementTree as ET
from tqdm import tqdm 
import pandas as pd

SMS_DATA = 'data/sms_conversation.xml'
CALL_DATA = 'data/nathans_calls.xml'


# ---- Get SMS messages from xml ---- #
tree = ET.parse(SMS_DATA)
root = tree.getroot()

df = pd.DataFrame(columns=['protocol', 'address', 'date', 'type', 'subject', 'body', 'toa', 'sc_toa', 'service_center', 'read', 'status', 'locked', 'date_sent', 'sub_id', 'readable_date', 'contact_name'])
for child in tqdm(root):
    if child.tag == 'sms':
        df = pd.concat([df, pd.DataFrame([child.attrib])], ignore_index=True)

df['author'] = df['type'].apply(lambda x: 'Nathan' if x == '2' else 'Bernice')
df[['date', 'author', 'body', 'readable_date']].head(30)

df[['date', 'author', 'body', 'readable_date']].to_csv('parsed_data/sms_conversation.csv', index=False)


# ---- Get MMS messages from xml --- #
tree = ET.parse(SMS_DATA)
root = tree.getroot()

df = pd.DataFrame(columns=['date', 'spam_report', 'ct_t', 'msg_box', 'address', 'sub_cs', 're_type', 'retr_st', 're_original_body', 'd_tm', 'exp', 'locked', 'msg_id', 'app_id', 'from_address', 'm_id', 'retr_txt', 'date_sent', 'read', 'rpt_a', 'ct_cls', 'bin_info', 'pri', 'sub_id', 're_content_type', 'object_id', 'resp_txt', 're_content_uri', 'ct_l', 're_original_key', 'd_rpt', 'reserved', 'using_mode', '_id', 'rr_st', 'm_type', 'favorite', 'rr', 'sub', 'hidden', 'deletable', 'read_status', 'd_rpt_st', 'callback_set', 'seen', 're_recipient_address', 'device_name', 'cmc_prop', 'resp_st', 'text_only', 'sim_slot', 'st', 'retr_txt_cs', 'creator', 'm_size', 'sim_imsi', 'correlation_tag', 're_body', 'safe_message', 'tr_id', 'm_cls', 'v', 'secret_mode', 're_file_name', 're_count_info', 'readable_date', 'contact_name'])
for child in tqdm(root):
    if child.tag == 'mms':
        df = pd.concat([df, pd.DataFrame([child.attrib])], ignore_index=True)

df['author'] = df['msg_box'].apply(lambda x: 'Nathan' if x == '2' else 'Bernice')
df[['date', 'author', 'readable_date']].to_csv('parsed_data/mms_conversation.csv', index=False)

for column in df.columns:
    amount = df[column].nunique()
    if amount < 10:
        print(f'{column}: {df[column].unique()}')
    else:
        print(f'{column}: {df[column].nunique()} unique values')


# ---- Get calls from xml ---- #
tree = ET.parse(CALL_DATA)
root = tree.getroot()
root[0].attrib.keys()

df = pd.DataFrame(columns=['number', 'duration', 'date', 'type', 'presentation', 'subscription_id', 'post_dial_digits', 'subscription_component_name', 'readable_date', 'contact_name'])
for child in tqdm(root):
    df = pd.concat([df, pd.DataFrame([child.attrib])], ignore_index=True)

types = {   # just for reference
    '1': 'Incoming',
    '2': 'Outgoing',
    '3': 'Missed',
    '5': 'Voicemail'
}

df = df[df['contact_name'] == 'Bernice Lau']
df['caller'] = df['type'].apply(lambda x: 'Nathan' if x in ('2', '5') else 'Bernice')
df['missed'] = df['type'].apply(lambda x: True if x in ('3', '5') else False)

df[['date', 'caller', 'duration', 'missed', 'readable_date']].to_csv('parsed_data/call_log.csv', index=False)
df[['date', 'caller', 'duration', 'missed', 'readable_date']].head(50)