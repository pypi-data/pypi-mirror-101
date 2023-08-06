Youtube-Video-Comment-Replies-Scraper-Python is a python library to fetch video comment replies on youtube using browser automation. 
It currently runs only on windows.

### Example
In this example we first import library, then we open video link and fetch comment replies.
```sh
from youtube_video_comment_replies_scraper_python import *
youtube.open("https://www.youtube.com/watch?v=LMmuChXra_M")
youtube.keypress("pagedown")
youtube.click_view_replies(comment='The person who is reading this comment , i wish you great success , health, love and happiness !') # will click on view replies of comment passed
youtube.click_show_more_replies() #will click on show more replies to load more replies
response=youtube.get_comment_replies()
data=response['body']
#data=[{"userlink": "https://www.youtube.com/channel/UChLZFVcaw-tsCshiYTV326w", "replytext": "Om Chanting 108 times\nhttps://youtu.be/bcvdE6iISpc\nPlease watch and give your feedback", "user": "Spiritual Infinity"}]
```

This module depends on the following python modules
* [requests](https://pypi.org/project/requests/)
* [bot_studio](https://pypi.org/project/bot_studio/)

#### BotStudio
[bot_studio](https://pypi.org/project/bot_studio/) is needed for browser automation. As soon as this library is imported in code, automated browser will open up in which video will be opened and comment replies will be fetched.

Complete documentation for YouTube Automation available [here](https://youtube-api.datakund.com/en/latest/)

### Installation

```sh
pip install youtube-video-comment-replies-scraper-python
```

### Import
```sh
from youtube_video_comment_replies_scraper_python import *
```

### Open video
```sh
youtube.open("video url")
```

### Load comments
```sh
youtube.keypress("pagedown")
```

### Click on view replies
```sh
youtube.click_view_replies(comment="comment text")
```

### Get Replies
```sh
response=youtube.get_comment_replies()
data=response['body']
```

### Send Feedback to Developers
```sh
bot_studio.send_feedback(feedback="Need help with this ......")
```

### Contact Us
* [Telegram](https://t.me/datakund)
* [Website](https://datakund.com)

