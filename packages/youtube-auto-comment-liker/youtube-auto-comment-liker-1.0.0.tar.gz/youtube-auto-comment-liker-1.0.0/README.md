Youtube-Auto-Comment-Liker is a python library to like a comment of a youtube video automatically.It currently runs only on windows.

### Example
In this example we first import library, then we login with cookies, then we like a comment of video on youtube.
```sh
from youtube_auto_comment_liker import *
true=True;false=False
list_of_cookies=[
{
    "domain": ".youtube.com",
    "expirationDate": 1676431710.556339,
    "hostOnly": false,
    "httpOnly": false,
    "name": "__Secure-3PAPISID",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "ZyIV9eK7BkQoQ36b/AmdNVfNhZBCfBCbHV",
    "id": 1
}]
#please replace the above sample cookies with your cookies, can see below link of how to fetch cookies
youtube.login_cookie(cookies=list_of_cookies)
youtube.open("https://www.youtube.com/watch?v=C5duQyX7Gec")
youtube.keypress("pagedown") #scroll down to load comments
youtube.like_comment(comment='This planet belongs to all of us . Appreciate the work. Kudos to iamgurgaon citizens group.')
```

This module depends on the following python modules
* [requests](https://pypi.org/project/requests/)
* [bot_studio](https://pypi.org/project/bot_studio/)

#### BotStudio
[bot_studio](https://pypi.org/project/bot_studio/) is needed for browser automation. As soon as this library is imported in code, automated browser will open up. To like a comment first need to open the video url and then scroll the page to load comments. After that can call function like_comment to like the comment.

Complete documentation for YouTube Automation available [here](https://youtube-api.datakund.com/en/latest/)

### Installation

```sh
pip install youtube-auto-comment-liker
```

### Import
```sh
from youtube_auto_comment_liker import *
```

### Login with credentials
```sh
youtube.login(username="youtube username",password="youtube password")
```

### Login with cookies
```sh
youtube.login_cookie(cookies=list_of_cookies)
```

### Like Comment
```sh
youtube.like_comment(comment='comment text')
```

### Send Feedback to Developers
```sh
bot_studio.send_feedback(feedback="Need help with this ......")
```

### Cookies
To login with cookies [Edit this Cookie Extension](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?hl=en) can be added to browser. Please check [this](https://abhishek-chaudhary.medium.com/how-to-get-cookies-of-any-website-from-browser-22b3d6348ed2) link how to get cookies to login to your youtube.
### Contact Us
* [Telegram](https://t.me/datakund)
* [Website](https://datakund.com)

