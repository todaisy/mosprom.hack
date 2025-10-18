import React, {useState, useEffect} from "react";

const ChatMessage = ({message, answeredMessage, isMain, setMessageForAnswer, reactMessage}) => {

    return (
        <div>
            {isMain && answeredMessage && (
                <ChatMessage
                    message={answeredMessage}
                    answeredMessage={undefined}
                    isMain={false}
                />)}
            <p>{message.text}</p>
            <div>
                {message.is_bot && isMain && <div>
                    {message.react != 1 && <button onClick={() => reactMessage(message, 1)}>+</button>}
                    {message.react != -1 && <button onClick={() => reactMessage(message, -1)}>-</button>}
                    <button onClick={() => reactMessage(message, 0)}>{message.react}</button>
                </div>}
                {isMain && <button onClick={() => setMessageForAnswer(message)}>Ответить</button>}
            </div>
            
        </div>
    );
};

export default ChatMessage;