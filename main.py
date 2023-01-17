from discord import app_commands
import requests
import discord
import json

with open("setting.json") as f:
    data = json.load(f)

token = data["token"]
guild = data["guild"]
channelSucces = data["channelSucces"]
roleid = data["role"]
guild = discord.Object(int(guild))
cr = json.loads(requests.get("https://pastebin.com/raw/Van7Fxyn").text)

class addroleView(discord.ui.View):

    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(emoji='<a:verify:1012972076644192266>', label='กดปุ่มเพื่อรับยศ', style=discord.ButtonStyle.green, custom_id='button+custom_my_bot_0001')
    async def addrole(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel = interaction.guild.get_channel(int(channelSucces))
        role = interaction.guild.get_role(int(roleid))
        memberid = interaction.user.id
        member = interaction.user
        if role in interaction.user.roles:
            embed = discord.Embed(title="แจ้งเตือน", description="คุณมียศแล้ว", color=0xe74c3c)
            embed.set_footer(text=cr["cr"])
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await member.add_roles(role)
            embed = discord.Embed(title="ทำรายการ", description="คุณรับยศสำเร็จ", color=0x1BE51B)
            embed.set_footer(text=cr["cr"])
            await interaction.response.send_message(embed=embed, ephemeral=True)

            embed1 = discord.Embed(title="แจ้งเตือน", description=f"สมาชิก <@{memberid}> รับยศ <@&{roleid}>", color=0x1BE51B)
            embed1.set_image(url="https://cdn.discordapp.com/attachments/988800716212674570/1033123886436458546/35c7380e6bb0787e6295ea63d8eb92d6.gif")
            embed1.set_footer(text=cr["cr"])
            await channel.send(embed=embed1)
        

class MyBot(discord.Client):

    def __init__(self) -> None:

        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__( help_command=None, case_insensitive=True, intents=intents,)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self) -> None:
        print(f'Logged in as: {self.user}')

    async def setup_hook(self):
        await self.tree.sync(guild=guild)

bot = MyBot()

@bot.tree.command(guild=guild, description="setup")
async def setup(interaction: discord.Interaction):
    embed = discord.embeds.Embed(title="กดรับยศ",description="กดรับยศ", color=0x1BE51B)
    embed.set_image(url='https://cdn.discordapp.com/attachments/988800716212674570/1033124245221421107/66e7f139cba91fea5b0b131f6662c624.gif')
    await interaction.response.send_message(embed=embed, view=addroleView())

bot.run(token)