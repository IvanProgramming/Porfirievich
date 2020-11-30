import json
import logging
from os import getenv

import aiohttp
import discord
from vbml import Pattern

TOKEN = getenv("DISCORD_TOKEN")

client = discord.Client()
gen_pattern = Pattern("+gen <start: str>")
gen_words_pattern = Pattern("+gen<quantity: int> <start: str>")

users = {}


def get_word_ending(n, is_verb=False):
    if n % 10 == 1 and n % 10 != 1:
        return "а"
    elif 5 > n % 10 > 0 and n % 10 != 1:
        return "ы"
    else:
        if is_verb:
            return "о"
        else:
            return ""


def get_answer_embed(user_id):
    answer_embed = discord.Embed()
    phrase_counter = users[user_id]["phrases_counter"]
    length = users[user_id]["length"]
    answer_embed.set_footer(text="{0} слов(а), сгеннерированн{1} {2} фраз{3}"
                            .format(length,
                                    get_word_ending(length),
                                    phrase_counter,
                                    get_word_ending(phrase_counter)))
    answer_embed.colour = discord.Color.blue()
    answer_embed.description = "{0} **{1}**".format(users[user_id]["phrase_begin"],
                                                    users[user_id]["replies"][users[user_id]["reply_index"]])

    return answer_embed


@client.event
async def on_ready():
    logging.log(logging.INFO, "Bot started!")
    print('bot started!')


@client.event
async def on_message(msg: discord.Message):
    usr_msg = msg.content.replace("\n", " ")

    if gen_pattern.parse(usr_msg):
        phrase_begin = gen_pattern.dict()["start"]
        data = await get_phrase(phrase_begin)
        users[msg.author.id] = {
            "replies": data["replies"],
            "user": msg.author,
            "length": 30,
            "reply_index": 0,
            "phrase_begin": phrase_begin,
            "phrases_counter": 1
        }
        reply = data['replies'][0]
        reply_msg: discord.Message = await msg.channel.send(embed=get_answer_embed(msg.author.id))
        users[msg.author.id]["msg"] = reply_msg
        await reply_msg.add_reaction("🔄")
    elif gen_words_pattern.parse(usr_msg):
        length, phrase_begin = gen_words_pattern.dict().values()
        data = await get_phrase(phrase_begin, length)
        users[msg.author.id] = {
            "replies": data["replies"],
            "user": msg.author,
            "length": int(length),
            "reply_index": 0,
            "phrase_begin": phrase_begin,
            "phrases_counter": 1
        }
        reply = data['replies'][0]
        reply_msg: discord.Message = await msg.channel.send(embed=get_answer_embed(msg.author.id))
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
        users[user_id]["phrases_counter"] += 1
        await users[user_id]["msg"].edit(embed=get_answer_embed(user_id))
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
