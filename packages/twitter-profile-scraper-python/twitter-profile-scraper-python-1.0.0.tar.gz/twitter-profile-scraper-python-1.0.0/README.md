Twitter-Profile-Scraper-Python is a python library to scrape user profile data on twitter using browser automation. 
It currently runs only on windows.

### Example
In this example we first import library, then we login with cookies and scrape data.
```sh
from twitter_profile_scraper_python import *
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
response=twitter.get_user(profile_url='https://twitter.com/narendramodi')
data=response['body']
#data={"Joined": "Joined January 2009", "Info": "Prime Minister of India", "DOB": "Born September 17", "Following": "2349", "Website": "https://t.co/zzYhUUfq6i?amp=1", "Followers": "65.7M", "Location": "India", "Twitter_Id": "@narendramodi", "Name": "Narendra Modi
", "TweetsCount": "29K"}
```

This module depends on the following python modules
* [requests](https://pypi.org/project/requests/)
* [bot_studio](https://pypi.org/project/bot_studio/)

#### BotStudio
[bot_studio](https://pypi.org/project/bot_studio/) is needed for browser automation. As soon as this library is imported in code, automated browser will open up.
Complete documentation for Twitter Automation available [here](https://twitter-api.datakund.com/en/latest/)

### Installation

```sh
pip install twitter-profile-scraper-python
```

### Import
```sh
from twitter_profile_scraper_python import *
```

### Login with credentials
```sh
twitter.login(username="twitter username",password="twitter password")
```

### Login with cookies
```sh
twitter.login_cookie(cookies=list_of_cookies)
```

### Get user profile
```sh
response=twitter.get_user(profile_url='profile_url')
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

