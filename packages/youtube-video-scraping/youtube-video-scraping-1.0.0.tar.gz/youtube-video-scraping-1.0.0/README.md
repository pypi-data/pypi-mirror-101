Youtube-Video-Scraping is a python library to scrape youtube video data using browser automation. 
It currently runs only on windows.

### Example
In this example we first import library, then we fetched data using simple function.
```sh
from youtube_video_scraping import *
response=youtube.get_video_info(video_url='https://www.youtube.com/watch?v=LMmuChXra_M')
data=response['body']
#data={"DisLikes": "4.8K", "Title": "OM Chanting @ 528Hz", "Subscribers": "3.66M", "Comments": "2631", "ChannelLink": "https://www.youtube.com/channel/UCM0YvsRfYfsniGAhjvYFOSA", "ChannelName": "Meditative Mind", "Desc": "OM is the mantra, or vibrations that is chanted in the beginning and end of any Meditation or Yoga ", "Views": "9,737,330 views", "Duration": "3:20:02", "Publish_Date": "17 Aug 2016", "Likes": "84K"}
```

This module depends on the following python modules
* [requests](https://pypi.org/project/requests/)
* [bot_studio](https://pypi.org/project/bot_studio/)

#### BotStudio
[bot_studio](https://pypi.org/project/bot_studio/) is needed for browser automation. As soon as this library is imported in code, automated browser will open up in which video will be opened.

Complete documentation for YouTube Automation available [here](https://youtube-api.datakund.com/en/latest/)

### Installation

```sh
pip install youtube-video-scraping
```

### Import
```sh
from youtube_video_scraping import *
```

### Login with credentials
```sh
youtube.login(username="youtube username",password="youtube password")
```

### Login with cookies
```sh
youtube.login_cookie(cookies=list_of_cookies)
```

### Get video info
```sh
response=youtube.get_video_info(video_url='video_url')
data=response['body']
```

### Get only limited data
```sh
response=youtube.get_video_info(video_url='video_url',fields=['Subscribers'])
data=response['body']
#data={"Subscribers":""}
```

### Send Feedback to Developers
```sh
bot_studio.send_feedback(feedback="Need help with this ......")
```

### Contact Us
* [Telegram](https://t.me/datakund)
* [Website](https://datakund.com)

