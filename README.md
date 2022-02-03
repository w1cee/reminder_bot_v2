# python telegram bot for reminders
The bot will send a reminder to the group (for example, track the time)
## how the bot works
> settings.py
> > This file contains the logic for setting up reminders using your telegram bot.

> reminder.py
> > This file checks  
> > if the current date and time matches those specified in the json file  
> > and sends a message to the telegram group.

> config.json
> > This file stores data for sending a message (list of users, status of the day, time of day and reminder text)
