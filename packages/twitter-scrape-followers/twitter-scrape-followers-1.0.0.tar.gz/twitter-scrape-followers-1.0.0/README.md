Twitter-Scrape-Followers is a python library to scrape followers of a twitter user using browser automation. 
It currently runs only on windows.

### Example1
In this example we first import library, then we login with cookies and scrape followers data one time only.
```sh
from twitter_scrape_followers import *
import time
true=True;false=False
list_of_cookies=[
{
    "domain": ".twitter.com",
    "expirationDate": 1676520136,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_ga",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "GA1.2.1110230825266.1610349768",
    "id": 1
}]
#please replace the above sample cookies with your cookies, can see below link of how to fetch cookies
twitter.login_cookie(cookies=list_of_cookies)
twitter.open("https://twitter.com/narendramodi/followers")
time.sleep(2)
response=twitter.get_followers()
data=response['body']
#data=[{"Link": "https://twitter.com/rupeshj08678392", "Info": "Rupesh Jain"},...]
```

### Example2:- Load More Followers
In this example we first import library, then we login with cookies and scrape followers five times, as it scrolls whenever function called.
```sh
from twitter_scrape_followers import *
import time
true=True;false=False
list_of_cookies=[
{
    "domain": ".twitter.com",
    "expirationDate": 1676520136,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_ga",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "GA1.2.1110230825266.1610349768",
    "id": 1
}]
#please replace the above sample cookies with your cookies, can see below link of how to fetch cookies
twitter.login_cookie(cookies=list_of_cookies)
twitter.open("https://twitter.com/narendramodi/followers")
time.sleep(2)
all_data=[]
for i in range(0,5):
	response=twitter.get_followers()
	data=response['body']
	all_data.extend(data)
#data=[{"Link": "https://twitter.com/rupeshj08678392", "Info": "Rupesh Jain"},...]
```

This module depends on the following python modules
* [requests](https://pypi.org/project/requests/)
* [bot_studio](https://pypi.org/project/bot_studio/)

#### BotStudio
[bot_studio](https://pypi.org/project/bot_studio/) is needed for browser automation. As soon as this library is imported in code, automated browser will open up.
Complete documentation for Twitter Automation available [here](https://twitter-api.datakund.com/en/latest/)

### Installation

```sh
pip install twitter-scrape-followers
```

### Import
```sh
from twitter_scrape_followers import *
```

### Login with credentials
```sh
twitter.login(username="twitter username",password="twitter password")
```

### Login with cookies
```sh
twitter.login_cookie(cookies=list_of_cookies)
```

### Open Followers page
```sh
twitter.open("followers link")
```

### Get Followers
```sh
response=twitter.get_followers()
data=response['body']
```

### Send Feedback to Developers
```sh
bot_studio.send_feedback(feedback="Need help with this ......")
```

### Cookies
To login with cookies [Edit this Cookie Extension](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?hl=en) can be added to browser. Please check [this](https://abhishek-chaudhary.medium.com/how-to-get-cookies-of-any-website-from-browser-22b3d6348ed2) link how to get cookies to login to your twitter.
### Contact Us
* [Telegram](https://t.me/datakund)
* [Website](https://datakund.com)

