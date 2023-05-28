# ReminderBot

ReminderBot is a versatile bot designed to send reminders to a group at specified times on any day of the week. This bot
is built to help users stay organized and never miss an important task or event.

## Features

- **Flexible Scheduling**: ReminderBot allows you to schedule reminders at any time and on any day of the week. Whether
  it's a one-time reminder or a recurring event, this bot has got you covered.
- **Group Notifications**: You can configure ReminderBot to send reminders to a specific group or channel. This ensures
  that everyone in the group receives the necessary reminders and stays updated.
- **Timezone Support**: ReminderBot takes into account different time zones, allowing you to set reminders based on the
  local time of each group member.
- **Customizable Messages**: You have the freedom to customize the content of your reminders. Include important details,
  instructions, or any other relevant information to make sure everyone is well-informed.
- **Language Selection**: ReminderBot supports multiple languages, allowing you to choose the language that suits your
  group's preferences. You can easily switch between available languages using a simple command.
- **Custom Language Support**: In addition to the provided languages, ReminderBot enables you to add your own language
  translations. This feature ensures that the bot can adapt to your specific language requirements and improve
  communication within your group.

## Getting Started

To add ReminderBot to your group, follow these simple steps:

1. Add your @username to admin list in config.json
2. Create your own bot with @BotFather and set your token in bot_config.py
3. Invite your ReminderBot to your desired group.
4. Once added, you can configure the bot by sending it commands in the private messages.
5. Specify the time and day of the week when you want the reminder to be sent using commands `/day_on` `/day_off`
   and `/set_time`
6. Customize the content of your reminder by using `/set_text` command
7. ReminderBot will confirm the scheduling and start sending reminders according to your instructions.

## Usage

Here are some example commands you can use with ReminderBot:

### Commands for everyone

- `/view`: This command allows you to see current reminder text, list of users to mention, day statuses and time. Admins
  receive additional information, such as group ID and time zone, in a separate message.
- `/help`: Use this command to get instructions on how to use ReminderBot effectively.

### Commands admins

- `/set_text`: With this command, you can customize the text and language settings of ReminderBot to fit the preferences
  of your group.
- `/day_on`: Use this command to enable reminders for a specific day of the week.
- `/day_off`: This command disables reminders for a specific day of the week.
- `/set_time`: Use this command to set the time for reminders for a specific day.
- `/add`: This command adds a user's username (@username) to the mention list, ensuring they receive reminders.
- `/del`: Use this command to remove a user's username (@username) from the notification list, stopping them from
  receiving reminders.
- `/add_admin`: This command adds an administrator.
- `/del_admin`: This command deletes an administrator. Admin can't delete himself, and can't delete everyone but
  himself, there will always be two admins.
- `/change_group`: This command allows you to change the group where ReminderBot sends reminders.
- `/set_lang`: Use this command to change the language of ReminderBot's messages and responses.
- `/change_timezone`: This command allows you to change the time zone so that your reminders are always on time.

### Add new languages
To add new languages you need to put *.json file into the lang folder, 