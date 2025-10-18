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
    const [generatingMessage, setGeneratingMessage] = useState(false);
    const [blockChatSwitch, setBlockChatSwitch] = useState(false);
    const [blockSendMessage, setBlockSendMessage] = useState(false);
    const [chatWasSwitchedBeforeGettingMessage, setChatWasSwitchedBeforeGettingMessage] = useState(false);

    const api_adress = "127.0.0.1:8000";

    const reactMessage = async (message, reaction) => {
        try {
            const responce = await axios.patch(`http://${api_adress}/react`, {
                message_id: message.message_id,
                react: reaction
            });
            const updatedMessages = messages.map(messageInMap =>
                messageInMap.message_id === message.messageId ?
                {...messageInMap, react: reaction} :
                messageInMap
            );
            setMessages(updatedMessages);
        } catch (err) {
            alert(err.message)
        }
    };
    
    const sendMessageForMessageSender = async (messageText) => {
        
        if (choosenChat === 0) {
            try {
                const responceToCreate = await axios.post(`http://${api_adress}/create-chat`, {
                    user_uuid: user_uuid,
                });

                navigate(`/${user_uuid}?chat=${responceToCreate.chat_id}`);

                const responceToMessage = await axios.post(`http://${api_adress}/create-message`, {
                    user_uuid: user_uuid,
                    chat_id: responceToCreate.chat_id,
                    text: messageText,
                    answer_to: NaN,
                    is_bot: false
                });
            } catch (err) {
                alert(err.message)
            }
        } else if (messageForAnswer.message_id == -1) {
            try {
                const responce = await axios.post(`http://${api_adress}/create-message`, {
                    user_uuid: user_uuid,
                    chat_id: responce.chat_id,
                    text: messageText,
                    answer_to: NaN,
                    is_bot: false
                });
                setGeneratingMessage(true);
                const responceToMessage = await axios.get(`http://${api_adress}/create-llm-message`, {
                    chat_id: choosenChat
                });
                if (responceToMessage.data.chat_id == choosenChat) {
                    setMessages([...messages, responceToMessage.data]);
                    setGeneratingMessage(false);
                }
            } catch (err) {
                alert(err.message)
            }
        } else {
            try {
                const responce = await axios.post(`http://${api_adress}/create-message`, {
                    user_uuid: user_uuid,
                    chat_id: responce.chat_id,
                    text: messageText,
                    answer_to: messageForAnswer.message_id,
                    is_bot: false
                });
                setGeneratingMessage(true);
                const responceToMessage = await axios.get(`http://${api_adress}/create-llm-message`, {
                    chat_id: choosenChat
                });
                if (responceToMessage.data.chat_id == choosenChat) {
                    setMessages([...messages, responceToMessage.data]);
                    setGeneratingMessage(false);
                }
            } catch (err) {
                alert(err.message)
            }
        }

    };

    useEffect(() => {

        const initPage = async () => {
            setBlockAll(true);
            
            try {
                const responce = axios.get(`http://${api_adress}/all-user-chats/${user_uuid}`);
                setChats(responce.data);
            } catch (err) {
                alert(err.message)
            }
            
            // if (user_uuid in mockChats) {
            //     setChats(mockChats[user_uuid]);
            // } else {
            //     navigate(`/`);
            // }
        };

        initPage();

    }, []);

    useEffect(() => {

        const initChat = () => {
            const chat_id = searchParams.get('chat_id');
            if (chat_id && !(/^\d+$/.test(chat_id))) {
                navigate(`/${user_uuid}`);
                setBlockAll(false);
            }
            setChoosenChat(Number(searchParams.get('chat_id')))
        };

        initChat();

    }, [chats]);

    useEffect(() => {

        const initMessages = async () => {
            if (!(chats.some((chat) => (chat.chat_id === choosenChat)))) {
                navigate(`/${user_uuid}`);

                setBlockAll(false);
            }
            setGeneratingMessage(false);

            try {
                const responce = axios.get(`http://${api_adress}/chats/${choosenChat}?n=500`);
                setMessages(responce.data);
                setGeneratingMessage(responce.is_generating);
                if (generatingMessage) {
                    const responceToMessage = await axios.get(`http://${api_adress}/create-llm-message`, {
                        chat_id: choosenChat
                    });
                
                    if (responceToMessage.data.chat_id == choosenChat) {
                        setMessages([...messages, responceToMessage.data]);
                        setGeneratingMessage(false);
                    }
                    setMessages([...messages, responceToMessage.data]);
                    setGeneratingMessage(false);
                }
            } catch (err) {
                alert(err.message)
            }
            

            setBlockAll(false);
        };

        initMessages();
    }, [choosenChat]);

    const findChat = () => {
        if (!chats) {
            return undefined;
        }

        const foundChat = chats.find((chat) => (chat.chat_id === choosenChat));

        return (foundChat && choosenChat && foundChat != {}) ? foundChat : undefined
    }

    return (blockAll || !chats ?
        <div>
            <p>Загрузка...</p>
        </div> :
        <div className="chatPage">
            <ChatList chats={chats} setChoosenChat={setChoosenChat} generatingMessage={generatingMessage}></ChatList>
            {!findChat() ?
                <h2 className="newChatQuestion">Опишите свою проблему</h2> :
                <Chat
                    chatMessages={findChat(choosenChat).messages}
                    setMessageForAnswer={setMessageForAnswer}
                    reactMessage={reactMessage}
                />
            }
            {/* <div>
                {notes.map((item) => 
                (<div>
                {Object.entries(item).map(([key, value]) => (
                    <p key={key}>
                        <strong>{key}:</strong> {value}
                    </p>
                    ))}
                </div>)
                )}
            </div> */}
            <ChatMessageSender
                SendMessage={sendMessageForMessageSender}
                setMessageForAnswer={setMessageForAnswer}
                messageForAnswer={messageForAnswer}
            />
        </div>
    );
};

export default ChatPage;