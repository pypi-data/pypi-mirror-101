#imports
import BenBotAsync
import aiohttp
import FortniteAPIAsync
import sanic
import discord
from sanic import Sanic
from sanic import response
import colorama
from colorama import Fore, Back, Style, init
import crayons
import os
import asyncio
import requests
import fortnitepy
import aioconsole
from typing import Optional	
from threading import Thread
from functools import partial
import json
from fortnitepy.ext import commands
from fortnitepy.ext import commands as fortnite_commands
from discord.ext import commands as discord_commands
#definitions
sanic_app = Sanic("NeoBotNet")
filename = "device_auths.json"
loop = asyncio.get_event_loop()
currentpatch = "0.0.2"
pirxcy = requests.get("https://cdn.pirxcy.xyz/network")
patch = pirxcy.json()["version"]
logs = pirxcy.json()["logs"]
fortnitestat = requests.get("https://benbotfn.tk/api/v1/status")
fortnitepatch = fortnitestat.json()["currentFortniteVersion"]



async def keep_alive():
		url = f'https://{os.getenv("REPL_SLUG")}--{os.getenv("REPL_OWNER")}.repl.co'
		url2 = f'https://{os.getenv("REPL_SLUG")}.{os.getenv("REPL_OWNER")}.repl.co'
		r = requests.post('https://pinger.pirxcy.xyz/api/add', json={'url': url})
		r2 = requests.post('https://pinger.pirxcy.xyz/api/add', json={'url': url2})
		print(r.status_code, r.reason)
		print(r2.status_code, r2.reason)
		while True:
			print(f'Pinged {url} and {url2} Via NeoBot Using keep_alive!')
			await asyncio.sleep(300)


with open('config.json') as f:
	try:
		data = json.load(f)
	except json.decoder.JSONDecodeError as e:
		print('Error Loading File: config.json')
		print(e)
		exit(1)

def getNewSkins():
	r = requests.get('https://benbotfn.tk/api/v1/files/added')

	response = r.json()

	cids = []

	for cid in [item for item in response if item.split('/')[-1].upper().startswith('CID_')]:
		cids.append(cid.split('/')[-1].split('.')[0])
	
	return cids

def getNewEmotes():
	r = requests.get('https://benbotfn.tk/api/v1/files/added')

	response = r.json()

	eids = []

	for cid in [item for item in response if item.split('/')[-1].upper().startswith('EID_')]:
		eids.append(cid.split('/')[-1].split('.')[0])
	
	return eids

def get_device_auth_details():
	if os.path.isfile(filename):
		with open(filename, 'r') as fp:
			return json.load(fp)
	return {}

def store_device_auth_details(Email, details):
	existing = get_device_auth_details()
	existing[Email] = details


	with open(filename, 'w') as fp:
		json.dump(existing, fp)

def perms():
	async def predicate(ctx):
		return ctx.author.display_name in data['AdminPerms']
	return commands.check(predicate)

async def get_authorization_code():
	while True:
		response = await aioconsole.ainput("Go to https://rebrand.ly/authcode sign in with "  + data['email'] + " and paste everything!\n")
		if "redirectUrl" in response:
			response = json.loads(response)
			if "?code" not in response["redirectUrl"]:
				print("Invalid response.")
				continue
			code = response["redirectUrl"].split("?code=")[1]
			return code
		else:
			if "https://accounts.epicgames.com/fnauth" in response:
				if "?code" not in response:
					print("Incorrect Code!")
					continue
				code = response.split("?code=")[1]
				return code
			else:
				code = response
				return code

device_auth_details = get_device_auth_details().get(data['email'], {})
fortnite_bot  = fortnite_commands.Bot(
	command_prefix=data['prefix'],case_insensitive=True,
	auth=fortnitepy.AdvancedAuth(
		Email=data['email'],
		prompt_authorization_code=True,
		delete_existing_device_auths=True,
		authorization_code=get_authorization_code,
		 **device_auth_details
	),
	status='Made By Pirxcy and Quax',
	platform=fortnitepy.Platform("XBL"),
)
T = data['prefix']

discord_bot = discord_commands.Bot(
		command_prefix="!help",
		description="My Current",
		case_insensitive=True
	)


fortnite_bot.outfitchange_sentembed = False
fortnite_bot.msg = None


