export const mockChats = {
    '12345': [
        {
            chat_id: '55555',
            title: "Первый чат",
            messages: [
                {
                    message_id: 0,
                    is_bot: false,
                    text: "Первое сообщение пользователя 12345 в чате 55555",
                    answer_to: NaN,
                    react: 0
                },
                {
                    message_id: 1,
                    is_bot: true,
                    text: "Первый ответ бота пользователю 12345 в чате 55555",
                    answer_to: NaN,
                    react: 0
                },
                {
                    message_id: 2,
                    is_bot: false,
                    text: "Второе сообщение пользователя 12345 в чате 55555",
                    answer_to: NaN,
                    react: 0
                },
                {
                    message_id: 3,
                    is_bot: true,
                    text: "Второй ответ бота пользователю 12345 в чате 55555",
                    answer_to: NaN,
                    react: -1
                },
                {
                    message_id: 4,
                    is_bot: false,
                    text: "Третье сообщение пользователя 12345 в чате 55555",
                    answer_to: 2,
                    react: 0
                },
                {
                    message_id: 5,
                    is_bot: true,
                    text: "Третий ответ бота пользователю 12345 в чате 55555",
                    answer_to: NaN,
                    react: 1
                }
            ]
        },
        {},
        {}
    ],
    '54321': [
        {},
        {},
        {}
    ]
}

export default mockChats;