import React, { useState, useRef, useEffect } from 'react';
import { Input, Button, Spin, message as antdMsg, Space, Typography, Badge } from 'antd';
import MessageBubble from './MessageBubble';
import { streamLLMChat, generateSessionId, resetSession } from '../api/aiApi';

const { Text } = Typography;
const { TextArea } = Input;

const WELCOME_MSG = '您好！我是中国电信客服助手小天，很高兴为您服务。您可以咨询流量查询、宽带报修、套餐变更、副卡申请等业务，也可以与我闲聊。';

export default function AIChatBox({ chat, updateChat }) {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [streaming, setStreaming] = useState(false);
  const [currentStream, setCurrentStream] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [businessMode, setBusinessMode] = useState(false);
  const inputRef = useRef();
  const [welcomed, setWelcomed] = useState(false);

  // 初始化会话ID
  useEffect(() => {
    if (!sessionId) {
      const newSessionId = generateSessionId();
      setSessionId(newSessionId);
      console.log('生成新的会话ID:', newSessionId);
    }
  }, [sessionId]);

  // 只在Tab初始渲染时输出欢迎语
  useEffect(() => {
    if (!welcomed && chat.messages.length === 0) {
      updateChat(chat => ({
        ...chat,
        messages: [
          {
            id: Date.now(),
            role: 'ai',
            text: WELCOME_MSG,
            status: 'welcome'
          }
        ]
      }));
      setWelcomed(true);
    }
    // eslint-disable-next-line
  }, [chat.messages, welcomed]);

  // 重置会话
  const handleResetSession = async () => {
    try {
      if (sessionId) {
        await resetSession(sessionId);
      }
      const newSessionId = generateSessionId();
      setSessionId(newSessionId);
      setBusinessMode(false);
      console.log('会话已重置，新会话ID:', newSessionId);
      antdMsg.success('会话已重置');
    } catch (error) {
      console.error('重置会话失败:', error);
      antdMsg.error('重置会话失败');
    }
  };

  // 主输入处理：集成业务流程管理
  const handleSend = async () => {
    if (!input.trim() || !sessionId) return;
    
    const userMsg = {
      id: Date.now(),
      role: 'user',
      text: input.trim()
    };
    updateChat(chat => ({ ...chat, messages: [...chat.messages, userMsg] }));
    setStreaming(true);
    
    const aiMsg = {
      id: Date.now() + 1,
      role: 'ai',
      text: '',
      status: 'thinking'
    };
    updateChat(chat => ({ ...chat, messages: [...chat.messages, aiMsg] }));
    
    try {
      const eventSource = streamLLMChat(
        chat.messages.map(msg => ({ role: msg.role, content: msg.text })),
        input.trim(),
        sessionId,
        (token) => {
          // 流式渲染纯文本增量
          updateChat(chat => {
            const newMessages = [...chat.messages];
            const lastMsg = newMessages[newMessages.length - 1];
            if (lastMsg && lastMsg.role === 'ai') {
              lastMsg.text += token;  // 直接拼接纯文本增量
              lastMsg.status = 'streaming';
            }
            return { ...chat, messages: newMessages };
          });
        },
        (error) => {
          console.error('AI回复错误:', error);
          antdMsg.error(`AI回复失败: ${error}`);
          updateChat(chat => {
            const newMessages = [...chat.messages];
            const lastMsg = newMessages[newMessages.length - 1];
            if (lastMsg && lastMsg.role === 'ai') {
              lastMsg.status = 'error';
              lastMsg.text = `抱歉，AI回复出现错误: ${error}`;
            }
            return { ...chat, messages: newMessages };
          });
          setStreaming(false);
        },
        (returnedSessionId) => {
          console.log('AI流式响应完成，会话ID:', returnedSessionId);
          setStreaming(false);
          
          // 更新会话ID（如果服务器返回了新的）
          if (returnedSessionId && returnedSessionId !== sessionId) {
            setSessionId(returnedSessionId);
          }
          
          updateChat(chat => {
            const newMessages = [...chat.messages];
            const lastMsg = newMessages[newMessages.length - 1];
            if (lastMsg && lastMsg.role === 'ai') {
              lastMsg.status = 'completed';
              
              // 检查是否包含业务相关内容，启用业务模式指示
              const businessKeywords = ['流量', '宽带', '套餐', '副卡', '查询', '报修', '变更', '申请'];
              const hasBusinessContent = businessKeywords.some(keyword => 
                lastMsg.text.includes(keyword)
              );
              if (hasBusinessContent) {
                setBusinessMode(true);
              }
            }
            return { ...chat, messages: newMessages };
          });
        }
      );
      setCurrentStream(eventSource);
    } catch (error) {
      console.error('streamLLMChat调用异常:', error);
      antdMsg.error('AI接口调用失败');
      updateChat(chat => {
        const newMessages = [...chat.messages];
        const lastMsg = newMessages[newMessages.length - 1];
        if (lastMsg && lastMsg.role === 'ai') {
          lastMsg.status = 'error';
          lastMsg.text = '抱歉，AI接口调用失败';
        }
        return { ...chat, messages: newMessages };
      });
      setStreaming(false);
    } finally {
      setInput('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  useEffect(() => {
    return () => {
      if (currentStream) {
        currentStream.close();
      }
    };
  }, [currentStream]);

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* 状态栏 */}
      <div style={{ 
        padding: '8px 16px', 
        borderBottom: '1px solid #f0f0f0',
        backgroundColor: '#fafafa',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <Space>
          <Badge 
            status={businessMode ? "processing" : "default"} 
            text={businessMode ? "业务模式" : "聊天模式"}
          />
          <Text type="secondary" style={{ fontSize: '12px' }}>
            会话ID: {sessionId ? sessionId.slice(-8) : 'loading...'}
          </Text>
        </Space>
        <Button 
          size="small" 
          type="link" 
          onClick={handleResetSession}
          disabled={streaming}
        >
          重置会话
        </Button>
      </div>

      {/* 消息列表 */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '16px' }}>
        {chat.messages.map((message) => (
          <MessageBubble
            key={message.id}
            message={message}
            isStreaming={streaming && message.role === 'ai' && message.status === 'streaming'}
          />
        ))}
        {loading && (
          <div style={{ textAlign: 'center', padding: '20px' }}>
            <Spin size="large" />
            <div style={{ marginTop: '8px' }}>
              <Text type="secondary">AI正在思考中...</Text>
            </div>
          </div>
        )}
      </div>

      {/* 输入区域 */}
      <div style={{ padding: '16px', borderTop: '1px solid #f0f0f0' }}>
        <Space.Compact style={{ width: '100%' }}>
          <TextArea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={businessMode ? "请继续提供业务信息或提出新问题..." : "请输入您的问题..."}
            autoSize={{ minRows: 1, maxRows: 4 }}
            disabled={loading || streaming}
            style={{ flex: 1 }}
          />
          <Button
            type="primary"
            onClick={handleSend}
            loading={loading || streaming}
            disabled={!input.trim() || !sessionId}
            style={{ width: '80px' }}
          >
            发送
          </Button>
        </Space.Compact>
        <div style={{ marginTop: '8px' }}>
          <Text type="secondary" style={{ fontSize: '12px' }}>
            智能业务助手 - 支持流量查询、宽带报修、套餐变更等业务办理，按Enter发送，Shift+Enter换行
          </Text>
        </div>
      </div>
    </div>
  );
} 