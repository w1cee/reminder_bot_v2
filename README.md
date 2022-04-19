# python telegram bot for reminders
The bot will send a reminder to the group (for example, track the time).  
Access to the bot settings is allowed only to admins (admin id must be written in LIST_OF_ADMINS).
## how it works

> **main.py**
> > admin-panel
> > > The bot is configured directly through the chat with the bot:
> > > ![image](https://user-images.githubusercontent.com/93093228/163984995-43251a61-a3d7-4270-bd0b-fed0375e3bf1.png)
> > > ![image](https://user-images.githubusercontent.com/93093228/163985157-695e2c21-1d5f-40b7-b281-db58e0323a41.png)
>
> > reminder message  
> > > Using admin-commands [/add, /del, /settext]
> > > You can completely change the message that the bot should send to the group
> > > ![image](https://user-images.githubusercontent.com/93093228/163987018-3269ea16-7eae-4f34-911f-0c02b3a645b7.png)

> **config.json**
> > This file stores data for sending a message (list of users, status of the day, time of day and reminder text)
