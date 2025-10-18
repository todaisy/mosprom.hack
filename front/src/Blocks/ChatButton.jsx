import React, {useState, useEffect} from "react";

const ChatButton = ({chat_id, title, setChoosenChat}) => {
    return (
        <button onClick={() => {setChoosenChat(chat_id)}} className="chatButton">
            {title}
        </button>
    ); 
};

export default ChatButton;