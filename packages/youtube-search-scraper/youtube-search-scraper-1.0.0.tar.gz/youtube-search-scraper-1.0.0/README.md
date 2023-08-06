Youtube-Search-Scraper is a python library to search keyword automatically on youtube and get search results using browser automation. 
It currently runs only on windows.

### Example
In this example, we are searching a keyword and then getting search results. 
```sh
from youtube_search_scraper import *
youtube.search(keyword='cbse exams')
response=youtube.search_results()
data=response['body']
#data=[{"viewsandtime": "220K views 2 months ago", "channel": "the quint", "title": "CBSE Exams 2021: When Will Board Exams Happen?", "link": "https://www.youtube.com/watch?v=KSg1RleLs3M"},{},...]
```


This module depends on the following python modules
* [requests](https://pypi.org/project/requests/)
* [bot_studio](https://pypi.org/project/bot_studio/)

#### BotStudio
[bot_studio](https://pypi.org/project/bot_studio/) is needed for browser automation. As soon as this library is imported in code, automated browser will open up. Then you can search on browser using simple functions and get search results.

Complete documentation for YouTube Automation available [here](https://youtube-api.datakund.com/en/latest/)

### Installation

```sh
pip install youtube-search-scraper
```

### Import
```sh
from youtube_search_scraper import *
```

### Login with credentials
```sh
youtube.login(username="youtube username",password="youtube password")
```

### Login with cookies
```sh
youtube.login_cookie(cookies=list_of_cookies)
```

### Search
```sh
youtube.search(keyword='search keyword')
```

### Search Results
```sh
response=youtube.search_results()
data=response['body']
```

### Send Feedback to Developers
```sh
bot_studio.send_feedback(feedback="Need help with this ......")
```

### Contact Us
* [Telegram](https://t.me/datakund)
* [Website](https://datakund.com)

