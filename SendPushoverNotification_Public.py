import http.client, urllib, sys

# Auth arguments
userKey = "u82eurp8nvzbvpbtttf1xyrdd91iy2"
appToken = "auhvweppes6gxsu1wgxayg5e3eirz7"

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