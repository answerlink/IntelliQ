import React from 'react';

export default function MessageBubble({ message, msg, isStreaming }) {
  // 兼容不同的参数名
  const msgData = message || msg;
  const isAI = msgData.role === 'ai';
  
  return (
    <div style={{
      display: 'flex',
      justifyContent: isAI ? 'flex-start' : 'flex-end',
      marginBottom: 8
    }}>
      <div style={{
        background: isAI ? '#f6fff6' : '#e6f7ff',
        color: '#222',
        borderRadius: 8,
        padding: '8px 16px',
        maxWidth: 400,
        boxShadow: '0 1px 4px #eee',
        position: 'relative'
      }}>
        <div style={{ fontWeight: isAI ? 'bold' : 'normal', marginBottom: 2 }}>
          {isAI ? 'AI助手' : '你'}
        </div>
        <div>
          {msgData.text}
          {isStreaming && (
            <span style={{ 
              display: 'inline-block',
              width: '8px',
              height: '8px',
              backgroundColor: '#1890ff',
              borderRadius: '50%',
              marginLeft: '4px',
              animation: 'pulse 1s infinite'
            }} />
          )}
        </div>
        {msgData.status && (
          <div style={{ 
            fontSize: '12px', 
            color: '#999', 
            marginTop: '4px',
            fontStyle: 'italic'
          }}>
            {msgData.status}
          </div>
        )}
      </div>
      <style jsx>{`
        @keyframes pulse {
          0% { opacity: 1; }
          50% { opacity: 0.5; }
          100% { opacity: 1; }
        }
      `}</style>
    </div>
  );
} 