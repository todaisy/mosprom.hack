import React, {useState, useEffect} from "react";
import { useParams, useSearchParams, useNavigate, Link } from 'react-router-dom';
import mockChats from "../mockData/mockChats.js"
import ChatList from "./ChatList.jsx"
import Chat from "./Chat.jsx"
import ChatMessageSender from "./ChatMessageSender.jsx";
import axios from 'axios';

const ChatPage = () => {

    const { user_uuid } = useParams();
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const [choosenChat, setChoosenChat] = useState(0);
    const [chats, setChats] = useState([]);
    const [messages, setMessages] = useState([]);
    const [messageForAnswer, setMessageForAnswer] = useState({message_id: -1});
    const [blockAll, setBlockAll] = useState(true);
    const [blockChatSwitch, setBlockChatSwitch] = useState(false);
    const [blockSendMessage, setBlockSendMessage] = useState(false);
    const [chatWasSwitchedBeforeGettingMessage, setChatWasSwitchedBeforeGettingMessage] = useState(false);

    const api_adress = "";

    const getChats = async () => {
        try {
            const responce = axios.get(`http://${api_adress}/all-user-chats/${user_uuid}`);
            setChats(responce.data);
            setBlockAll(false);
        } catch (err) {
            alert(err.message)
        }
    };
    const getMessages = async () => {
        try {
            const responce = axios.get(`http://${api_adress}/chats/${choosenChat}?n=500`);
            setMessages(responce.data);
        } catch (err) {
            alert(err.message)
        }
    };
    const createDialog = async () => {
        try {
            const responce = axios.post(`http://${api_adress}/create-chat`, {
                user_uuid: user_uuid,
            });
            setChoosenChat(responce.data.chat_id);
        } catch (err) {
            alert(err.message)
        }
    };
    const sendMessage = async (messageText, answer_to) => {
        try {
            const responce = axios.post(`http://${api_adress}/create-message`, {
                user_uuid: user_uuid,
                chat_id: choosenChat,
                text: messageText,
                answer_to: answer_to,
                is_bot: false
            });
            // setMessages(responce.data);
        } catch (err) {
            alert(err.message)
        }
    };
    const reactMessage = async () => {
        try {
            const responce = axios.post(`http://${api_adress}/react`);
            setMessages(responce.data);
        } catch (err) {
            alert(err.message)
        }
    };
    
    const sendMessageForMessageSender = async (messageText) => {
        chats.push({
            chat_id: -1,
            title: "Новый чат",
            messages: [
                {
                    message_id: 0,
                    is_bot: false,
                    text: messageText,
                    answer_to: NaN,
                    react: 0
                }
            ]
        })
        if (choosenChat === 0) {
            createDialog();
        } else if (messageForAnswer.message_id == -1) {
            sendMessage();
        } else {
            sendMessage();
        }

    };

    useEffect(() => {
        setBlockAll(true);
        if (user_uuid in mockChats) {
              setChats(mockChats[user_uuid]);
        } else {
            navigate(`/`);
        }

        const chat_id = searchParams.get('chat_id');
        if (chat_id && !(/^\d+$/.test(chat_id))) {
            navigate(`/${user_uuid}`);
            setBlockAll(false);
        }

        setChoosenChat(Number(searchParams.get('chat_id')))
    }, []);

    useEffect(() => {
        if (chats.some((chat) => (chat.chat_id === choosenChat))) {
            navigate(`/${user_uuid}?chat_id=${choosenChat}`);
        } else {
            navigate(`/${user_uuid}`);
        }
        setBlockAll(false);
    }, [choosenChat])

    return (blockAll ?
        <div>
            <p>Загрузка...</p>
        </div> :
        <div>
            <ChatList chats={chats} setChoosenChat={setChoosenChat}></ChatList>
            {(!(chats.find((chat) => (chat.chat_id === choosenChat)))) ?
                <h2>Опишите свою проблему</h2> :
                <Chat
                    chatMessages={chats.find((chat) => (chat.chat_id === choosenChat)).messages}
                    setMessageForAnswer={setMessageForAnswer}
                    reactMessage={reactMessage}
                />
            }
            <ChatMessageSender
                SendMessage={sendMessageForMessageSender}
                setMessageForAnswer={setMessageForAnswer}
                messageForAnswer={messageForAnswer}
            />
        </div>
    );
};

export default ChatPage;