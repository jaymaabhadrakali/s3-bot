import requests
import os

from slack_sdk.webhook import WebhookClient

url = input('Enter Site URL: ')

rq = requests.get(url)
data = str(rq.content)

splitedData = list(data.split(".s3"))

buckets = []
for i in range(len(splitedData)-1):
    temp = ''
    for j in range(len(splitedData[i])-1, -1, -1):

        if splitedData[i][j] != '/':
            temp = splitedData[i][j] + temp

        if splitedData[i][j] == '/':
            break
    if temp not in buckets:
        buckets.append(temp)

print(f'\n->> Total {len(buckets)} Buckets Found:')

for i in range(len(buckets)):
    if i != len(buckets)-1:
        print('-> ' + buckets[i] + ',')
    else:
        print('-> ' + buckets[i])

val_nonVul = {}
for i in range(len(buckets)):
    l = os.system(f'cmd /c "aws s3 ls s3://{buckets[i]} --no-sign-request"')

    if str(l) == '0':
        val_nonVul[buckets[i]] = 'Vulnerable'
    else:
        val_nonVul[buckets[i]] = 'Not Vulnerable'

body = ''
for i in range(len(val_nonVul)):
    body = body + buckets[i] + ' - ' + val_nonVul[buckets[i]] + '\n'

body = 'S3-jaimin-bot\n' + 'Site Name:\n' + url + '\n\n' + body


# slack notify

url = "<-----------------------YOUR SLACK WEBHOOK URL----------------------------->" 
webhook = WebhookClient(url)

response = webhook.send(text=body)
assert response.status_code == 200
assert response.body == "ok"
