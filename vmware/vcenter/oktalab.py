# Automated vCenter API driven VM Suspend and Start Script 
# Adam Matthews - adam@adammatthews.co.uk / adammatthews.couk
# Feb 2022
# Purpose - use in conjunction with a crontab entry to suspend and start a set of VM IDs (obtained by using GET https://{{host}}/api/vcenter/vm) 

import requests
import urllib3
import sys, getopt
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #Supress the HSTS errors


session = ""
vms = ["5008","5010","5011","5013"] # List of VM ID's you want to take action on
host = "https://vcsa.am-emm.lan/" # Root host of your vCenter Server

def start(): # Start an authenticated session
        global session

        url = host+"api/session"

        payload={}
        headers = {
          'Authorization': 'Basic YWRtaW5pc3RyYXRvckB2c3BoZXJlLmxvY2FsOlNlY3VyZXowMSE=' #Base 64 of username@domain:Password
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify = False)

        print("Session Started")
        session = response.text.strip('"')

        return session

def endsession(session): # End the active session

        callApi("api/session", "DELETE")

        print("Session Ended")

def callApi(url,method): # Call the API endpoint with the URL and method required

        payload={}
        headers = {
          'vmware-api-session-id': session
        }

        response = requests.request(method, host+url, headers=headers, data=payload, verify = False)
        return response.text

def suspend(): # Suspend VMs

        start()

        for x in vms:
          print(callApi("api/vcenter/vm/vm-"+x+"/power?action=suspend", "POST"))

        endsession(session)


def resume(): # Start the VMs

        start()

        for x in vms:
          print(callApi("api/vcenter/vm/vm-"+x+"/power?action=start", "POST"))

        endsession(session)


def main(argv):

  options, remainder = getopt.getopt(sys.argv[1:], 'sr', ['resume', 'suspend'])
  # print('OPTIONS   :', options)
  for opt, arg in options:
      if opt in ('-r', '--resume'):
          resume()
      elif opt in ('-s', '--suspend'):
          suspend()

if __name__ == "__main__":
   main(sys.argv[1:])

