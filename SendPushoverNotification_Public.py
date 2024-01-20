import http.client, urllib, sys

# You will need to modify this section. Obtain an app key by signing up for Pushover, and locating the User Key in the "Your User Key" section of https://pushover.net/#apps. It is a string of 30 random letters and numbers. 
userKey = "YourUserKeyHere"

# You will need to modify this section. Obtain a user key by registering an application under "Your Applications" section of https://pushover.net/#apps. Once complete, you can click the name of your application on https://pushover.net/#apps, and your API token will be displayed. It is a string of 30 random letters and numbers. 
appToken = "YourAppKeyHere"

# Message -- for this script, the first argument specified in the prompt or in the batch script. 
try:
    message = sys.argv[1]
except:
    message = "Default notification from Agisoft Metashape"   

# Send push notification
connection = http.client.HTTPSConnection("api.pushover.net:443")
connection.request("POST", "/1/messages.json",
  urllib.parse.urlencode({
    "token": appToken,
    "user": userKey,
    "message": message,
  }), { "Content-type": "application/x-www-form-urlencoded" })
connection.getresponse()
