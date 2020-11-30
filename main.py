from os import getenv

import discord
import logging
import aiohttp
import json
from vbml import Pattern

TOKEN = getenv("DISCORD_TOKEN")

client = discord.Client()
gen_pattern = Pattern("+gen <start: str>")
gen_words_pattern = Pattern("+gen<quantity: int> <start: str>")

users = {}


@client.event
async def on_ready():
    logging.log(logging.INFO, "Bot started!")
    print('bot started!')


@client.event
async def on_message(msg: discord.Message):
    if gen_pattern.parse(msg.content):
        phrase_begin = gen_pattern.dict()["start"]
        data = await get_phrase(phrase_begin)
        users[msg.author.id] = {
            "replies": data["replies"],
            "user": msg.author,
            "length": 30,
            "reply_index": 0,
            "phrase_begin": phrase_begin
        }
        reply = data['replies'][0]
        reply_msg: discord.Message = await msg.channel.send(
            embed=discord.Embed(description=f"{phrase_begin}**{reply}**", color=discord.Color.blue()))
        users[msg.author.id]["msg"] = reply_msg
        await reply_msg.add_reaction("🔄")
    elif gen_words_pattern.parse(msg.content):
        length, phrase_begin = gen_words_pattern.dict().values()
        data = await get_phrase(phrase_begin, length)
        users[msg.author.id] = {
            "replies": data["replies"],
            "user": msg.author,
            "length": length,
            "reply_index": 0,
            "phrase_begin": phrase_begin
        }
        reply = data['replies'][0]
        reply_msg: discord.Message = await msg.channel.send(
            embed=discord.Embed(description=f"{phrase_begin}**{reply}**", color=discord.Color.blue()))
        users[msg.author.id]["msg"] = reply_msg
        await reply_msg.add_reaction("🔄")


@client.event
async def on_raw_reaction_add(reaction_raw: discord.RawReactionActionEvent):
    await handle_emoji_click(reaction_raw)


@client.event
async def on_raw_reaction_remove(reaction_raw):
    await handle_emoji_click(reaction_raw)


async def handle_emoji_click(reaction_raw):
    if reaction_raw.user_id in users:
        if users[reaction_raw.user_id]["msg"].id == reaction_raw.message_id:
            if str(reaction_raw.emoji) == "🔄":
                await update_reply(reaction_raw.user_id)


async def update_reply(user_id):
    if users[user_id]["reply_index"] < 2:
        users[user_id]["reply_index"] += 1
        phrase_begin = users[user_id]["phrase_begin"]
        reply = users[user_id]["replies"][users[user_id]["reply_index"]]
        await users[user_id]["msg"].edit(
            embed=discord.Embed(description=f"{phrase_begin}**{reply}**", color=discord.Color.blue())
        )
    else:
        users[user_id]["reply_index"] = -1
        users[user_id]["replies"] = (await get_phrase(users[user_id]["phrase_begin"], users[user_id]["length"]))[
            "replies"]
        await update_reply(user_id)


async def get_phrase(begin, words_quantity=30):
    session = aiohttp.ClientSession()
    request = await session.post("https://pelevin.gpt.dobro.ai/generate/", json={"prompt": begin,
                                                                                 "length": words_quantity},
                                 headers={
                                     "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 "
                                                   "(KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 RuxitSynthetic"
                                                   "/1.0 v2820781040184328804 t4157550440124640339"})
    data = json.loads(await request.text())
    await session.close()
    return data


client.run(TOKEN)

