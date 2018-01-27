import json
from channels import Group
from channels import Channel
from channels.auth import channel_session_user_from_http, channel_session_user
from .models import Room
from .utils import catch_client_error, get_room_or_error
from .exceptions import ClientError

@channel_session_user_from_http
def ws_connect(message):
    message.reply_channel.send({"accept": True})
    message.channel_session['rooms'] = []


@channel_session_user
def ws_disconnect(message):
    for room_id in message.channel_session.get("rooms", set()):

        try:
            room = Room.objects.get(pk=room_id)
            room.websocket_group.discard(message.reply_channel)
        except Room.DoesNotExist:
            pass


def ws_receive(message):
    payload = json.loads(message['text'])
    payload['reply_channel'] = message.content['reply_channel']
    Channel("chat.receive").send(payload)


@channel_session_user
@catch_client_error
def chat_join(message):
    room = get_room_or_error(message["room"], message.user)
    user = message.user.username
    room.send_message(user+' has joined the chat', message.user)

    room.websocket_group.add(message.reply_channel)
    message.channel_session['rooms'] = list(set(message.channel_session['rooms']).union([room.id]))
    message.reply_channel.send({
        "text": json.dumps({
            "join": str(room.id),
            "display_name": room.display_name,
        }),
    })

@channel_session_user
@catch_client_error
def chat_leave(message):
    room = get_room_or_error(message["room"], message.user)
    user = message.user.username
    room.send_message(user+' has joined the chat', message.user)

    room.websocket_group.discard(message.reply_channel)
    message.channel_session['rooms'] = list(set(message.channel_session['rooms']).difference([room.id]))

    message.reply_channel.send({
        "text": json.dumps({
            "leave": str(room.id),
        })
    })

@channel_session_user
@catch_client_error
def chat_send(message):
    if message['room'] not in message.channel_session['rooms']:
        raise ClientError("ROOM_ACCESS_DENIED")
    room = get_room_or_error(message["room"], message.user)
    room.send_message(message["message"], message.user)
