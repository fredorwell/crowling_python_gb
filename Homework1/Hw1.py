import vk_api
import json
my_token = "f06af244bb4c369bea37453dc312fc6c0cdb9a23a0d1999668a9b06faa6b421458cb277b02203482e9db2"

session = vk_api.VkApi(token= my_token)
vk = session.get_api()


friend_list = vk.friends.get()
print(friend_list)

with open("friend_list.json", "w") as f:
    json.dump(friend_list, f)


# Я немного посмотрел апи вк и сделал ниже скрипт для отправки сообщений, можете не обращать на него внимание:
# def send(inp):
#     vk.messages.send(user_id = 1986107, message = inp, random_id=0)
#
#
# while True:
#     msg = input("введите сообщение или q для выхода:")
#     if msg != "q":
#         send(input())
#     else:
#         break


