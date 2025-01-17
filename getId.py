import re
import requests
import json
import streamlit as st
import base64


# Функция для получения ID пользователя
def getId(nick):
    def has_russian_letters(string):
        pattern = re.compile('[а-яА-Я]')
        return re.search(pattern, string) is not None

    if nick[0] == "#":
        first = int(nick[1:3], 16)
        second = int(nick[3:5], 16)
        third = int(nick[5:], 16)
        nick = str(first * 256 * 256 + second * 256 + third)
        nick = "ID=" + nick
    elif has_russian_letters(nick):
        nick = base64.b64encode(nick.encode('utf-8'))
        nick = str(nick)[2:len(str(nick)) - 1]
        nick = "@" + str(nick)
        nick = "nick=" + nick
    else:
        nick = "nick=" + nick

    req1 = "https://api.efezgames.com/v1/social/findUser ?{NICK}"
    request1 = req1.format(NICK=nick)
    response = requests.get(request1)
    try:
        data = json.loads(response.text)
        uID = str(data["_id"])
    except json.decoder.JSONDecodeError:
        return "error"
    return uID


# Функция для торговли
def trade(nick, skin="GG40$Xz0$Xz1$Xz2$Xz3$Xz4"):
    iD = getId(nick)
    if iD == "error":
        iD = nick

    # Здесь вы должны заменить c._token и другие переменные на ваши реальные значения
    req = "https://api.efezgames.com/v1/trades/createOffer?token={TOKEN}&timestamp={TS}&playerID={PLAYERID}&receiverID={RECEIVERID}&senderNick={SENDERNICK}&senderFrame={SENDERFRAME}&senderAvatar={SENDERAVATAR}&receiverNick={RECEIVERNICK}&receiverFrame={RECEIVERFRAME}&receiverAvatar={RECEIVERAVATAR}&skinsOffered={SKINSOFFERED}&skinsRequested={SKINSREQUESTED}&message={MESSAGE}&pricesHash={PRICESHASH}&senderOneSignal=01122&receiverOneSignal=01122&senderVersion=2.31.0&receiverVersion=2.31.0"

    # Замените эти значения на свои
    token = "01122"  # Замените на ваш токен
    sender_nick = "Tool_Bot™"  # Замените на ваше имя отправителя
    sender_frame = "lP"  # Замените на ваше имя рамки отправителя
    sender_avatar = "default_avatar"  # Замените на ваше имя аватара отправителя
    prices_hash = "097ae5177d15c2fbbd39942daf818255"  # Замените на ваш хэш цен

    request = req.format(
        TOKEN=token,
        PLAYERID=iD,
        RECEIVERID=iD,
        SENDERNICK=sender_nick,
        SENDERFRAME=sender_frame,
        SENDERAVATAR=sender_avatar,
        RECEIVERNICK=sender_nick,
        RECEIVERFRAME=sender_frame,
        RECEIVERAVATAR=sender_avatar,
        SKINSOFFERED=skin,
        TS="01122",
        SKINSREQUESTED=skin,
        PRICESHASH=prices_hash,
        MESSAGE="<color = red>Made by 01122"
    )
    response = requests.get(request)
    return response.text


# Streamlit UI
st.title("Case Opener Tool by 01122!")

# Создание вкладок
tabs = st.sidebar.radio("Select a tab:", ["Get User ID", "Trade"])

if tabs == "Get User ID":
    # Вкладка для получения ID пользователя
    nick_input = st.text_input("Type user nick or tag:")
    if st.button("Get ID"):
        if nick_input:
            user_id = getId(nick_input)
            if user_id != "error":
                st.success(f"User  ID: {user_id}")
            else:
                st.error("Oops! Something went wrong. Check if nickname is bugged in game or try again!")
        else:
            st.warning("Please enter something!")

elif tabs == "Trade":
    # Вкладка для торговли
    trade_nick = st.text_input("Type the player's nick for trade:")
    skin_input = st.text_input("Type the skin you want to trade:", value="GG40$Xz0$Xz1$Xz2$Xz3$Xz4")

    if st.button("Create Trade Offer"):
        if trade_nick:
            trade_response = trade(trade_nick, skin_input)
            st.success(f"Trade response: {trade_response}")
        else:
            st.warning("Please enter a player's nick!")
