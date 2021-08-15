def kick_and_delete(vk, peer_id, from_id, admins, message_ids):

    if from_id not in admins:

        try:

            vk.messages.removeChatUser(
                chat_id=peer_id - 2000000000,
                member_id=from_id,
            )

        except:

            pass

        try:

            vk.messages.delete(
                peer_id=peer_id,
                conversation_message_ids=message_ids,
                delete_for_all=1
            )

        except:

            pass

    return 'ok'
