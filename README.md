# SCP-5170
### Pattern Screamer

## Project Structure
```
╭─ scp
├──── core / clients - filters - functions
├─────── # core files
├──── database
├─────── # a cache memory database
├──── plugins / bot - private - user
├─────── # the plugins directory
├──── utils
╰─────── # few helper scripts laying around for plugins
```

### Requirements
 - a brain
 - python==3.9.2

### Setup
 - clone this repository with `git clone` with `--recursive` flag and change directory to the root of the project
 - this project only works on python 3.9.2. I suggest using pyenv on unix or pyenv-win on windows to install version 3.9.2
 - create a `venv` with `python -m venv venv` and activate the `venv`
 - install all modules in requirements with `python -m pip install -r requirements.txt` and `python -m pip install -r session/requirements.txt`
 - move config sample from `config.ini.sample` to `config.ini` and fill in the configs
  ```
  [pyrogram]
  api_id = API_ID from my.telegram.org
  api_hash = API_HASH from my.telegram.org
  test_mode = 0

  [scp-5170]
  sudolist = List of users you want to have to control your userbot (seperated by spaces)
  prefixes = Command Trigger prefixes (seperated by spaces)
  logchannel = a channel you create with your bot and user inside it as administrator
  ignoregroups = IDs of groups you want to disable bot from working (seperated by spaces)
  plugins = Plugins directories (seperated by spaces)
  ```
 - create session for user and bot
   - user: `python -m session -s scp-user`
   - bot : `python -m session -s scp-bot -t {bot_token}`
 - all done. run the userbot with `hy -m scp`

### Creating own modules
as you know SCP-5170 is using a Customized Client around Pyrogram library.
therefore a plugin can be very simple to make and import into `scp/plugins/private` directory:
```
scp.bot - The Bot Client
scp.user - The User Client
```

 - an Example plugin the echo to a command with `(*prefix)hello`:

#### python
```
from scp import user

@user.on_message(
    user.filters.sudo
    & user.filters.command('hello')
)
async def _(_, message: types.Message):
    return await message.reply('hello')
```

#### hy
```
(import [scp[user]])

(with-decorator (
    user.on_message (user.filters.command "hello"))
    (defn/a _ [_ message]
        (return (await (message.reply "hello")))))
```
or
```
(import [scp[user]])

(defn/a echo-hello [_ message]
    (return (await (message.reply "hello"))))


(user.add_handler
    :handler (user.handlers.MessageHandler
    :callback echo-hello
    :filters (& user.filters.me (bot.filters.command "hello" :prefixes "/") bot.filters.private)))
```

### FAQ
- why given that name?
  the name speaks to itself, `the Pattern Screamer`

- will there ever be a Heroku or Fly.io support...?
  just use localhost, trust me.

- Why does it look like kantek?
  i always loved it, therefore i did add KanteX to globally use in this userbot

### Special thancc
 - [hylang](https://hylang.org) - hy team <3
 - [Dan](https://github.com/delivrance) - pyrogram
 - [Fluffy Shark](https://github.com/ColinShark) - QR Code session generator Script
 - [Kneesocks](https://github.com/the-blank-x) - 13 year old with multiple police records (also eval module is originally by him)
 - [Davide Goggles](https://github.com/DavideGalilei) - spam check and automatic logging with extra pineapple toppings

and everyone who built awesome modules that are being used by this project
