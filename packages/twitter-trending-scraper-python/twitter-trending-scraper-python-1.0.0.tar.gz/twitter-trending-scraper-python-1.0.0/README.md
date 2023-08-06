 Twitter-Trending-Scraper-Python is a python library to scrape trending keywords on twitter using browser automation. 
It currently runs only on windows.

### Example
In this example we first import library, then we login with cookies and scrape trending keywords.
```sh
from twitter_trending_scraper_python import *
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
twitter.open("https://twitter.com/explore/tabs/trending")
response=twitter.trending()
data=response['body']
keywords=[]
for key in data:
    keywords.append(key['keyword'])
```

This module depends on the following python modules
* [requests](https://pypi.org/project/requests/)
* [bot_studio](https://pypi.org/project/bot_studio/)

#### BotStudio
[bot_studio](https://pypi.org/project/bot_studio/) is needed for browser automation. As soon as this library is imported in code, automated browser will open up.
Complete documentation for Twitter Automation available [here](https://twitter-api.datakund.com/en/latest/)

### Installation

```sh
pip install twitter-trending-scraper-python
```

### Import
```sh
from twitter_trending_scraper_python import *
```

### Login with credentials
```sh
twitter.login(username="twitter username",password="twitter password")
```

### Login with cookies
```sh
twitter.login_cookie(cookies=list_of_cookies)
```

### Open twitter trending page
```sh
twitter.open("trending link")
```

### Get trending keywords
```sh
response=twitter.trending()
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

