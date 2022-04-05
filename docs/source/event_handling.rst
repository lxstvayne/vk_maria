:ref: `event_handling`

Обработка событий
------------------

*****************
Лонгполлинг
*****************

События можно обрабатывать двумя способами

###############
С помощью цикла
###############

.. code-block:: python3

    from vk_maria import Vk
    from vk_maria.longpoll import LongPoll

    vk = Vk(access_token='token')
    lp = LongPoll(vk)

    for event in lp.listen():
        ...


##############################
С помощью диспетчера событий
##############################

.. code-block:: python3

    from vk_maria import Vk
    from vk_maria.dispatcher import Dispatcher

    vk = Vk(access_token='token')
    dp = Dispatcher(vk)

    @dp.message_handler()
    def handler(event: types.Message)
        ...

    if __name__ == '__main__':
        dp.start_polling()

