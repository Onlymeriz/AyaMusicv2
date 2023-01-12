from youtubesearchpython import VideosSearch
import os
from os import path
import random
import asyncio
import shutil
from time import time
import yt_dlp
from .. import converter
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.types import Voice
from AyaMusic import (app, BOT_USERNAME, BOT_ID)
from ..AyaUtils.tgcallsrun import (aya, convert, download, clear, get, is_empty, put, task_done, smexy)
from AyaMusic.AyaUtils.database.queue import (is_active_chat, add_active_chat, remove_active_chat, music_on, is_music_playing, music_off)
from AyaMusic.AyaUtils.database.onoff import (is_on_off, add_on, add_off)
from AyaMusic.AyaUtils.database.blacklistchat import (blacklisted_chats, blacklist_chat, whitelist_chat)
from AyaMusic.AyaUtils.database.gbanned import (get_gbans_count, is_gbanned_user, add_gban_user, add_gban_user)
from AyaMusic.AyaUtils.database.playlist import (get_playlist_count, _get_playlists, get_note_names, get_playlist, save_playlist, delete_playlist)
from AyaMusic.AyaUtils.helpers.inline import play_keyboard, confirm_keyboard, play_list_keyboard, close_keyboard, confirm_group_keyboard
from AyaMusic.AyaUtils.database.theme import (_get_theme, get_theme, save_theme)
from AyaMusic.AyaUtils.database.assistant import (_get_assistant, get_assistant, save_assistant)
from ..config import DURATION_LIMIT, ASS_ID
from ..AyaUtils.helpers.decorators import errors
from ..AyaUtils.helpers.filters import command, other_filters
from ..AyaUtils.helpers.gets import (get_url, themes, random_assistant)
from ..AyaUtils.helpers.thumbnails import gen_thumb
from ..AyaUtils.helpers.chattitle import CHAT_TITLE
from ..AyaUtils.helpers.ytdl import ytdl_opts 
from ..AyaUtils.helpers.inline import (play_keyboard, search_markup, play_markup, playlist_markup)
from pyrogram import filters
from typing import Union
from youtubesearchpython import VideosSearch
from pyrogram.types import Message, Audio, Voice
from pyrogram.types import (CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Message, )


options = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "all","16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",]   


@Client.on_message(command(["playlist", "playlist"]) & other_filters)
async def pause_cmd(_, message):
    thumb ="cache/playlist.png"
    await message.reply_photo(
    photo=thumb, 
    caption=("**❓ Which playlist do you want to play ?**"),    
    reply_markup=play_list_keyboard) 
    return 


@Client.on_message(command(["delmyplaylist", "delmyplaylist"]) & other_filters)
async def delmyplaylist(_, message):
    usage = ("usage:\n\n/delmyplaylist [numbers between 1-30] (to delete a particular music in playlist)\n\n/delmyplaylist all (to delete whole playlist)")
    if len(message.command) < 2:
        return await message.reply_text(usage)
    name = message.text.split(None, 1)[1].strip()
    if not name:
        return await message.reply_text(usage)
    if name not in options:
        return await message.reply_text(usage)
    if len(message.text) == 18:
        return await message.reply_text(f"💡 **confirmation** !\n\nare you sure want to delete your whole playlist ?", reply_markup=confirm_keyboard)
    else:
         _playlist = await get_note_names(message.from_user.id)
    if not _playlist:
        await message.reply_text("you have no playlist on aya music database !")
    else:
        titlex = []
        j = 0
        count = int(name)
        for note in _playlist:
            j += 1
            _note = await get_playlist(message.from_user.id, note)
            if j == count:
                deleted = await delete_playlist(message.from_user.id, note)
                if deleted:
                    return await message.reply_text(f"**deleted the {count} music in playlist**")
                else:
                    return await message.reply_text(f"**no such saved music in playlist.**")                                
        await message.reply_text("you have no such music in playlist.")                             


@Client.on_message(command(["delchatplaylist", "delchatplaylist"]) & other_filters)
async def delchatplaylist(_, message):
    a = await app.get_chat_member(message.chat.id , message.from_user.id)
    if not a.can_manage_voice_chats:
        return await message.reply_text("you must be admin with permission:\n\n» ❌ __Can manage video chat__")
    usage = ("usage:\n\n/delchatplaylist [numbers between 1-30] (to delete a particular music in playlist)\n\n/delchatplaylist all (to delete whole playlist)")
    if len(message.command) < 2:
        return await message.reply_text(usage)
    name = message.text.split(None, 1)[1].strip()
    if not name:
        return await message.reply_text(usage)
    if name not in options:
        return await message.reply_text(usage)
    if len(message.text) == 21:
        return await message.reply_text(f"💡 confirmation !\n\nare you sure want to delete whole whole playlist ?", reply_markup=confirm_group_keyboard)
    else:
         _playlist = await get_note_names(message.chat.id)
    if not _playlist:
        await message.reply_text("Group's has no playlist on aya music database.")
    else:
        titlex = []
        j = 0
        count = int(name)
        for note in _playlist:
            j += 1
            _note = await get_playlist(message.chat.id, note)
            if j == count:
                deleted = await delete_playlist(message.chat.id, note)
                if deleted:
                    return await message.reply_text(f"**deleted the {count} music in group's playlist**")
                else:
                    return await message.reply_text(f"**no such saved music in Group playlist.**")                                
        await message.reply_text("you have no such music in Group's playlist.")
