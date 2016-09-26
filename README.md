Gifbot
========

Gifbot is a Facebook Messenger Bot that sends you a GIF everytime you send it a message.
Built using Flask.


<kbd>[![Gifbot View](gifbotdemo.gif)](http://m.me/sendmeagif)</kbd>


## Demo

[m.me/sendmeagif](http://m.me/sendmeagif)

## Facebook Page

[fb.com/sendmeagif](https://www.facebook.com/sendmeagif/)

## Running the bot

Messenger bots uses a web server to process messages it receives or to figure out what messages to send. You also need to have the bot be authenticated to speak with the web server and the bot approved by Facebook to speak with the public.

Create a file called `config.py` that looks like `config_example.py`. Fill in the necessary values.

### *Build the server using heroku*

```
git init
git add .
git commit --message 'hello world'
heroku create
git push heroku master
```

To learn more on how to setup the Facebook page and setup the bot refer to [messenger tutorial](https://github.com/jw84/messenger-bot-tutorial).

**Powered by Giphy**