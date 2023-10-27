from telegram.ext import CommandHandler, MessageHandler, Filters
from settings import TELEGRAM_SUPPORT_CHAT_ID


def start(update, context):
    update.message.reply_text('Привет, задай мне свой вопрос)')

    user_info = update.message.from_user.to_dict()

    context.bot.send_message(
        chat_id=TELEGRAM_SUPPORT_CHAT_ID,
        text=f"""
📞 Новый пользователь -  {user_info}.
        """,
    )


def forward_to_chat(update, context):
    forwarded = update.message.forward(chat_id=TELEGRAM_SUPPORT_CHAT_ID)
    # print(forwarded.forward_from)
    # print()
    # print(forwarded)
    # print()
    # print(update)
    try:
        context.bot.send_message(
            chat_id=TELEGRAM_SUPPORT_CHAT_ID,
            reply_to_message_id=forwarded.message_id,
            text=f'Новый вопрос от @{update.message.chat.username} ID:{update.message.from_user.id}\n'
                 f'{"Отвечайте только на это сообщение (Reply)"}'
        )
    except Exception as err:
        print(err)


def forward_to_user(update, context):
    user_id = None
    try:
        if update.message is not None:
            user_id = int(update.message.reply_to_message.text.split('ID:')[1].split('\n')[0])
        else:
            user_id = int(update.channel_post.reply_to_message.text.split('ID:')[1].split('\n')[0])
    except AttributeError:
        user_id = None
    if user_id:
        if update.message is not None:
            context.bot.copy_message(
                message_id=update.message.message_id,
                chat_id=user_id,
                from_chat_id=update.message.chat.id
            )
        else:
            context.bot.copy_message(
                message_id=update.channel_post.message_id,
                chat_id=user_id,
                from_chat_id=update.channel_post.chat.id
            )
    else:
        context.bot.send_message(
            chat_id=TELEGRAM_SUPPORT_CHAT_ID,
            text='Пользователь выше не разрешает пересылать свои сообщения. Вы должны ответить на ответ бота под сообщением, переадресованным пользователем.'
        )


def setup_dispatcher(dp):
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.chat_type.private, forward_to_chat))
    dp.add_handler(MessageHandler(Filters.chat(TELEGRAM_SUPPORT_CHAT_ID) & Filters.reply, forward_to_user))
    return dp