@fortnite_bot.event
async def event_device_auth_generate(details, email):
	store_device_auth_details(email, details)

@fortnite_bot.event
async def event_party_member_join(member):
				embed=discord.Embed(title=f"{fortnite_bot.user.display_name} Launched!", description=f"Watching {fortnite_bot.user.display_name}")
				embed.set_thumbnail(url=f"https://benbotfn.tk/cdn/images/{fortnite_bot.party.me.outfit}/icon.png")
				embed.add_field(name="Party", value=f"{fortnite_bot.party.member_count} / {fortnite_bot.party.max_size}", inline=True)
				embed.add_field(name="Friends", value=f"{len(fortnite_bot.friends)}", inline=True)
				embed.add_field(name="Fortnite Version", value=f"{fortnitepatch}", inline=True)
				embed.add_field(name="Bot Version", value=f"{patch}\nPowered By PirxcyAPI", inline=True)
				embed.set_footer(text="Made By Pirxcy and Quax!")

				if not fortnite_bot.msg:
					channel = discord_bot.get_channel(819830100102348811)
					fortnite_bot.msg = await channel.send(embed=embed)

				await fortnite_bot.msg.edit(embed=embed)

@fortnite_bot.event
async def event_before_close():
				embed=discord.Embed(title=f"{fortnite_bot.user.display_name} Launched!", description=f"Watching {fortnite_bot.user.display_name}")
				embed.set_thumbnail(url=f"https://benbotfn.tk/cdn/images/{fortnite_bot.party.me.outfit}/icon.png")
				embed.add_field(name="Party", value=f"{fortnite_bot.party.member_count} / {fortnite_bot.party.max_size}", inline=True)
				embed.add_field(name="Friends", value=f"{len(fortnite_bot.friends)}", inline=True)
				embed.add_field(name="Fortnite Version", value=f"{fortnitepatch}", inline=True)
				embed.add_field(name="Bot Version", value=f"{patch}\nPowered By PirxcyAPI", inline=True)
				embed.set_footer(text="Made By Pirxcy and Quax!")

				if not fortnite_bot.msg:
					channel = discord_bot.get_channel(819830100102348811)
					fortnite_bot.msg = await channel.send(embed=embed)

				await fortnite_bot.msg.edit(embed=embed)

@fortnite_bot.event
async def event_party_member_leave(member):
				embed=discord.Embed(title=f"{fortnite_bot.user.display_name} Launched!", description=f"Watching {fortnite_bot.user.display_name}")
				embed.set_thumbnail(url=f"https://benbotfn.tk/cdn/images/{fortnite_bot.party.me.outfit}/icon.png")
				embed.add_field(name="Party", value=f"{fortnite_bot.party.member_count} / {fortnite_bot.party.max_size}", inline=True)
				embed.add_field(name="Friends", value=f"{len(fortnite_bot.friends)}", inline=True)
				embed.add_field(name="Fortnite Version", value=f"{fortnitepatch}", inline=True)
				embed.add_field(name="Bot Version", value=f"{patch}\nPowered By PirxcyAPI", inline=True)
				embed.set_footer(text="Made By Pirxcy and Quax!")

				if not fortnite_bot.msg:
					channel = discord_bot.get_channel(819830100102348811)
					fortnite_bot.msg = await channel.send(embed=embed)

				await fortnite_bot.msg.edit(embed=embed)



