from utils.rp_commands import rp_list
from utils.other import get_user, send_msg, get_rp_names


def rp_user(vk, peer_id, from_id, split_text, data, NOTICE, RPS):

    try:

        if RPS == 1:

            if len(split_text) == 2:

                user_id = get_user(vk, split_text[1])

            elif len(split_text) == 1 and "reply_message" in data['object']['message']:

                user_id = data['object']['message']['reply_message']['from_id']

            else:

                user_id = None

            if user_id is None:

                if NOTICE == 1: return send_msg(vk, peer_id, '❎ Пользователь не указан', '')

            else:

                result = get_rp_names(vk, from_id, user_id, rp_list[split_text[0]]["name_case"])

                name_a = f"{result['result'][0]['first_name']} {result['result'][0]['last_name']}"
                name_b = f"{result['result'][1]['first_name']} {result['result'][1]['last_name']}"

                smile = rp_list[split_text[0]]["smile"]

                if result['result'][0]['sex'] == 2:

                    rp_action = rp_list[split_text[0]]["male"]

                else:

                    rp_action = rp_list[split_text[0]]["female"]

                return send_msg(vk, peer_id, f"{smile} [id{from_id}|{name_a}] {rp_action} [id{user_id}|{name_b}]", '')

        else:

            if NOTICE == 1: return send_msg(vk, peer_id, '❎ Вы не можете использовать рп команды', '')

    except:

        if NOTICE == 1: return send_msg(vk, peer_id, '❎ Невозможно применить рп команду', '')

    return "ok"
