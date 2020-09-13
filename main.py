import requests
import discord
from discord.ext import commands
import json
from datetime import date
import io

bot_config = json.loads(open("config.json", "r").read())
client = commands.Bot(command_prefix=bot_config["bot_prefix"])


async def on_ready():
    print("Bot is ready")


@client.command(pass_context=True)
async def ping(ctx):
    today = date.today()
    embed = discord.Embed(title=bot_config["bot_name"], description="", color=0x1E68F4)
    embed.add_field(name="Success", value="Pong `" + str(round(client.latency * 1000)) + "`ms", inline=False)
    embed.set_footer(text=bot_config["bot_name"] + " | " + str(
        today.strftime("%m") + "/" + today.strftime("%d") + "/" + today.strftime("%y")))
    await ctx.send(embed=embed)


@client.command(pass_context=True)
async def obfuscate(ctx, *args):
    today = date.today()
    # await client.delete_message(ctx.message)

    try:
        attachment_url = ctx.message.attachments[0].url
        script_to_obfuscate = str(requests.get(attachment_url).text)
    except:
        script_to_obfuscate = "none"

    if script_to_obfuscate == "none":
        embed = discord.Embed(title=bot_config["bot_name"], description="", color=0xFF0000)
        embed.add_field(name="Error", value="`Error occured! {Please upload the .txt/.lua file.}`", inline=False)
        embed.set_footer(text=bot_config["bot_name"] + " | " + str(
            today.strftime("%m") + "/" + today.strftime("%d") + "/" + today.strftime("%y")))
        await ctx.send(embed=embed)
    else:
        values = {}
        for x in args:
            if x.lower() == "encstrall" or x.lower() == "encall":
                x = "EncryptStrings"
            elif x.lower() == "encstrimp" or x.lower() == "encimp":
                x = "EncryptImportantStrings"
            elif x.lower() == "preslineinfo":
                x = "PreserveLineInfo"
            elif x.lower() == "memes" or x.lower() == "addmemes":
                x = "AddMemes"
            elif x.lower() == "uglify":
                x = "Uglify"

            if "customvar:" in x:
                x = x.replace("customvar:", "")
                values["CustomVarName"] = x
            else:
                values[x] = "on"

        obfuscated_script = str(
            requests.post("https://obfuscator.aztupscripts.xyz/Obfuscate", files={"Input": str(script_to_obfuscate)},
                          data=values).text)
        if obfuscated_script != "The file weren't able to be found !" and obfuscated_script != script_to_obfuscate:
            d1 = str(today.strftime("%m") + "_" + today.strftime("%d") + "_" + today.strftime("%y"))
            f = io.StringIO(obfuscated_script)
            await ctx.channel.send(content="> `تم التشفير بنجاح`",
                                   file=discord.File(f, d1 + "_obfuscated" + ".lua"))

        else:
            embed = discord.Embed(title=bot_config["bot_name"], description="", color=0xFF0000)
            embed.add_field(name="Error", value="`Syntax Error.`", inline=False)
            embed.set_footer(text=bot_config["bot_name"] + " | " + str(
                today.strftime("%m") + "/" + today.strftime("%d") + "/" + today.strftime("%y")))
            await ctx.send(embed=embed)


client.run(bot_config["bot_token"])
