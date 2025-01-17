import re
import requests
import json
import streamlit as st
import base64
import hashlib

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

# Функция для получения ID пользователя с учетом дополнительных параметров
def get_id_bugged(nick, keyword, chat, region):
    # Здесь вы можете реализовать логику для получения ID с учетом дополнительных параметров
    # Например, отправка запроса к другому API или выполнение поиска по базе данных
    return "ID с учетом дополнительных параметров"

# Функция для торговли
def trade(nick, skin="GG40$Xz0$Xz1$Xz2$Xz3$Xz4"):
    iD = getId(nick)
    if iD == "error":
        iD = nick

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
        MESSAGE="<color=red>Made by 01122"
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
    
    # Выбор ключевого слова
    keyword = st.selectbox("Select keyword:", ["Keyword1", "Keyword2", "Keyword3"])
    
    # Выбор чата
    chat = st.selectbox("Select chat type:", ["Chat1", "Chat2", "Chat3"])
    
    # Выбор региона
    region = st.selectbox("Select region:", ["RU", "DE", "US", "PL", "PREMIUM"])
    
    if st.button("Get ID"):
        if nick_input:
            user_id = get_id_bugged(nick_input, keyword, chat, region)
            if user_id != "error":
                st.success(f"User  ID: {user_id}")
            else:
                st.error("Oops! Something went wrong. Check if nickname is bugged in game or try again!")
        else:
            st.warning("Please enter something!")

elif tabs == "Trade":
    # Вкладка для торговли
    trade_nick = st.text_input("Type the player's nick for trade:")
    skin_input = st.text_input("Type the skin you want to trade:", placeholder="GG40$Xz0$Xz1$Xz2$Xz3$Xz4")
    password_input = st.text_input("Enter password:", type="password")
    hash_object = hashlib.sha256(password_input.encode())
    hash_hex = hash_object.hexdigest()
    target_hash = "5a6036bf59e008f5eb445d335b28fb5bcc9f47b1a030488642fab2dcec5190b1"
    
    if st.button("Create Trade Offer"):
        if trade_nick and hash_hex == target_hash:
            trade_response = trade(trade_nick, skin_input)
            st.success(f"Trade response: {trade_response}")
        elif hash_hex != target_hash:
            st.error("Incorrect password!")
        else:
            st.warning("Please enter a player's nick!")
