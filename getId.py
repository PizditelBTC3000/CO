import re
import requests
import json
import streamlit as st
import base64

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

# Streamlit UI
st.title("Getting user ID in Case Opener")

# Текстовое поле для ввода ника
nick_input = st.text_input("Type user nick or tag:")

# Кнопка для получения идентификатора
if st.button("Get ID"):
    if nick_input:
        user_id = getId(nick_input)
        if user_id != "error":
            st.success(f"User ID: {user_id}")
        else:
            st.error("Oops! Something went wrong. Check if nickname is bugged in game ar try again!")
    else:
        st.warning("Please enter something!")
