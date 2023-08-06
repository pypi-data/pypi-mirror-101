Linkedin-Feed-Scraper-Bot is a python library to scrape feed data on linkedin using browser automation. 
It currently runs only on windows.

### Example1
In this example we first import library, then we login with cookies and then scrape data on linkedin.
```sh
from linkedin_feed_scraper_bot import *
true=True;false=False
list_of_cookies=[
{
    "domain": ".linkedin.com",
    "expirationDate": 1676463230,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_ga",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "GA1.2.1029585723.1610264105",
    "id": 1
}]
#please replace the above sample cookies with your cookies, can see below link of how to fetch cookies
linkedin.login_cookie(cookies=list_of_cookies)
response=linkedin.get_feed()
data=response['body']
```

### Example2:- Load More Data
In this example we first import library, then we login with cookies, fetch the data five times, as it scrolls whenever function called.
```sh
from linkedin_feed_scraper_bot import *
true=True;false=False
list_of_cookies=[
{
    "domain": ".linkedin.com",
    "expirationDate": 1676463230,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_ga",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "GA1.2.1029585723.1610264105",
    "id": 1
}]
#please replace the above sample cookies with your cookies, can see below link of how to fetch cookies
linkedin.login_cookie(cookies=list_of_cookies)
all_data=[]
for i in range(0,5):
	response=linkedin.get_feed()
	data=response['body']
	all_data.extend(data)
```
This module depends on the following python modules
* [requests](https://pypi.org/project/requests/)
* [bot_studio](https://pypi.org/project/bot_studio/)

#### BotStudio
[bot_studio](https://pypi.org/project/bot_studio/) is needed for browser automation. As soon as this library is imported in code, automated browser will open up. Complete documentation for Linkedin Automation available [here](https://linkedin-api.datakund.com/en/latest/)

### Installation

```sh
pip install linkedin-feed-scraper-bot
```

### Import
```sh
from linkedin_feed_scraper_bot import *
```

### Login with credentials
```sh
linkedin.login(username="linkedin username",password="linkedin password")
```

### Login with cookies
```sh
linkedin.login_cookie(cookies=list_of_cookies)
```

### Get Feed content 
```sh
response=linkedin.get_feed()
data=response['body']
```

### Send Feedback to Developers
```sh
bot_studio.send_feedback(feedback="Need help with this ......")
```

### Cookies
To login with cookies [Edit this Cookie Extension](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?hl=en) can be added to browser. Please check [this](https://abhishek-chaudhary.medium.com/how-to-get-cookies-of-any-website-from-browser-22b3d6348ed2) link how to get cookies to login to your linkedin.

### Contact Us
* [Telegram](https://t.me/datakund)
* [Website](https://datakund.com)