@fortnite_bot.event
async def event_ready():
	startskin = requests.get(f'https://fortnite-api.com/v2/cosmetics/br/search?name={data["Skin"]}').json()['data']
	startemote = requests.get(f'https://fortnite-api.com/v2/cosmetics/br/search?name={data["Backbling"]}').json()['data']
	startbackpack = requests.get(f'https://fortnite-api.com/v2/cosmetics/br/search?name={data["Emote"]}').json()['data']
	member = fortnite_bot.party.me
	#os.system('cls||clear')
	print('Connecting To Server (via sanic)')
	loop.create_task(sanic_app.create_server(host="0.0.0.0",port=8080,return_asyncio_server=True, access_log=False))
	#os.system('cls||clear')
	print(f'Connected To {fortnite_bot.user.display_name} Using Sanic')
	embed=discord.Embed(title=f"{fortnite_bot.user.display_name} Launched!", description=f"Watching {fortnite_bot.user.display_name}")
	embed.set_thumbnail(url=f"https://benbotfn.tk/cdn/images/{fortnite_bot.party.me.outfit}/icon.png")
	embed.add_field(name="Party", value=f"{fortnite_bot.party.member_count} / {fortnite_bot.party.max_size}", inline=True)
	embed.add_field(name="Friends", value=f"{len(fortnite_bot.friends)}", inline=True)
	embed.add_field(name="Fortnite Version", value=f"{fortnitepatch}", inline=True)
	embed.add_field(name="Bot Version", value=f"{patch}\nPowered By PirxcyAPI", inline=True)
	embed.set_footer(text="Made By Pirxcy and Quax!")

	channel = discord_bot.get_channel(819830100102348811)
	fortnite_bot.msg = await channel.send(embed=embed)

	await member.edit_and_keep(
	partial(
			fortnitepy.ClientPartyMember.set_outfit,
			asset=startskin['id']
	),
	partial(
			fortnitepy.ClientPartyMember.set_emote,
			asset=startemote['id']
	),
	partial(
			fortnitepy.ClientPartyMember.set_backpack,
			asset=startbackpack['id']
	),
	partial(
			fortnitepy.ClientPartyMember.set_pickaxe,
			asset="Pickaxe_ID_111_BlackWidow"
	),
	partial(
			fortnitepy.ClientPartyMember.set_banner,
			icon="influencerbanner57",
			color="black",
			season_level="999"
	),
	partial(
			fortnitepy.ClientPartyMember.set_battlepass_info,
			has_purchased=True,
			level="999"
		
	)
)
  

@fortnite_bot.event
async def event_party_member_outfit_change(member, before, after):
				embed=discord.Embed(title=f"{fortnite_bot.user.display_name} Launched!", description=f"Watching {fortnite_bot.user.display_name}")
				embed.set_thumbnail(url=f"https://benbotfn.tk/cdn/images/{fortnite_bot.party.me.outfit}/icon.png")
				embed.add_field(name="Party", value=f"{fortnite_bot.party.member_count} / {fortnite_bot.party.max_size}", inline=True)
				embed.add_field(name="Friends", value=f"{len(fortnite_bot.friends)}", inline=True)
				embed.add_field(name="Fortnite Version", value=f"{fortnitepatch}", inline=True)
				embed.add_field(name="Bot Version", value=f"{patch}\nPowered By PirxcyAPI", inline=True)
				embed.set_footer(text="Made By Pirxcy and Quax!")

				if not fortnite_bot.msg:
					channel = discord_bot.get_channel(819830100102348811)
					fortnite_bot.msg = await channel.send(embed=embed)

				await fortnite_bot.msg.edit(embed=embed)

@discord_bot.event
async def on_ready():
		print(f'Connected {os.getenv("REPL_OWNER")} To NeoBot!')
		print(f'Pinged https://{os.getenv("REPL_SLUG")}--{os.getenv("REPL_OWNER")}.repl.co Via NeoBot')

@sanic_app.route('/friends/list', methods=['GET'])
async def friendcountv2(request):
	friends = [friend.display_name for friend in fortnite_bot.friends]
	return sanic.response.json(friends)            

@sanic_app.route('/friends/count', methods=['GET'])
async def friendcount(request):
	friends = len(fortnite_bot.friends)
	return sanic.response.json(friends)             

@sanic_app.route('/')
def index(request):
		return response.html(
			f'<img src="https://benbotfn.tk/cdn/images/{fortnite_bot.party.me.outfit}/icon.png" alt="Current Skin">\n<b>Watching {fortnite_bot.user.display_name}<b>')

@fortnite_bot.event
async def event_friend_add(Friend):
	await Friend.invite()
	

@fortnite_bot.event
async def event_party_invite(invite):
	if data['AcceptInvite'] == 'true'.lower():
		try:
			await invite.accept()
			print(f'Accepted party invite from {invite.sender.display_name}', 'blue')
		except Exception:
			pass
	elif data['AcceptInvite'].lower() == 'false':
		if invite.sender.display_name in data['AdminPerms']:
			await invite.accept()
			print(f'Accepted party invite from {invite.sender.display_name}', 'blue')
		else:
			print(f'Never accepted party invite from {invite.sender.display_name}', 'red')

