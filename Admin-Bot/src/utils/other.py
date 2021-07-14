import random


def send_msg(vk, peer_id, message, attachment):
    return vk.messages.send(
        peer_id=peer_id,
        message=message,
        attachment=attachment,
        random_id=random.randint(1, 999999999)
    )


def get_name(vk, uid: int) -> str:
    data = vk.method("users.get", {"user_ids": uid})[0]
    return "{} {}".format(data["first_name"], data["last_name"])


def get_rp_names(vk, user_1, user_2, case):
    return vk.execute(code='var user_a = {'
                           f'"user_ids": {user_1},'
                           '"fields": "sex",'
                           '};'
                           'var user_b = {'
                           f'"user_ids": {user_2},'
                           f'"name_case": "{case}",'
                           '};'
                           'var out = { "result": [] };'
                           'out.result.push(API.users.get(user_a)[0]);'
                           'out.result.push(API.users.get(user_b )[0]);'
                           'return out;'
    )


def get_user(vk, pattern: str):
    if "[id" in pattern:
        return int(pattern.split("|")[0].replace("[id", ""))

    if "[club" in pattern:
        return int(pattern.split("|")[0].replace("[club", "-"))

    if "vk.com/" in pattern:
        domen = pattern.split("/")[-1].replace("id", "")
        return vk.users.get(user_ids=domen)[0]["id"]
