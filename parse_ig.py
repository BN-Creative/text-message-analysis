import json
import csv


# ---- Combine all the ig_dms files into one file ---- #
file_names = ['data/ig_dms_1.json', 'data/ig_dms_2.json', 'data/ig_dms_3.json']
all_messages = []

for file_name in file_names:
    with open(file_name, 'r') as file:
        data = json.load(file)
        all_messages.extend(data.get('messages', []))

with open('data/ig_dms_combined.json', 'w') as file:
    json.dump({"messages": all_messages}, file)


# ---- Parse the data and write to a CSV file ---- #
with open('data/ig_dms_combined.json', 'r') as file:
    data = json.load(file)

with open('parsed_data/ig_dms.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['sender_name', 'timestamp_ms', 'content', 'share_link', 'share_text', 'share_content_owner', 'reaction', 'call_duration'])  # Write header row

    for message in data['messages']:
        sender_name = message['sender_name']
        timestamp_ms = message['timestamp_ms']

        content = message.get('content')
        content = content.encode('latin-1').decode('utf-8') if content else None

        share_link = message.get('share', {}).get('link')
        share_text = message.get('share', {}).get('share_text')
        share_text = share_text.encode('latin-1').decode('utf-8') if share_text else None
        share_content_owner = message.get('share', {}).get('original_content_owner')

        reaction = message.get('reactions', [{}])[0].get('reaction')
        reaction = reaction.encode('latin-1').decode('utf-8') if reaction else None

        call_duration = message.get('call_duration')

        writer.writerow([sender_name, timestamp_ms, content, share_link, share_text, share_content_owner, reaction, call_duration])