def lenFriends():
	friends = fortnite_bot.friends
	return len(friends)

def lenPartyMembers():
	members = fortnite_bot.party.members
	return len(members)
	
@fortnite_bot.event
async def event_friend_request(request):
	if data['FriendAccept'].lower() == 'true':
		try:
			await request.accept()
			print(f'Accepted friend request from {request.display_name}' + f' ({lenFriends()}')
		
		except Exception as e:
			print(str(e))
		
	else:
			print(f'Never accepted friend request from {request.display_name}', 'red')
						
@fortnite_bot.event
async def event_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.send('That is not a command. Try !help')
	elif isinstance(error, IndexError):
		pass
	elif isinstance(error, fortnitepy.HTTPException):
		pass
	elif isinstance(error, commands.CheckFailure):
		await ctx.send("You don't have access to that command.")
	elif isinstance(error, TimeoutError):
		await ctx.send("You took too long to respond!")
	else:
		print(error)

@fortnite_bot.command()
async def hello(ctx):
	await ctx.send('Hello!')

async def set_and_update_party_prop(schema_key: str, new_value: str):
	prop = {schema_key: fortnite_bot.party.me.meta.set_prop(schema_key, new_value)}
	await fortnite_bot.party.patch(updated=prop)

@fortnite_bot.command()
@perms()
async def unhide(ctx, *, epic_username: Optional[str] = None) -> None:
	if epic_username is None:
		user = await fortnite_bot.fetch_user(ctx.author.display_name)
		member = fortnite_bot.party.get_member(user.display_name)
	else:
		user = await fortnite_bot.fetch_user(epic_username)
		member = fortnite_bot.party.get_member(user.display_name)

	if member is None:
		await ctx.send("Failed to find that user, are you sure they're in the party?")
	else:
		try:
			await member.promote()
			await ctx.send("unhid everyone")
		except fortnitepy.errors.Forbidden:
			await ctx.send("i found unhide report in server.")
			print(crayons.red("Failed to unhide members as I don't have the required permissions."))


@fortnite_bot.command()
async def emote(ctx, *, content = None):
	if content is None:
		await ctx.send(f'No emote was given, try: {T}emote (emote name)')
	elif content.lower() == 'floss':
		await fortnite_bot.party.me.clear_emote()
		await fortnite_bot.party.me.set_emote(asset='EID_Floss')
		await ctx.send('Emote set to: Floss')
	elif content.lower() == 'none':
		await fortnite_bot.party.me.clear_emote()
		await ctx.send('Emote set to: None')
	elif content.upper().startswith('EID_'):
		await fortnite_bot.party.me.clear_emote()
		await fortnite_bot.party.me.set_emote(asset=content.upper())
		await ctx.send(f'Emote set to: {content}')
	else:
		try:
			cosmetic = await BenBotAsync.get_cosmetic(
				lang="en",
				searchLang="en",
				matchMethod="contains",
				name=content,
				backendType="AthenaDance"
			)
			await fortnite_bot.party.me.clear_emote()
			await fortnite_bot.party.me.set_emote(asset=cosmetic.id)
			await ctx.send(f'Emote set to: {cosmetic.name}')
		except BenBotAsync.exceptions.NotFound:
			await ctx.send(f'Could not find an emote named: {content}')


@fortnite_bot.command()
@perms()
async def promote(ctx, *, epic_username: Optional[str] = None) -> None:
	if epic_username is None:
		user = await fortnite_bot.fetch_user(ctx.author.display_name)
		member = fortnite_bot.party.get_member(user.display_name)
	else:
		user = await fortnite_bot.fetch_user(epic_username)
		member = fortnite_bot.party.get_member(user.display_name)

	if member is None:
		await ctx.send("Failed to find that user, are you sure they're in the party?")
	else:
		try:
			await member.promote()
			await ctx.send(f"Promoted user: {member.display_name}.")
			print(f"Promoted user: {member.display_name}", "blue")
		except fortnitepy.errors.Forbidden:
			await ctx.send(f"Failed topromote {member.display_name}, as I'm not party leader.")
			print(crayons.red("Failed to promote member as I don't have the required permissions."))


