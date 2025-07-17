/**
 * 前端应用配置
 */

// 从环境变量获取配置，提供默认值
const config = {
  // API配置
  apiBaseUrl: process.env.REACT_APP_API_BASE_URL || 'http://localhost:5050',
  
  // 环境配置
  env: process.env.REACT_APP_ENV || 'development',
  
  // 调试模式
  debug: process.env.REACT_APP_DEBUG === 'true',
  
  // 是否为开发环境
  isDevelopment: process.env.NODE_ENV === 'development',
  
  // 是否为生产环境
  isProduction: process.env.NODE_ENV === 'production',
  
  // API路径前缀
  apiPrefix: '/api'
};

// 开发环境下打印配置信息
if (config.debug && config.isDevelopment) {
  console.log('📋 前端配置信息:', config);
}

export default config; 