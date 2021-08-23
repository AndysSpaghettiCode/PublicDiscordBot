import os
import discord
import heapq
from datetime import datetime
import asyncio
from CyoaBuild import *
from CyoaParser import *

file1 = open("token.txt", "r")
DISCORD_TOKEN = file1.readline()
client = discord.Client()
date_heap = []
heapq.heapify(date_heap)
current_task_obj = None
time_date_dict = dict()
time_format_str = "%m/%d/%Y %H:%M:%S"
channel_str = ""

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message_obj):
    if message_obj.content.startswith('!time') and correct_role(message_obj.author.roles):

        input_str = message_obj.content
        split_message_list = input_str.split(' ', 3)
        message_datetime_str = split_message_list[1] + " " + split_message_list[2]
        end_time_obj = datetime.strptime(message_datetime_str, time_format_str)
        message_str = split_message_list[3]

        if end_time_obj in time_date_dict:
            return

        time_date_dict[end_time_obj] = message_str
        if date_heap and end_time_obj < date_heap[0]:
            cancel_task()
        heapq.heappush(date_heap, end_time_obj)
        if not current_task_obj:
            await message_generator(message_obj)

    elif message_obj.content.startswith('!logs') and correct_role(message_obj.author.roles):
        await logs(message_obj)

    elif message_obj.content.startswith('!cancel') and correct_role(message_obj.author.roles):
        input_str = message_obj.content
        split_message_list = input_str.split(' ', 1)

        if split_message_list[1] == "0":
            cancel_task()
            del_heap_head()
            if date_heap:
                await message_generator(message_obj)
        else:
            date_idx_int = int(split_message_list[1])
            del time_date_dict[date_heap[date_idx_int]]
            date_heap.pop(date_idx_int)
            heapq.heapify(date_heap)

    elif message_obj.content.startswith('!setchannel') and correct_role(message_obj.author.roles):
        input_str = message_obj.content
        split_message_list = input_str.split(' ', 1)
        set_channel(split_message_list[1])

    # Choose your own adventure Section#
    elif message_obj.content.startswith('!story') and correct_player_role(message_obj.author.roles):

        input_str = message_obj.content
        split_message_list = input_str.split(' ', 1)
        file_name_str = split_message_list[1]+".txt"
        if os.path.exists(file_name_str):
            await message_obj.channel.send("story file found")
        else:
            await message_obj.channel.send("story file not found")

        path_import_list, dialogue_import_list, options_import_list = parse_text(file_name_str)
        client.cyoa_dict = cyoa_dict(path_import_list, dialogue_import_list, options_import_list)
        client.cyoa_dict["current"] = client.cyoa_dict["0"]
        await print_node(message_obj, client.cyoa_dict["current"])

    elif message_obj.content.startswith('!option') and correct_player_role(message_obj.author.roles):
        input_str = message_obj.content
        split_message_list = input_str.split(' ', 1)
        num_options_int = len(client.cyoa_dict["current"].options)
        if split_message_list[1].isnumeric() and 0 <= int(split_message_list[1])-1 < num_options_int:
            client.cyoa_dict["current"] = next_node(client.cyoa_dict, client.cyoa_dict["current"], split_message_list[1])
            await print_node(message_obj, client.cyoa_dict["current"])
        else:
            await message_obj.channel.send("invalid option")


def correct_role(ctx_obj):
    for roles_obj in ctx_obj:
        if roles_obj.name == "DM":
            return True
    return False


def correct_player_role(ctx_obj):
    for roles_obj in ctx_obj:
        if roles_obj.name == "Player":
            return True
    return False


def set_channel(name_str):
    global channel_str
    channel_str = name_str


def cancel_task():
    global current_task_obj
    current_task_obj.cancel()
    current_task_obj = None


async def message(ctx_obj, end_time_obj):
    global current_task_obj
    global channel_str
    current_task_obj = asyncio.current_task()
    time_diff_int = end_time_obj - datetime.now()
    await asyncio.sleep(time_diff_int.total_seconds())
    channel_obj = discord.utils.get(ctx_obj.guild.channels, name=channel_str)
    await channel_obj.send(time_date_dict[end_time_obj])
    del_heap_head()
    current_task_obj = None
    if date_heap:
        await message_generator(ctx_obj)


async def message_generator(ctx_obj):
    asyncio.create_task(message(ctx_obj, date_heap[0]))


async def logs(ctx_obj):
    print_message_str = ""
    for idx_int, date_time_obj in enumerate(date_heap):
        print_message_str = print_message_str + str(idx_int) + " " + str(date_time_obj) + " " + time_date_dict[date_time_obj] + " \n"
    await ctx_obj.channel.send(print_message_str)


def del_heap_head():
    del time_date_dict[date_heap[0]]
    heapq.heappop(date_heap)


client.run(DISCORD_TOKEN)
