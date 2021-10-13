#!/usr/bin/python3
#
# Helper tool to find required data for Workspace ONE UEM App Blocking functionality for macOS
#
# Created by Adam Matthews - adam@adammatthews.co.uk // matthewsa@vmware.com 
# Date: 6th July 2021
# Update: 13th October 2021
#

import subprocess, sys, getopt, re, argparse, os, uuid

parser = argparse.ArgumentParser()
parser.add_argument('--apps', help='Application Path')
parser.add_argument('--list', help='List applications', action='store_true')

args = parser.parse_args()

if args.apps:
	app = args.apps
	cmd = ["/usr/bin/codesign","-dv","--verbose=4",app]
	returned_value = subprocess.run(cmd, capture_output=True) # returns the exit code in unix

	out = returned_value.stderr

	cdhash = ""
	teamid = ""
	sha256 = ""
	name = ""
	bundleid = ""
	path = ""

	# get CDHash
	for line in out.splitlines():	
		result = str(line).find('CDHash',0,10)
		if result > 0:
			# print(line) #CDHash
			m = re.search('(?<=\=).*', str(line, 'utf-8').rstrip())
			cdhash = m.group(0)
	# get TeamIdentifier
	for line in out.splitlines():	
		result = str(line).find('TeamIdentifier',0,20)
		if result > 0:
			# print(line) #TeamID
			m = re.search('(?<=\=).*', str(line, 'utf-8').rstrip())
			teamid = m.group(0)

	# Get Sha-256 Hash
	list_files = subprocess.run(["ls", f"{app}/Contents/MacOS"], capture_output=True)

	ps = subprocess.Popen(("ls", f"{app}/Contents/MacOS"), stdout=subprocess.PIPE)
	sha_contents = subprocess.check_output(('head', '-1'), stdin=ps.stdout)

	#sha_contents = str(list_files.stdout, 'utf-8').rstrip()
	name = str(sha_contents, 'utf-8').rstrip()
	sha = ["/usr/bin/openssl","dgst","-sha256",f"{app}/Contents/MacOS/{name}"]
	sha_value = subprocess.run(sha, capture_output=True) # returns the exit code in unix
	sha_out = sha_value.stdout
	m = re.search('(?<=\=).*', str(sha_out, 'utf-8'))
	if m is not None:
		sha256 = m.group(0).strip()
	else:
		sha256 = "none"

	bundle_plist = subprocess.run(["osascript", "-e", f"id of app \"{name}\""], capture_output=True)
	bundleid = str(bundle_plist.stdout, 'utf-8').strip()
	print(f"")
	print(f"----- App and Process Blocking Details for Custom Settings Profile-----")
	print(f"Name: {name}")
	print(f"File Path: {app}/Contents/MacOS")
	print(f"CD Hash: {cdhash}")
	print(f"Team ID: {teamid}")
	print(f"SHA-256: {sha256}")
	print(f"Bundle ID: {bundleid}")
	print(f"")

	print("<dict>")
	print("\t<key>Restrictions</key>")
	print("\t<array>")

	print("======== Beginning of app config (delete this line) ========")

	print("<dict>")
	print("\t<key>Attributes</key>")
	print("\t<dict>")
	if cdhash:
		print("\t\t<key>cdhash</key>")
		print(f"\t\t<string>{cdhash}</string>")
	print("\t\t<key>name</key>")
	print(f"\t\t<string>{name}</string>")
	if sha256:
		print("\t\t<key>sha256</key>")
		print(f"\t\t<string>{sha256}</string>")
	print("\t\t<key>path</key>")
	print(f"\t\t<string>{app}/Contents/MacOS</string>")
	if bundleid:
		print("\t\t<key>bundleId</key>")
		print(f"\t\t<string>{bundleid}</string>")
	print("\t</dict>")
	print("\t<key>Actions</key>")
	print("\t<array>")
	print("\t\t<integer>1</integer>")
	print("\t</array>")
	print("\t<key>Message</key>")
	print(f"\t<string>You are not permitted to use the {name} App</string>")
	print("</dict>")

	print("======== End of App Config - Rest of payload, use if required (delete this line) ========")
	print("\t</array>")
	print("\t<key>PayloadDisplayName</key>")
	print("\t<string>Restricted Software Policy</string>")
	print("\t<key>PayloadIdentifier</key>")
	unique_uuid = uuid.uuid4()
	print(f"\t<string>HubSettings.{unique_uuid}</string>")
	print("\t<key>PayloadOrganization</key>")
	print("\t<string>VMware</string>")
	print("\t<key>PayloadType</key>")
	print("\t<string>com.vmware.hub.mac.restrictions</string>")
	print("\t<key>PayloadUUID</key>")
	print(f"\t<string>{unique_uuid}</string>")
	print("\t<key>PayloadVersion</key>")
	print("\t<integer>1</integer>")
	print("</dict>")

if args.list:
	list_apps = subprocess.run(["ls"], capture_output=True, cwd="/Applications/")
	apps_list = list_apps.stdout

	list_system_apps = subprocess.run(["ls"], capture_output=True, cwd="/System/Applications/")
	system_apps_list = list_system_apps.stdout

	list_utility_apps = subprocess.run(["ls"], capture_output=True, cwd="/System/Applications/Utilities")
	utility_apps_list = list_utility_apps.stdout

	for line in apps_list.splitlines():	
		print(f'"/Applications/{str(line,"utf-8")}"')
	for line in system_apps_list.splitlines():		
		print(f'"/System/Applications/{str(line,"utf-8")}"')
	for line in utility_apps_list.splitlines():		
		print(f'"/System/Applications/Utilities/{str(line,"utf-8")}"')