@fortnite_bot.command()
@perms()
async def hide(ctx, *, user = None):
	if fortnite_bot.party.me.leader:
		if user != None:
			try:
				if user is None:
					user = await fortnite_bot.fetch_profile(ctx.message.author.display_name)
					member = fortnite_bot.party.members.get(user.display_name)
				else:
					user = await fortnite_bot.fetch_profile(user)
					member = fortnite_bot.party.members.get(user.display_name)

				raw_squad_assignments = fortnite_bot.party.meta.get_prop('Default:RawSquadAssignments_j')["RawSquadAssignments"]

				for m in raw_squad_assignments:
					if m['memberId'] == member.display_name:
						raw_squad_assignments.remove(m)

				await set_and_update_party_prop(
					'Default:RawSquadAssignments_j',
					{
						'RawSquadAssignments': raw_squad_assignments
					}
				)

				await ctx.send(f"Hid {member.display_name}")
			except AttributeError:
				await ctx.send("I could not find that user.")
			except fortnitepy.HTTPException:
				await ctx.send("I am not party leader.")
		else:
			try:
				await set_and_update_party_prop(
					'Default:RawSquadAssignments_j',
					{
						'RawSquadAssignments': [
							{
								'memberId': fortnite_bot.user.display_name,
								'absoluteMemberIdx': 1
							}
						]
					}
				)

				await ctx.send("Hid everyone in the party.")
			except fortnitepy.HTTPException:
				await ctx.send("I am not party leader.")
	else:
		await ctx.send("I need party leader to do this!")


@fortnite_bot.command()
@perms()
async def add(ctx, *, member = None):
	if member is not None:
		try:
			user = await fortnite_bot.fetch_profile(member)
			friends = fortnite_bot.friends

			if user.display_name in friends:
				await ctx.send(f"I already have {user.display_name} as a friend")
			else:
				await fortnite_bot.add_friend(user.display_name)
				await ctx.send(f'Sent a friend request to {user.display_name}')
				print('Sent a friend request to: ' f'{user.display_name}')

		except fortnitepy.HTTPException:
			await ctx.send("There was a problem trying to add this friend.")
		except AttributeError:
			await ctx.send("I can't find a player with that name.")
	else:
		await ctx.send(f"No user was given. Try: {T}add (user)")

@fortnite_bot.command()
async def pickaxe(ctx, *, content = None):
	if content is None:
		await ctx.send(f'No pickaxe was given, try: {T}pickaxe (pickaxe name)')
	elif content.upper().startswith('Pickaxe_'):
		await fortnite_bot.party.me.set_pickaxe(asset=content.upper())
		await ctx.send(f'Pickaxe set to: {content}')
	else:
		try:
			cosmetic = await BenBotAsync.get_cosmetic(
				lang="en",
				searchLang="en",
				matchMethod="contains",
				name=content,
				backendType="AthenaPickaxe"
			)
			await fortnite_bot.party.me.set_pickaxe(asset=cosmetic.id)
			await ctx.send(f'Pickaxe set to: {cosmetic.name}')
		except BenBotAsync.exceptions.NotFound:
			await ctx.send(f'Could not find a pickaxe named: {content}')


@fortnite_bot.command()
async def pet(ctx, *, content = None):
	if content is None:
		await ctx.send(f'No pet was given, try: {T}pet (pet name)')
	elif content.lower() == 'none':
		await fortnite_bot.party.me.clear_pet()
		await ctx.send('Pet set to: None')
	else:
		try:
			cosmetic = await BenBotAsync.get_cosmetic(
				lang="en",
				searchLang="en",
				matchMethod="contains",
				name=content,
				backendType="AthenaPet"
			)
			await fortnite_bot.party.me.set_pet(asset=cosmetic.id)
			await ctx.send(f'Pet set to: {cosmetic.name}')
		except BenBotAsync.exceptions.NotFound:
			await ctx.send(f'Could not find a pet named: {content}')


@fortnite_bot.command()
async def pinkghoul(ctx):
	variants = fortnite_bot.party.me.create_variants(material=3)

	await fortnite_bot.party.me.set_outfit(
		asset='CID_029_Athena_Commando_F_Halloween',
		variants=variants
	)

	await ctx.send('Skin set to: Pink Ghoul Trooper')


