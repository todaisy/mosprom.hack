import React, {useState, useEffect} from "react";
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const UUID_Choice = () => {
    const [User_uuid, setUser_uuid] = useState('');
    const navigate = useNavigate();

 
    const api_adress = "";

    useEffect(() => {
        const createUser = async () => {
            try {
                const responce = axios.post(`http://${api_adress}/create-user`, {});
                setUser_uuid(responce.data.user_uuid);
                navigate(`/${User_uuid.trim()}`);
            } catch (err) {
                alert(err.message)
            }
        };
    });

    const handleSubmit = (e) => {
        e.preventDefault();
        if (User_uuid.trim()) {
            navigate(`/${User_uuid.trim()}`);
        }
    };

     return (
        <div>
            <h1>Главная страница</h1>
            <p>Введите id пользователя для перехода на соответствующую страницу</p>
      
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="user_uuid">ID пользователя:</label>
                    <input
                        id="user_uuid"
                        type="text"
                        value={User_uuid}
                        onChange={(e) => setUser_uuid(e.target.value)}
                        placeholder="Введите id пользователя..."
                        required
                    />
                </div>
        
                <button type="submit" >Перейти</button>
            </form>

      
        </div>
    );
};

export default UUID_Choice;