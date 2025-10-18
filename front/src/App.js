import './App.css';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ChatPage from './Blocks/ChatPage';
import UUID_Choice from './Blocks/UUID_Choice';

function App() {
  return (
    <Router>
        <Routes>
          <Route path="/:user_uuid" element={<ChatPage />} />
          <Route path="/" element={<UUID_Choice />} />
        </Routes>
    </Router>
  );
}

export default App;
