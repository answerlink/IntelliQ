import React, { useState, useRef } from 'react';
import { Input, Button, Spin, message as antdMsg, Space, Typography } from 'antd';
import MessageBubble from './MessageBubble';
import SlotFiller from './SlotFiller';
import KnowledgeCitation from './KnowledgeCitation';
import { sendMessage, getMockSlots } from '../api/aiApi';
import { detectIntent } from '../utils/intentMap';

const { Text } = Typography;

// 业务场景格式化回复
function formatBusinessReply(intent, data, slotValues = {}) {
  if (!data) return '处理完成';
  // 流量查询
  if (intent.businessKey === 'traffic_query') {
    return `本月总流量：${data.total_traffic}，已用：${data.used_traffic}，剩余：${data.remain_traffic}，状态：${data.status}`;
  }
  // 宽带报修
  if (intent.businessKey === 'broadband_repair') {
    return `宽带报修工单已创建，联系电话：${data.phone}，账号：${data.broadband_account}，地址：${data.address}，故障类型：${data.fault_type}，工单状态：${data.status || '已受理'}。${data.remark || ''}`;
  }
  // 套餐变更
  if (intent.businessKey === 'package_change') {
    return `套餐变更成功！原套餐：${data.old_package || ''}，新套餐：${data.new_package || data.package_type || ''}，生效时间：${data.effective_time || ''}，月费：${data.monthly_fee || ''}，状态：${data.status || ''}。${data.remark || ''}`;
  }
  // 副卡办理
  if (intent.businessKey === 'sub_card_apply') {
    return `副卡办理成功！主卡：${data.main_phone}，副卡张数：${data.sub_card_count}，套餐：${data.sub_package_type}，副卡号码：${Array.isArray(data.sub_cards) ? data.sub_cards.join('、') : ''}，月费：${data.monthly_fee}，总月费：${data.total_monthly_fee}，办理时间：${data.apply_time}。${data.remark || ''}`;
  }
  // 实名认证
  if (intent.businessKey === 'realname_query') {
    if (data.status === '已实名' || data.realname_status === '已实名') {
      return `实名认证结果：已实名，姓名：${data.name || ''}，证件号：${data.id_number || ''}`;
    } else if (data.status === '未实名' || data.realname_status === '未实名') {
      return '实名认证结果：未实名。';
    } else {
      return data.remark || data.msg || '实名认证结果：' + (data.status || data.realname_status || '未知');
    }
  }
  // 话费账单
  if (intent.businessKey === 'account_bill') {
    return `账单周期：${data.bill_period || ''}，应缴：${data.amount_due || ''}元，已缴：${data.amount_paid || ''}元，状态：${data.status || ''}`;
  }
  // 积分查询
  if (intent.businessKey === 'points_query') {
    return `当前积分：${data.points || ''}分，有效期至：${data.expire_date || ''}`;
  }
  // 停机保号
  if (intent.businessKey === 'suspend_apply') {
    return `停机保号办理成功，停机时长：${data.suspend_duration || ''}月，生效时间：${data.effective_time || ''}，状态：${data.status || ''}`;
  }
  // 发票申请
  if (intent.businessKey === 'invoice_apply') {
    return `发票申请成功，类型：${data.invoice_type || ''}，邮寄地址：${data.mailing_address || ''}，状态：${data.status || ''}`;
  }
  // 套餐余量
  if (intent.businessKey === 'package_balance') {
    return `套餐余量：语音${data.voice_balance || ''}，流量${data.data_balance || ''}，短信${data.sms_balance || ''}，套餐：${data.package_name || ''}，到期：${data.expire_date || ''}`;
  }
  // 充值缴费
  if (intent.businessKey === 'recharge') {
    const amount = data.amount || slotValues.amount || '';
    const payment_method = data.payment_method || slotValues.payment_method || '';
    const status = data.status || '充值成功';
    return `充值成功，金额：${amount}元，方式：${payment_method}，状态：${status}`;
  }
  // 号码过户
  if (intent.businessKey === 'number_transfer') {
    return `号码过户成功，原号码：${data.original_phone || ''}，新机主证件号：${data.new_owner_id || ''}，状态：${data.status || ''}`;
  }
  // 国际漫游
  if (intent.businessKey === 'roaming_enable') {
    return `国际漫游已开通，国家：${data.roaming_country || ''}，起止：${data.start_date || ''}~${data.end_date || ''}，状态：${data.status || ''}`;
  }
  // 积分兑换
  if (intent.businessKey === 'points_exchange') {
    const exchange_type = data.exchange_type || slotValues.exchange_type || '';
    const exchange_quantity = data.exchange_quantity || slotValues.exchange_quantity || '';
    const status = data.status || '兑换成功';
    return `积分兑换成功，类型：${exchange_type}，数量：${exchange_quantity}，状态：${status}`;
  }
  // 通知订阅
  if (intent.businessKey === 'notification_subscribe') {
    return `通知订阅成功，类型：${data.notification_type || ''}，状态：${data.status || ''}`;
  }
  // 套餐退订
  if (intent.businessKey === 'package_unsubscribe') {
    return `套餐退订成功，类型：${data.package_type || ''}，状态：${data.status || ''}`;
  }
  // 宽带升级
  if (intent.businessKey === 'broadband_upgrade') {
    return `宽带升级成功，账号：${data.broadband_account || ''}，类型：${data.upgrade_type || ''}，状态：${data.status || ''}`;
  }
  // 停/复机
  if (intent.businessKey === 'stop_resume') {
    return `业务办理成功，操作：${data.action || ''}，状态：${data.status || ''}`;
  }
  // 密码重置
  if (intent.businessKey === 'password_reset') {
    return `密码重置成功，状态：${data.status || ''}`;
  }
  // 对话日志
  if (intent.businessKey === 'chat_log') {
    return data.log || data.remark || data.msg || '对话日志操作完成';
  }
  // 服务评价
  if (intent.businessKey === 'feedback') {
    return `服务评价提交成功，评分：${data.score || ''}，内容：${data.comment || ''}`;
  }
  // 投诉工单
  if (intent.businessKey === 'complaint') {
    return `投诉已受理，工单号：${data.complaint_id || ''}，类型：${data.complaint_type || ''}，优先级：${data.priority || ''}，预计处理时长：${data.estimated_time || ''}，状态：${data.status || ''}。${data.remark || ''}`;
  }
  // 增值业务
  if (intent.businessKey === 'value_added') {
    return `增值业务${data.service_name || ''}${data.action || ''}，状态：${data.status || ''}`;
  }
  // FAQ
  if (intent.businessKey === 'faq') {
    return data.answer || data.msg || '这是一个模拟FAQ答案。';
  }
  // 地址变更
  if (intent.businessKey === 'address_modify') {
    const new_address = data.new_address || slotValues.new_address || '';
    const status = data.status || '修改成功';
    return `通信地址修改成功，新地址：${new_address}，状态：${status}`;
  }
  // 兜底
  return data.remark || data.answer || data.msg || '处理完成';
}