@fortnite_bot.command()
async def purpleskull(ctx):
	variants = fortnite_bot.party.me.create_variants(clothing_color=1)

	await fortnite_bot.party.me.set_outfit(
		asset='CID_030_Athena_Commando_M_Halloween',
		variants = variants
	)

	await ctx.send('Skin set to: Purple Skull Trooper')




@fortnite_bot.command()
async def hatlessrecon(ctx):
	variants = fortnite_bot.party.me.create_variants(parts=2)

	await fortnite_bot.party.me.set_outfit(
		asset='CID_022_Athena_Commando_F',
		variants=variants
	)

	await ctx.send('Skin set to: Hatless Recon Expert')



@fortnite_bot.command()
async def hologram(ctx):
	await fortnite_bot.party.me.set_outfit(
		asset='CID_VIP_Athena_Commando_M_GalileoGondola_SG'
	)
	
	await ctx.send("Skin set to: Hologram")




@fortnite_bot.command()
async def new(ctx, content = None):
	newSkins = getNewSkins()
	newEmotes = getNewEmotes()

	previous_skin = fortnite_bot.party.me.outfit

	if content is None:
		await ctx.send(f'There are {len(newSkins) + len(newEmotes)} new skins + emotes')

		for cosmetic in newSkins + newEmotes:
			if cosmetic.startswith('CID_'):
				await fortnite_bot.party.me.set_outfit(asset=cosmetic)
				await asyncio.sleep(4)
			elif cosmetic.startswith('EID_'):
				await fortnite_bot.party.me.clear_emote()
				await fortnite_bot.party.me.set_emote(asset=cosmetic)
				await asyncio.sleep(4)

	elif 'skin' in content.lower():
		await ctx.send(f'There are {len(newSkins)} new skins')

		for skin in newSkins:
			await fortnite_bot.party.me.set_outfit(asset=skin)
			await asyncio.sleep(4)

	elif 'emote' in content.lower():
		await ctx.send(f'There are {len(newEmotes)} new emotes')

		for emote in newEmotes:
			await fortnite_bot.party.me.clear_emote()
			await fortnite_bot.party.me.set_emote(asset=emote)
			await asyncio.sleep(4)

	await fortnite_bot.party.me.clear_emote()
	
	await ctx.send('Done!')

	await asyncio.sleep(1.5)

	await fortnite_bot.party.me.set_outfit(asset=previous_skin)

	if (content is not None) and ('skin' or 'emote' not in content.lower()):
		ctx.send(f"Not a valid option. Try: {T}new (skins, emotes)")



@fortnite_bot.command()
async def style(ctx: fortnitepy.ext.commands.Context, cosmetic_name: str, variant_type: str, variant_int: str) -> None:
		# cosmetic_types = {
		#     "AthenaCharacter": self.bot.party.me.set_outfit,
		#     "AthenaBackpack": self.bot.party.me.set_backpack,
		#     "AthenaPickaxe": self.bot.party.me.set_pickaxe
		# }

	cosmetic = await fortnite_bot.fortnite_api.cosmetics.get_cosmetic(
		lang="en",
		searchLang="en",
		matchMethod="contains",
		name=cosmetic_name,
		backendType="AthenaCharacter"
	)

	cosmetic_variants =fortnite_bot.party.me.create_variants(
			# item=cosmetic.backend_type.value,
		**{variant_type: int(variant_int) if variant_int.isdigit() else variant_int}
	)

		# await cosmetic_types[cosmetic.backend_type.value](
	await fortnite_bot.party.me.set_outfit(
		asset=cosmetic.id,
		variants=cosmetic_variants
	)

	await ctx.send(f'Set variants of {cosmetic.id} to {variant_type} {variant_int}.')

@fortnite_bot.command()
async def ready(ctx):
	await fortnite_bot.party.me.set_ready(fortnitepy.ReadyState.READY)
	await ctx.send('Ready!')



@fortnite_bot.command()
async def unready(ctx):
	await fortnite_bot.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
	await ctx.send('Unready!')



@fortnite_bot.command()
async def skin(ctx, *, content = None):
	if content is None:
		await ctx.send(f'No skin was given, try: {T}!skin (skin name)')
	elif content.upper().startswith('CID_'):
		await fortnite_bot.party.me.set_outfit(asset=content.upper())
		await ctx.send(f'Skin set to: {content}')
	else:
		try:
			cosmetic = await BenBotAsync.get_cosmetic(
				lang="en",
				searchLang="en",
				name=content,
				backendType="AthenaCharacter"
			)
			await fortnite_bot.party.me.set_outfit(asset=cosmetic.id)
			await ctx.send(f'Skin set to: {cosmetic.name}')
		except BenBotAsync.exceptions.NotFound:
			await ctx.send(f'Could not find a skin named: {content}')


