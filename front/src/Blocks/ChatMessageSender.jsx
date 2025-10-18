import React, {useState, useEffect} from "react";
import ChatMessage from "./ChatMessage.jsx";

const ChatMessageSender = ({SendMessage, setMessageForAnswer, messageForAnswer}) => {
    const [message, setMessage] = useState();

    const handleSubmit = async (e) => {
        e.preventDefault();
        SendMessage(message);
    }

    return (
        <div>
            {(messageForAnswer.message_id != -1) && <div>
                <ChatMessage
                    message={messageForAnswer}
                    answeredMessage={{message_id: -1}}
                    isMain={false}
                />
                <button onClick={() => {setMessageForAnswer({message_id: -1})}}>Отменить</button>
            </div>}
            <form onSubmit={handleSubmit}>
                <input
                    id = "message"
                    type="text"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Написать чат-боту поддержки"
                    required
                />
                <button type="submit">Написать</button>
            </form>
        </div>
    );
};

export default ChatMessageSender;