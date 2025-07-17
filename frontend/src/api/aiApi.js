import axios from 'axios';
import config from '../config/config';

export const BASE_URL = config.apiBaseUrl;

export function sendMessage(api, params) {
  return axios.post(BASE_URL + api, params);
}

export function getMockSlots() {
  return axios.get(BASE_URL + config.apiPrefix + '/mock_slots');
}

// 流式AI聊天接口（支持业务流程）
export function streamLLMChat(messages, userInput, sessionId, onData, onError, onComplete) {
  const controller = new AbortController();
  
  if (config.debug) {
    console.log('开始流式AI聊天', { userInput, sessionId, apiUrl: `${BASE_URL}${config.apiPrefix}/llm_chat` });
  }
  
  fetch(`${BASE_URL}${config.apiPrefix}/llm_chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Accept': 'text/event-stream; charset=utf-8'
    },
    body: JSON.stringify({
      messages: messages,
      user_input: userInput,
      session_id: sessionId
    }),
    signal: controller.signal
  })
  .then(response => {
    if (config.debug) {
      console.log('收到响应', { 
        status: response.status, 
        contentType: response.headers.get('content-type'),
        sessionId: response.headers.get('x-session-id')
      });
    }
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    // 获取会话ID
    const returnedSessionId = response.headers.get('x-session-id');
    if (returnedSessionId && config.debug) {
      console.log('获取到会话ID:', returnedSessionId);
    }
    
    const reader = response.body.getReader();
    // 显式指定UTF-8解码器，使用非严格模式处理不完整字符
    const decoder = new TextDecoder('utf-8', { fatal: false, ignoreBOM: true });
    let buffer = '';
    let contentCount = 0;
    let totalContent = '';
    
    function readStream() {
      return reader.read().then(({ done, value }) => {
        if (done) {
          if (config.debug) {
            console.log('流式读取完成', { 
              contentCount, 
              totalContent: totalContent.substring(0, 100) + '...',
              sessionId: returnedSessionId
            });
          }
          onComplete && onComplete(returnedSessionId);
          return;
        }
        
        try {
          // 解码二进制数据为UTF-8字符串
          const chunk = decoder.decode(value, { stream: true });
          buffer += chunk;
          
          // 按行处理，确保完整的SSE消息
          const lines = buffer.split('\n');
          buffer = lines.pop() || ''; // 保留不完整的最后一行
          
          for (const line of lines) {
            const trimmedLine = line.trim();
            
            if (trimmedLine.startsWith('data: ')) {
              const data = trimmedLine.slice(6);
              
              if (data === '[DONE]') {
                if (config.debug) {
                  console.log('收到[DONE]标记，结束流式处理');
                }
                onComplete && onComplete(returnedSessionId);
                return;
              } else if (data.startsWith('[ERROR]')) {
                const errorMsg = data.slice(8);
                console.error('收到错误', { errorMsg });
                onError && onError(errorMsg);
                return;
              } else if (data.trim()) {
                contentCount++;
                totalContent += data;
                
                // 记录接收到的内容详情（仅在开发模式下）
                if (config.debug) {
                  console.log(`接收内容 #${contentCount}:`, { 
                    content: data, 
                    length: data.length
                  });
                }
                
                // 直接传递解码后的文本增量
                onData && onData(data);
              }
            }
          }
        } catch (error) {
          console.error('UTF-8解码错误', { 
            error: error.message, 
            value: value ? Array.from(value.slice(0, 20)) : null // 显示前20个字节
          });
          onError && onError(`解码错误: ${error.message}`);
          return;
        }
        
        return readStream();
      });
    }
    
    return readStream();
  })
  .catch(error => {
    console.error('fetch错误', { error: error.message, stack: error.stack });
    onError && onError(error.message);
  });
  
  return {
    close: () => controller.abort()
  };
}

// 普通AI聊天接口（非流式）
export function chatWithLLM(messages, userInput, sessionId) {
  return axios.post(BASE_URL + config.apiPrefix + '/llm_chat', {
    messages: messages,
    user_input: userInput,
    session_id: sessionId
  });
}

// 生成会话ID
export function generateSessionId() {
  return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

// 重置会话
export function resetSession(sessionId) {
  return axios.post(BASE_URL + config.apiPrefix + '/reset_session', {
    session_id: sessionId
  });
}

// 健康检查
export function healthCheck() {
  return axios.get(BASE_URL + config.apiPrefix + '/health');
}