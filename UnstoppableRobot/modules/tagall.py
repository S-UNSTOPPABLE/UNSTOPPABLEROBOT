import os
import asyncio
import random
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError
from UnstoppableRobot import telethn as client


spam_chats = []

TAG_TEXT = (
    "__Owww ... Such a stupid idiot, U Can't Do This Ask My Developers.__",
    "__Don't drink and type. You Are Not Allowed To Do This.__",
    "__Command not found. Just like your brain.You Are Not Allowed To Do This.__",
    "__Believe me you are not normal.You Are Not Allowed To Do This.__",
    "__Hey Demon Gu Away. You Are Not Allowed To Do This.__")

AUTH_USER = [5072650671, 5369590180, 5280801259]


@client.on(events.NewMessage(pattern="^/callall ?(.*)"))
@client.on(events.NewMessage(pattern="^@all ?(.*)"))
async def mentionall(event):
  TAGALL = random.choice(TAG_TEXT)
  chat_id = event.chat_id
  if event.sender_id in AUTH_USER:
      if event.is_private:
        return await event.respond("This command can be use in groups and channels!")
      
      is_admin = False
      try:
        partici_ = await client(GetParticipantRequest(
          event.chat_id,
          event.sender_id
        ))
      except UserNotParticipantError:
        is_admin = False
      else:
        if (
          isinstance(
            partici_.participant,
            (
              ChannelParticipantAdmin,
              ChannelParticipantCreator
            )
          )
        ):
          is_admin = True
      if not is_admin:
        return await event.respond("Only admins can mention all!")
      
      if event.pattern_match.group(1) and event.is_reply:
        return await event.respond("Give me one argument!")
      elif event.pattern_match.group(1):
        mode = "text_on_cmd"
        msg = event.pattern_match.group(1)
      elif event.is_reply:
        mode = "text_on_reply"
        msg = await event.get_reply_message()
        if msg == None:
            return await event.respond("I can't mention members for older messages! (messages which are sent before I'm added to group)")
      else:
        return await event.respond("Reply to a message or give me some text to mention others!")
      
      spam_chats.append(chat_id)
      usrnum = 0
      usrtxt = ''
      async for usr in client.iter_participants(chat_id):
        if not chat_id in spam_chats:
          break
        usrnum += 1
        usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}), "
        if usrnum == 5:
          if mode == "text_on_cmd":
            txt = f"{msg}\n{usrtxt}"
            await client.send_message(chat_id, txt)
          elif mode == "text_on_reply":
            await msg.reply(usrtxt)
          await asyncio.sleep(0)
          usrnum = 0
          usrtxt = ''
      try:
        spam_chats.remove(chat_id)
      except:
        pass
  else:
      return await event.respond(f"__Hey__ [{event.sender.first_name}](tg://user?id={event.sender_id}) " + TAGALL)

@client.on(events.NewMessage(pattern="^/cancel$"))
async def cancel_spam(event):
  if not event.chat_id in spam_chats:
    return await event.respond("__There is no proccess on going...__")
  is_admin = False
  try:
    partici_ = await client(GetParticipantRequest(
      event.chat_id,
      event.sender_id
    ))
  except UserNotParticipantError:
    is_admin = False
  else:
    if (
      isinstance(
        partici_.participant,
        (
          ChannelParticipantAdmin,
          ChannelParticipantCreator
        )
      )
    ):
      is_admin = True
  if not is_admin:
    return await event.respond("__Only admins can execute this command!__")
  
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await event.respond("__Stopped Mention.__")


__mod_name__ = "Tᴀɢ Aʟʟ​"
__help__ = """
──「 Only for Admins 」──

❍ /callall or @all '(reply to message or add another message) To mention all members in your group, without exception.'
"""
