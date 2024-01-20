import http.client, urllib, sys

# You will need to modify this section. Obtain a user key by ...
userKey = "YourUserKeyHere"

# You will need to modify this section. Obtain an app key by ...
appToken = "YourAppKeyHere"

# Message -- for this script, the first argument specified
message = sys.argv[1]

# Send push notification
connection = http.client.HTTPSConnection("api.pushover.net:443")
connection.request("POST", "/1/messages.json",
  urllib.parse.urlencode({
    "token": appToken,
    "user": userKey,
    "message": message,
  }), { "Content-type": "application/x-www-form-urlencoded" })
connection.getresponse()
