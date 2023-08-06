Youtube-Video-Uploader-Bot is a python library to upload videos on youtube using browser automation. 
It currently runs only on windows.

### Example
In this example we first import library, then we login with cookies, then we upload video on youtube 
```sh
from youtube_video_uploader_bot import *
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
response=youtube.upload(title='Testing Upload ', video_path='C:/Users/video.mp4', kid_type='Yes, it's made for kids', description='I am just testing', type='Public')
videolink=response['body']['VideoLink']
```

This module depends on the following python modules
* [requests](https://pypi.org/project/requests/)
* [bot_studio](https://pypi.org/project/bot_studio/)

#### BotStudio
[bot_studio](https://pypi.org/project/bot_studio/) is needed for browser automation. As soon as this library is imported in code, automated browser will open up in which video will be uploaded. To upload first login will need to be done. Login can be done either with credentials or via cookies

Complete documentation for YouTube Automation available [here](https://youtube-api.datakund.com/en/latest/)

### Installation

```sh
pip install youtube-video-uploader-bot
```

### Import
```sh
from youtube_video_uploader_bot import *
```

### Login with credentials
```sh
youtube.login(username="youtube username",password="youtube password")
```

### Login with cookies
```sh
youtube.login_cookie(cookies=list_of_cookies)
```

### Upload
```sh
youtube.upload(title='title', video_path='video_path', kid_type='kid_type', description='description', type='type')
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

