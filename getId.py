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

    req1 = "https://api.efezgames.com/v1/social/findUser?{NICK}"
    request1 = req1.format(NICK=nick)
    response = requests.get(request1)
    try:
        data = json.loads(response.text)
        uID = str(data["_id"])
    except json.decoder.JSONDecodeError:
        return "error"
    return uID

# Функция для получения ID пользователя с учетом дополнительных параметров
def get_id_bugged(keyword=None, chat_id="RU"):
    api_url = f"https://api-project-7952672729.firebaseio.com/Chat/Messages/{chat_id}.json?orderBy=\"ts\"&limitToLast=20"
    response = requests.get(api_url)
    if response.status_code != 200:
        return "error"  # Если произошла ошибка при запросе
    messages = response.json()  # Предполагается, что ответ в формате JSON
    user_id = None
    for message in messages:
        if keyword and keyword.lower() in messages[message]['msg'].lower():  # Проверяем наличие ключевого слова
            user_id = messages[message]['playerID']  # Получаем ID пользователя
            break  # Выходим из цикла, если нашли

    return user_id if user_id else "not found"

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
    st.header("Get User ID")
    
    # Разделение на секции
    method = st.radio("Choose a method to get User ID:", ["By Nickname", "By Keyword"])
    
    if method == "By Nickname":
        nick_input = st.text_input("Type user nick:")
        if st.button("Get ID by Nick"):
            if nick_input:
                user_id = getId(nick_input)
                if user_id != "error":
                    st.success(f"User   ID: {user_id}")
                else:
                    st.error("Oops! Something went wrong. Check if nickname is bugged in game or try again!")
            else:
                st.warning("Please enter a nickname!")

    elif method == "By Keyword":
        st.markdown("Use this if nickname is bugged. Just ask user to type any keyword in chat - method will search this keyword for last 20 messages in chosen local chat.")
        keyword_input = st.text_input("Enter a keyword:")
        chat = st.selectbox("Select chat region:", ["RU", "DE", "US", "PL", "PREMIUM"])
        if st.button("Get ID by Keyword"):
            if keyword_input:
                user_id = get_id_bugged(keyword=keyword_input, chat_id=chat)
                if user_id != "error":
                    st.success(f"User   ID with keyword: {user_id}")
                else:
                    st.error("Oops! Something went wrong. Try again!")
            else:
                st.warning("Please enter a keyword!")

elif tabs == "Trade":
    # Вкладка для торговли
    st.header("Trade")
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
