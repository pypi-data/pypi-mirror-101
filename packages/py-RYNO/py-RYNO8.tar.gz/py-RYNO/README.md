# py-RYNO Library
A stable userbot base library, based on Telethon.

## Installation
`pip install py-RYNO`

## Usage
=> Create folders named `plugins`, `addons`, `assistant` and `resources`.<br/>
=> Add your plugins in the `plugins` folder and others accordingly.<br/>
=> Create a `.env` file with `API_ID`, `API_HASH`, `SESSION`, 
`BOT_TOKEN`, `BOT_USERNAME`, `REDIS_URI`, `REDIS_PASSWORD` & 
`LOG_CHANNEL` as mandatory environment variables. Check
[`.env.sample`](https://github.com/RYNO/RYNO-X/.env.sample) for more details.<br/>
=> Run `python -m py-RYNO` to start the bot.<br/>

### Creating plugins
To work everywhere

```python
@ultroid_cmd(
    pattern="start",
)   
async def _(e):   
    await eor(e, "RYNO Started")   
```

To work only in groups

```python
@ultroid_cmd(
    pattern="start",
    groups_only=True,
)   
async def _(e):   
    await eor(e, "RYNO Started")   
```

Assistant Plugins 👇

```python
@asst_cmd("start")   
async def _(e):   
    await e.reply("RYNO Started")   
```

Made with 💕 by [@OFFICIALRYNO](https://t.me/OFFICIALRYNO). <br />

# Credits
* [Lonami](https://github.com/LonamiWebs/) for [Telethon](https://github.com/LonamiWebs/Telethon)
