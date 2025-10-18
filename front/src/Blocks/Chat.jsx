import React, {useState, useEffect} from "react";
import ChatMessage from "./ChatMessage.jsx";

const Chat = ({chatMessages, setMessageForAnswer, reactMessage}) => {
    return (
        <div>
            {chatMessages.map((message, index) => (
                <ChatMessage
                    key={index}
                    message={message}
                    answeredMessage={chatMessages.find((messagesItem) => (messagesItem.message_id === message.answer_to))}
                    isMain={true}
                    setMessageForAnswer={setMessageForAnswer}
                    reactMessage={reactMessage}
                />
            ))}
        </div>
    );
};

export default Chat;