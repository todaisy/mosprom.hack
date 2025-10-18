import React, {useState, useEffect} from "react";
import ChatButton from "./ChatButton";

const ChatList = ({chats, setChoosenChat}) => {
    return (
        <div className="chatList">
            <div className="newChatButtonContainer">
                <ChatButton chat_id={undefined} title={"Новый чат"} setChoosenChat={setChoosenChat}></ChatButton>
            </div>
            {chats.map((chat, index) => (
                <div key={index} className="chatButtonContainer">
                    <ChatButton chat_id = {chat.chat_id} title = {chat.title} setChoosenChat={setChoosenChat}/>
                </div>
            ))}
        </div>
    );
};

export default ChatList;