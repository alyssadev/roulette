roulette
========

a hacky weird twitch roulette, cos the famous one is down for some reason

setup
-----

* go to https://www.twitch.tv/directory/all?sort=VIEWER_COUNT_ASC
* open network tools, hit refresh
* look for a gql xhr with operationName: `BrowsePage_Popular`
* from that request, get the Client-Id header, note that down as `TWITCH_OAUTH_ID`, then get the token from the end of the Authorization header, note that down as `TWITCH_OAUTH_SECRET`
* go to Heroku, make an account, make an app, link this github repo, or your own fork if you want
* under Settings, click Reveal Config Vars, then add the two variables you noted down earlier
* If you're not using heroku (maybe digitalocean or something idk), make sure you set the PORT environment variable as well to whatever you need. heroku sets this themselves
* It should Just Work:tm:
