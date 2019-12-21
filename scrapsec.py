import json
import requests
import html
import os
import argparse
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from apscheduler.schedulers.blocking import BlockingScheduler
	
init = True

def sendEmail(receiver, code):
	content = "<h1>Change Detected at " + code + "</h1><br><h3><a href=\"https://bugcrowd.com/" +code+ "\">Visit the program</a></h3>"
	message = Mail(
		from_email='scrapsite@gmail.com',
		to_emails= receiver,
		subject='Change Detected !',
		html_content=content
	)	   
	try:
		sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
		response = sg.send(message)
		print(response.status_code)
		print(response.body)
		print(response.headers)
	except Exception as e:
		print(e)
		return

def compare_file(programs):
    global init
    global email
    print(email)
    try:        
        if init:	
            print(True)
            old_file = open('old.txt', 'w')
            for i in programs:
                old_file.write(str(i) + ',')

            old_file.close()	
            init = False
        else:
            old_file = open('old.txt', 'r')

            string =""                        
            with open('old.txt', 'r') as old_file:
            	string += old_file.readline()
            old_file.close()
            print("Stre",string)
            old_ls = string.split(',')
            old_ls.pop()
	
            old_file.close()

            if old_ls == programs:
                print(str(datetime.today()), ' : No new programs')
            else:               
                print(datetime.today(), ' : There is new program')
                old_file = open('old.txt', 'w')
                for i in programs:
                    old_file.write(str(i) + ',')

                print("SENDING MAIL", programs[0])    
                sendEmail(email, programs[0])
        print("init", init)   
    except Exception as e:
        print(e)


def scrap_data():
    URL = "https://bugcrowd.com/programs"
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html5lib')

    table = soup.find('div', class_='react-component react-component-program-search-app')

    main_tag = html.unescape(str(table))
    start = main_tag.find('{')
    end = main_tag.rfind('}')
    main_tag = main_tag[start:end + 1]

    new_dictionary = json.loads(main_tag)

    programs = []
    for i in new_dictionary['programs']:
        programs.append(i['code'])

    compare_file(programs)
initial = True

if __name__ == "__main__":
    global email
    parser = argparse.ArgumentParser(description ='Scrapy : A tool to get notified for latest programs on bugcrowd.')
    parser.add_argument('-t','--time', type=int,metavar='',required=True, help='Time between every check in seconds')
    parser.add_argument('-e','--email', type=str,metavar='',required=True, help='Email ID to send the notification')
    args = parser.parse_args()
    
    email = args.email
    if not os.environ.get('SENDGRID_API_KE'):
        print("Run install.sh first! \nRun it using the following command \n. install.sh ")
        exit()
    
    scheduler = BlockingScheduler()
    scheduler.add_job(scrap_data, 'interval', seconds=args.time)
    scheduler.start()

