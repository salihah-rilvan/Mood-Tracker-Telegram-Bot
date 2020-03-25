import requests 
import json
import time
# add other import statements here if nec

##############################################################
# global variables 
##############################################################

chat_id =    # fill in your chat id here
api_token = '' # fill in your api token here 

# add other global variables here 
base_url = "https://api.telegram.org/bot{}/".format(api_token)

sendMsg_url = base_url + "sendMessage"
editMsg_url = base_url + "editMessageText"
sendPhoto_url = base_url + "sendPhoto"
sendDocument_url = base_url + "sendDocument"
getUpdates_url = base_url + "getUpdates"


##############################################################
# mood_tracker 
##############################################################


default_msg = "Please rate your current mood. 1(poor) to 5 (excellent)."
msg_text = default_msg

def send_msg(chat_id, msg_text):

	# user parse_mode parameter for formatting text
	# not required if your text is not formatted 
	params =  {'chat_id':chat_id, 'text':msg_text}
	r = requests.post(url=sendMsg_url, params=params)

	if r.status_code == 200:
		return r.json()
	return None 
send_msg(chat_id, msg_text)

interval_sec = 10
def mood_tracker(chat_id, interval_sec):
	#time.sleep(interval_sec)
	# get latest update id before this echobot 
	params = {'offset': 0}
	r = requests.get(url=getUpdates_url, params=params)
	try:
			previous_id = r.json()['result'][-1]['update_id']
	except:
			previous_id = 0 
	list_of_replies = {"1":"Oh no! Think positive and press on!","2":"Oh dear, hope you feel better soon!","3":"Exercise more to boost your mood!","4":"That's good! Keep it up!","5":"Amazing, I am happy for you!"}
	mood_record = []
	total=0
	count = 0
	while True:
	# we use try except here, because r.json()['result'] may be an empty list
	# alternatively, you can use IF-THEN to check that list is not empty 
	# run an infinite loop to continuously wait for more data inputs 
	# use CRTL-C in the terminal to stop the loop	
		send_msg(chat_id, default_msg)
		time.sleep(interval_sec/2)
		params = {'offset': previous_id+1}
		r = requests.get(url=getUpdates_url, params=params)
		print(r.json())
		results = r.json()['result'] # list of results, may be empty 
		print(results)
		time.sleep(interval_sec/2)
		if results == []:
			reply = "Please respond"
		else:

			for result in results:
				
				# we use an IF statement here, because the user may send sticker, files, etc
				# which are not text 
				# you can remove the IF statement if you assume that user will send only text 
				if 'text' in result['message']:
					text = result['message']['text']
					if text in list_of_replies:
						mood_record.append(int(text))
						if count<10:
							count +=1
						elif count==10:
							del mood_record[0]
						average = round(float(sum(mood_record)/count),1)
						reply = list_of_replies[text] + "\nYour avg mood for the last {} data points is {}".format(str(count),str(average))

					else:
						reply = "Sorry, please type a number between 1 and 5"
				else:
					reply = "Sorry, please type a number between 1 and 5"
					
				previous_id = max(previous_id, int(result['update_id']))
				print('previous_id', previous_id)
				
		send_msg(chat_id, msg_text = reply)
			
	return 
mood_tracker(chat_id, interval_sec)

