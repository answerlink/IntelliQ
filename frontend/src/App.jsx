import React, { useState } from 'react';
import { Layout, Tabs, Button, Space } from 'antd';
import { PlusOutlined, RobotOutlined, MessageOutlined } from '@ant-design/icons';
import ChatBox from './components/ChatBox';
import AIChatBox from './components/AIChatBox';
import './App.css';

const { Header, Content } = Layout;

function createNewChat(id, type = 'business') {
  return {
    id,
    title: type === 'business' ? `业务对话${id}` : `AI对话${id}`,
    type: type,
    messages: [],
    participants: { user: '你', ai: type === 'business' ? '业务助手' : 'AI助手' },
  };
}

export default function App() {
  const [chats, setChats] = useState([
    createNewChat(1, 'business'),
    createNewChat(2, 'ai')
  ]);
  const [activeKey, setActiveKey] = useState('1');
  const [nextId, setNextId] = useState(3);

  const addChat = (type = 'business') => {
    const id = String(nextId);
    setChats([...chats, createNewChat(id, type)]);
    setActiveKey(id);
    setNextId(nextId + 1);
  };

  const removeChat = (targetKey) => {
    let newActiveKey = activeKey;
    let lastIndex = -1;
    chats.forEach((chat, i) => {
      if (chat.id === targetKey) lastIndex = i - 1;
    });
    const newChats = chats.filter(chat => chat.id !== targetKey);
    if (newChats.length && newActiveKey === targetKey) {
      newActiveKey = newChats[lastIndex >= 0 ? lastIndex : 0].id;
    }
    setChats(newChats);
    setActiveKey(newActiveKey);
  };

  const updateChat = (id, updater) => {
    setChats(chats => chats.map(chat => chat.id === id ? updater(chat) : chat));
  };

  const renderChatComponent = (chat) => {
    if (chat.type === 'ai') {
      return (
        <AIChatBox
          chat={chat}
          updateChat={updater => updateChat(chat.id, updater)}
        />
      );
    } else {
      return (
        <ChatBox
          chat={chat}
          updateChat={updater => updateChat(chat.id, updater)}
        />
      );
    }
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ background: '#fff', borderBottom: '1px solid #eee', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ fontWeight: 'bold', fontSize: 20 }}>电信业务AI问答系统</div>
        <Space>
          <Button 
            icon={<RobotOutlined />} 
            type="primary" 
            onClick={() => addChat('business')}
          >
            新业务对话
          </Button>
          <Button 
            icon={<MessageOutlined />} 
            type="default" 
            onClick={() => addChat('ai')}
          >
            新AI对话
          </Button>
        </Space>
      </Header>
      <Content style={{ padding: 24, background: '#f5f6fa' }}>
        <Tabs
          type="editable-card"
          activeKey={activeKey}
          onChange={setActiveKey}
          onEdit={removeChat}
          hideAdd
          items={chats.map(chat => ({
            key: chat.id,
            label: (
              <span>
                {chat.type === 'business' ? <RobotOutlined /> : <MessageOutlined />}
                {' '}{chat.title}
              </span>
            ),
            children: renderChatComponent(chat),
          }))}
        />
      </Content>
    </Layout>
  );
} 