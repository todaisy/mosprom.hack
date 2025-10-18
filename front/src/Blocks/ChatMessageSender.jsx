import React, {useState, useEffect} from "react";
import ChatMessage from "./ChatMessage.jsx";

const ChatMessageSender = ({SendMessage, setMessageForAnswer, messageForAnswer, generatingMessage}) => {
    const [message, setMessage] = useState();

    const handleSubmit = async (e) => {
        e.preventDefault();
        SendMessage(message);
    }

    return (
        <div className="chatMessageSender">
            {(messageForAnswer.message_id != -1) && <div className="chatMessageSenderAnsweredMessageContainer">
                <ChatMessage
                    message={messageForAnswer}
                    answeredMessage={{message_id: -1}}
                    isMain={false}
                />
                <button onClick={() => {setMessageForAnswer({message_id: -1})}}>Отменить</button>
            </div>}
            <form onSubmit={handleSubmit} className="chatMessageSenderForm">
                <input
                    id = "message"
                    type="text"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Написать чат-боту поддержки"
                    required
                />
                <button type="submit" disabled={generatingMessage}>Написать</button>
            </form>
        </div>
    );
};

export default ChatMessageSender;