export default function ChatBox({ chat, updateChat }) {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [mockSlots, setMockSlots] = useState(null);
  const [pendingSlots, setPendingSlots] = useState([]);
  const [slotValues, setSlotValues] = useState({});
  const [currentIntent, setCurrentIntent] = useState(null);
  const inputRef = useRef();

  React.useEffect(() => {
    getMockSlots().then(res => setMockSlots(res.data.data)).catch(() => {});
  }, []);

  const handleSend = async (customValues, customIntent) => {
    let userInput = input;
    if (!userInput && !customValues) return;
    if (!customIntent) {
      const userMsg = { id: Date.now(), role: 'user', text: userInput || '[补全卡槽]' };
      updateChat(chat => ({ ...chat, messages: [...chat.messages, userMsg] }));
    }
    setInput('');
    setLoading(true);

    const intent = customIntent || detectIntent(userInput);
    setCurrentIntent(intent);
    let values = customValues || slotValues;
    let slotDefs = (mockSlots && intent.businessKey && mockSlots[intent.businessKey]?.slots) || {};
    // 以mock_slots为准，动态判断所有required字段
    let requiredKeys = Object.entries(slotDefs)
      .filter(([k, v]) => v.required)
      .map(([k]) => k);
    let missing = requiredKeys.filter(key => !values[key]);
    const askSlots = missing.slice(0, 2);
    if (process.env.NODE_ENV !== 'production') {
      console.log('【DEBUG】意图:', intent, '已填参数:', values, '缺失卡槽:', missing);
    }
    if (askSlots.length > 0) {
      setPendingSlots(askSlots);
      setSlotValues(values);
      setLoading(false);
      return;
    }
    try {
      const params = {};
      requiredKeys.forEach(key => { params[key] = values[key]; });
      if (process.env.NODE_ENV !== 'production') {
        console.log('【DEBUG】最终请求参数:', params);
      }
      const res = await sendMessage(intent.api, params);
      const aiMsg = {
        id: Date.now() + 1,
        role: 'ai',
        text: formatBusinessReply(intent, res.data.data, values),
        status: '处理完成',
        citations: res.data.data.citations || [],
      };
      updateChat(chat => ({ ...chat, messages: [...chat.messages, aiMsg] }));
      setSlotValues({});
      setPendingSlots([]);
    } catch (e) {
      antdMsg.error('AI接口调用失败');
    }
    setLoading(false);
  };

  const handleSlotFill = (values) => {
    const merged = { ...slotValues, ...values };
    setSlotValues(merged);
    setPendingSlots([]);
    setInput('');
    setTimeout(() => handleSend(merged, currentIntent), 0);
  };

  return (
    <div style={{ maxWidth: 700, margin: '0 auto', background: '#fff', borderRadius: 8, boxShadow: '0 2px 8px #eee', padding: 24, minHeight: 500 }}>
      <div style={{ marginBottom: 16 }}>
        <Text strong>{chat.title}</Text> <Text type="secondary">参与人：你 / AI助手</Text>
      </div>
      <div style={{ minHeight: 320, marginBottom: 16 }}>
        {chat.messages.map(msg => (
          <MessageBubble key={msg.id} message={msg} />
        ))}
        {loading && <Spin tip="AI处理中..." />}
      </div>
      {pendingSlots.length > 0 && mockSlots && currentIntent &&
        mockSlots[currentIntent.businessKey] && mockSlots[currentIntent.businessKey].slots && (
        <SlotFiller
          slotInfo={mockSlots[currentIntent.businessKey]}
          pendingSlots={pendingSlots}
          onSubmit={handleSlotFill}
        />
      )}
      <Space.Compact style={{ width: '100%' }}>
        <Input.TextArea
          ref={inputRef}
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="请输入您的问题或业务需求..."
          autoSize={{ minRows: 1, maxRows: 4 }}
          disabled={loading || pendingSlots.length > 0}
        />
        <Button type="primary" onClick={() => handleSend()} loading={loading} disabled={pendingSlots.length > 0}>发送</Button>
      </Space.Compact>
      {chat.messages.length > 0 && <KnowledgeCitation citations={chat.messages[chat.messages.length-1].citations} />}
    </div>
  );
} 