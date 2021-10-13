# Get App and Process Details

This is a helper for the Workspace ONE Intelligent Hub for macOS feature for blocking apps and processes. 

## Read First - VMware Docs

[VMware Docs for Apps and Process Restrictions for macOS](https://docs.vmware.com/en/VMware-Workspace-ONE-UEM/services/macOS_Platform/GUID-1457AF26-9546-49E5-8D63-6D9162604456.html?hWord=N4IghgNiBcIEoFMDOAXATgSwMYoAQFswsB5AZVwEEAHKibMFDAewDslcAyXABTSa2RJkIAL5A) 

## Author
Created by Adam Matthews (adam@adammatthews.co.uk) GitHub: [adammatthews](https://github.com/adammatthews) Twitter: [@AdamPMatthews](https://twitter.com/AdamPMatthews)


## Installation

A Mac is required to run this tool. Download the appblocker.py script. Ensure you have Python 3 installed, no additional packages required. 

## Usage

On a Mac where you have the apps you intend to block installed, follow the below steps. 

```shell
python3 appblock.py --list
```
```shell
python3 appblock.py --app /System/Applications/Utilities/Terminal.app
```
--List will show you an output of all installed applications on your Mac, under /Applications, /System/Applications and /System/Applications/Utilities. 

--apps "application path" will show the details required to populate the Custom XML payload to set up the App and Process blocking feature. 

## Output 

If you are setting up a new profile, use the entire output, and remove the comment lines. 

If you are adding an additional app to an existing profile, jusy copy the lines between the comments to the initial array. 

```shell
% python3 appblock.py --app "/System/Applications/Utilities/Disk Utility.app"


----- App and Process Blocking Details for Custom Settings Profile-----
Name: Disk Utility
File Path: /System/Applications/Utilities/Disk Utility.app/Contents/MacOS
CD Hash: 8b227c9f08fd4742fa1c98e4299d905629ae9673
Team ID: not set
SHA-256: c895cee3b20a18aff5828a8163d988be0508b93d9843b7094ba8e6691e8b73ba
Bundle ID: com.apple.DiskUtility

<dict>
	<key>Restrictions</key>
	<array>
======== Beginning of app config (delete this line) ========
<dict>
	<key>Attributes</key>
	<dict>
		<key>cdhash</key>
		<string>8b227c9f08fd4742fa1c98e4299d905629ae9673</string>
		<key>name</key>
		<string>Disk Utility</string>
		<key>sha256</key>
		<string>c895cee3b20a18aff5828a8163d988be0508b93d9843b7094ba8e6691e8b73ba</string>
		<key>path</key>
		<string>/System/Applications/Utilities/Disk Utility.app/Contents/MacOS</string>
		<key>bundleId</key>
		<string>com.apple.DiskUtility</string>
	</dict>
	<key>Actions</key>
	<array>
		<integer>1</integer>
	</array>
	<key>Message</key>
	<string>You are not permitted to use the Disk Utility App</string>
</dict>
======== End of App Config - Rest of payload, use if required (delete this line) ========
	</array>
	<key>PayloadDisplayName</key>
	<string>Restricted Software Policy</string>
	<key>PayloadIdentifier</key>
	<string>HubSettings.4cf9b463-2fe0-4b06-8df1-c24c67d8bd64</string>
	<key>PayloadOrganization</key>
	<string>VMware</string>
	<key>PayloadType</key>
	<string>com.vmware.hub.mac.restrictions</string>
	<key>PayloadUUID</key>
	<string>4cf9b463-2fe0-4b06-8df1-c24c67d8bd64</string>
	<key>PayloadVersion</key>
	<integer>1</integer>
</dict>
```

## Contributing
Changes and improvements welcome. 

## License
[BSD 3-Clause License](https://github.com/vmware-samples/euc-samples/blob/master/LICENSE)