@fortnite_bot.command()
async def sitin(ctx):
	await fortnite_bot.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
	await ctx.send('Sitting in')


@fortnite_bot.command()
async def sitout(ctx):
	await fortnite_bot.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
	await ctx.send('Sitting out')


@fortnite_bot.command()
async def tier(ctx, tier = None):
	if tier is None:
		await ctx.send(f'No tier was given. Try: {T}tier (tier number)') 
	else:
		await fortnite_bot.party.me.set_battlepass_info(
			has_purchased=True,
			level=tier
		)

		await ctx.send(f'Battle Pass tier set to: {tier}')


@fortnite_bot.command()
async def level(ctx, level = None):
	if level is None:
		await ctx.send(f'No level was given. Try: {T}level (number)')
	else:
		await fortnite_bot.party.me.set_banner(season_level=level)
		await ctx.send(f'Level set to: {level}')




copied_player = ""




@fortnite_bot.command()
async def copy(ctx, *, username = None):
	global copied_player

	if username is None:
		member = [m for m in fortnite_bot.party.members if m.display_name == ctx.author.display_name][0]

	else:
		user = await fortnite_bot.fetch_user(username)
		member = [m for m in fortnite_bot.party.members if m.display_name == user.display_name][0]

	await fortnite_bot.party.me.edit_and_keep(
			partial(
				fortnitepy.ClientPartyMember.set_outfit,
				asset=member.outfit,
				variants=member.outfit_variants
			),
			partial(
				fortnitepy.ClientPartyMember.set_backpack,
				asset=member.backpack,
				variants=member.backpack_variants
			),
			partial(
				fortnitepy.ClientPartyMember.set_pickaxe,
				asset=member.pickaxe,
				variants=member.pickaxe_variants
			),
			partial(
				fortnitepy.ClientPartyMember.set_banner,
				icon=member.banner[0],
				color=member.banner[1],
				season_level=member.banner[2]
			),
			partial(
				fortnitepy.ClientPartyMember.set_battlepass_info,
				has_purchased=member.battlepass_info[0],
				level=member.battlepass_info[1]
			),
			partial(
				fortnitepy.ClientPartyMember.set_emote,
				asset=member.emote
			)
		)

	await ctx.send(f"Now copying: {member.display_name}")

