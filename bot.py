import discord
import youtube_dl
from discord.ext import commands
from discord.ext.commands import Bot
import os

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
	print('Я готов')

@bot.event
async def on_disconnect( ):
	print('Сервер упал')
@bot.command()
async def test(ctx):
	m = await ctx.send("dsa")
	await m.add_reaction("👍")
	print(str(ctx))
	print(m)


@bot.command(help='This command plays songs')
async def test1(ctx):
	print("dsa")

@bot.command()
async def clear(ctx, amount = 999):
	await ctx.channel.purge(limit=amount+1)


@bot.event
async def on_raw_reaction_add(payload):
	if str(payload.emoji.name)=="👍":
		print("dsa")


# @bot.command()
# async def play(ctx, url : str):
# 	print (ctx.guild.Members)

@bot.event
async def on_member_remove(member):
	for categories_member in member.guild.categories:
		if str(categories_member)==str(f'канал {member.display_name}'):
			for delete_channel in categories_member.channels:await delete_channel.delete() 
			await categories_member.delete()
			return 0

@bot.event
async def on_voice_state_update(member,before,after):

	####    ЗАПРОСЫ 	####
	channel_check_text = discord.utils.get(member.guild.text_channels, name=f'канал-{member.display_name}')
	check_categories= discord.utils.get(member.guild.categories, name=f'канал {member.display_name}')

	overwrites_text = {
	member.guild.default_role: discord.PermissionOverwrite(read_messages=True,manage_channels=True,manage_permissions=True),
	member: discord.PermissionOverwrite(manage_channels=False,manage_permissions=False,send_messages=True,read_message_history=True,use_voice_activation=True)
	}
	overwrites_voice = {
	member.guild.default_role: discord.PermissionOverwrite(read_messages=True,manage_channels=True,manage_permissions=True,move_members=True,mute_members=True,deafen_members=True),
	member: discord.PermissionOverwrite(manage_channels=False,manage_permissions=False,send_messages=True,read_message_history=True,use_voice_activation=True,move_members=False,mute_members=False,deafen_members=False)
	}
	overwrites_category1 = {
	member.guild.default_role: discord.PermissionOverwrite(read_messages=False,manage_channels=False,manage_permissions=False),
	member: discord.PermissionOverwrite(read_messages=False)
	}



	if after.channel!=None and (after.channel.name=="Delete" or after.channel.name=="Create"):


		###### ЕСЛИ ЕСТЬ АКТИВАЦИЯ ПО КНОПКЕ ######
		for channel123 in after.channel.permissions_for(member):
			if str(channel123)=="('use_voice_activation', True)":


				###### ЕСЛИ Create ######

				if after.channel.name=="Create" and check_categories==None:

					category1 = await member.guild.create_category_channel(name=f'канал {member.display_name}',overwrites=overwrites_category1)
					channel_voice = await category1.create_voice_channel(name=f'канал {member.display_name}',overwrites=overwrites_voice)

					await member.move_to(channel_voice)
					channel_text = await category1.create_text_channel(name=f'канал {member.display_name}',overwrites=overwrites_text)


				###### ЕСЛИ Delete ######

				if str(channel_check_text)==str(f'канал-{member.display_name}') and after.channel.name=="Delete":
					for delete_channel in check_categories.channels:
						await delete_channel.delete()
					await check_categories.delete()				
		




					



		

bot.run('TOKEN')