@commands.dm_only()
@fortnite_bot.command()
async def admin(ctx, setting = None, *, user = None):
	if (setting is None) and (user is None):
		await ctx.send(f"Missing one or more arguments. Try: {T}admin (add, remove, list) (user)")
	elif (setting is not None) and (user is None):

		user = await fortnite_bot.fetch_profile(ctx.message.author.display_name)

		if setting.lower() == 'add':
			if user.display_name in data['AdminPerms']:
				await ctx.send("You are already an admin")

			else:
				await ctx.send("Password?")
				response = await fortnite_bot.wait_for('friend_message', timeout=20)
				content = response.content.lower()
				if content == data['AdminPassword']:
					data['AdminPerms'].append(user.display_name)
					with open('config.json', 'w') as f:
						json.dump(data, f, indent=4)
						await ctx.send(f"Correct. Added {user.display_name} as an admin.")
						print(Fore.GREEN + " [+] " + Fore.LIGHTGREEN_EX + user.display_name + Fore.RESET + " was added as an admin.")
				else:
					await ctx.send("Incorrect Password.")

		elif setting.lower() == 'remove':
			if user.display_name not in data['AdminPerms']:
				await ctx.send("You are not an admin.")
			else:
				await ctx.send("Are you sure you want to remove yourself as an admin?")
				response = await fortnite_bot.wait_for('friend_message', timeout=20)
				content = response.content.lower()
				if (content.lower() == 'yes') or (content.lower() == 'y'):
					data['AdminPerms'].remove(user.display_name)
					with open('config.json', 'w') as f:
						json.dump(data, f, indent=4)
						await ctx.send("You were removed as an admin.")
						print(Fore.BLUE + " [+] " + Fore.LIGHTBLUE_EX + user.display_name + Fore.RESET + " was removed as an admin.")
				elif (content.lower() == 'no') or (content.lower() == 'n'):
					await ctx.send("You were kept as admin.")
				else:
					await ctx.send("Not a correct reponse. Cancelling command.")
				
		elif setting == 'list':
			if user.display_name in data['AdminPerms']:
				admins = []

				for admin in data['AdminPerms']:
					user = await fortnite_bot.fetch_profile(admin)
					admins.append(user.display_name)

				await ctx.send(f"The bot has {len(admins)} admins:")

				for admin in admins:
					await ctx.send(admin)

			else:
				await ctx.send("You don't have permission to this command.")

		else:
			await ctx.send(f"That is not a valid setting. Try: {T}admin (add, remove, list) (user)")
			
	elif (setting is not None) and (user is not None):
		user = await fortnite_bot.fetch_profile(user)

		if setting.lower() == 'add':
			if ctx.message.author.display_name in data['AdminPerms']:
				if user.display_name not in data['AdminPerms']:
					data['AdminPerms'].append(user.display_name)
					with open('config.json', 'w') as f:
						json.dump(data, f, indent=4)
						await ctx.send(f"Correct. Added {user.display_name} as an admin.")
						print(Fore.GREEN + " [+] " + Fore.LIGHTGREEN_EX + user.display_name + Fore.RESET + " was added as an admin.")
				else:
					await ctx.send("That user is already an admin.")
			else:
				await ctx.send("You don't have access to add other people as admins. Try just: !admin add")
		elif setting.lower() == 'remove':
			if ctx.message.author.display_name in data['AdminPerms']:
				if user.display_name in data['AdminPerms']:
					await ctx.send("Password?")
					response = await fortnite_bot.wait_for('friend_message', timeout=20)
					content = response.content.lower()
					if content == data['AdminPassword']:
						data['AdminPerms'].remove(user.display_name)
						with open('config.json', 'w') as f:
							json.dump(data, f, indent=4)
							await ctx.send(f"{user.display_name} was removed as an admin.")
							print(Fore.BLUE + " [+] " + Fore.LIGHTBLUE_EX + user.display_name + Fore.RESET + " was removed as an admin.")
					else:
						await ctx.send("Incorrect Password.")
				else:
					await ctx.send("That person is not an admin.")
			else:
				await ctx.send("You don't have permission to remove players as an admin.")
		else:
			await ctx.send(f"Not a valid setting. Try: {T}admin (add, remove) (user)")

@fortnite_bot.command()
async def credit(ctx):
		credits = "Made By Pirxcy and Quax"
		await ctx.reply(credits)

@fortnite_bot.command()
async def goldpeely(ctx):
	variants = fortnite_bot.party.me.create_variants(progressive=4)

	await fortnite_bot.party.me.set_outfit(
		asset='CID_701_Athena_Commando_M_BananaAgent',
		variants=variants,
		enlightenment=(2, 350)
	)
	await ctx.send('Skin set to: Golden Peely')

async def startcord():
		print('Checking for Discord Updates...')
		if currentpatch == patch:
				print('All Up To Date! Starting Bot!')
				await discord_bot.start('NzgxNzk1MTMzMDQxMTQ3OTM0.X8C1dA.ZlsP5y1SmzUEROQTDTIAPQASSVo')
		else:
				print('This Client is Outdated! Fetching an Update From PirxcyAPI')
				print(f'Updating {currentpatch} To {patch}')
				os.system('pip uninstall NeoBot')
				os.system(f'pip3 install -U NeoBot=={patch}')

async def autoupdate():
		print('Checking for Updates...')
		if currentpatch == patch:
				try:
						print('All Up To Date! Starting Bot!')                        
						await fortnite_bot.start()
				except:
						print('Error Starting!')               
		else:
				print('This Client is Outdated! Fetching an Update From PirxcyAPI')
				print(f'Updating {currentpatch} To {patch}')
				os.system('pip uninstall NeoBot')
				os.system(f'pip3 install -U NeoBot=={patch}')

task = loop.create_task(autoupdate()) and loop.create_task(startcord()) and loop.create_task(keep_alive())							
loop.run_forever()
