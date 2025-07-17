import { detectIntent, intentMap } from './intentMap';
import { sendMessage, getMockSlots } from '../api/aiApi';

// 业务场景格式化回复（与ChatBox一致，支持所有主流业务）
export function formatBusinessReply(intent, data, slotValues = {}) {
  if (!data) return '未查到业务数据，请检查参数或稍后重试。';
  if (intent.businessKey === 'traffic_query') {
    return `本月总流量：${data.total_traffic}，已用：${data.used_traffic}，剩余：${data.remain_traffic}，状态：${data.status}`;
  }
  if (intent.businessKey === 'broadband_repair') {
    return `宽带报修工单已创建，联系电话：${data.phone}，账号：${data.broadband_account}，地址：${data.address}，故障类型：${data.fault_type}，工单状态：${data.status || '已受理'}。${data.remark || ''}`;
  }
  if (intent.businessKey === 'package_change') {
    return `套餐变更成功！原套餐：${data.old_package || ''}，新套餐：${data.new_package || data.package_type || ''}，生效时间：${data.effective_time || ''}，月费：${data.monthly_fee || ''}，状态：${data.status || ''}。${data.remark || ''}`;
  }
  if (intent.businessKey === 'sub_card_apply') {
    return `副卡办理成功！主卡：${data.main_phone}，副卡张数：${data.sub_card_count}，套餐：${data.sub_package_type}，副卡号码：${Array.isArray(data.sub_cards) ? data.sub_cards.join('、') : ''}，月费：${data.monthly_fee}，总月费：${data.total_monthly_fee}，办理时间：${data.apply_time}。${data.remark || ''}`;
  }
  if (intent.businessKey === 'realname_query') {
    if (data.status === '已实名' || data.realname_status === '已实名') {
      return `实名认证结果：已实名，姓名：${data.name || ''}，证件号：${data.id_number || ''}`;
    } else if (data.status === '未实名' || data.realname_status === '未实名') {
      return '实名认证结果：未实名。';
    } else {
      return data.remark || data.msg || '实名认证结果：' + (data.status || data.realname_status || '未知');
    }
  }
  if (intent.businessKey === 'account_bill') {
    return `账单周期：${data.bill_period || ''}，应缴：${data.amount_due || ''}元，已缴：${data.amount_paid || ''}元，状态：${data.status || ''}`;
  }
  if (intent.businessKey === 'points_query') {
    return `当前积分：${data.points || ''}分，有效期至：${data.expire_date || ''}`;
  }
  if (intent.businessKey === 'suspend_apply') {
    return `停机保号办理成功，停机时长：${data.suspend_duration || ''}月，生效时间：${data.effective_time || ''}，状态：${data.status || ''}`;
  }
  if (intent.businessKey === 'invoice_apply') {
    return `发票申请成功，类型：${data.invoice_type || ''}，邮寄地址：${data.mailing_address || ''}，状态：${data.status || ''}`;
  }
  if (intent.businessKey === 'package_balance') {
    return `套餐余量：语音${data.voice_balance || ''}，流量${data.data_balance || ''}，短信${data.sms_balance || ''}，套餐：${data.package_name || ''}，到期：${data.expire_date || ''}`;
  }
  if (intent.businessKey === 'recharge') {
    const amount = data.amount || slotValues.amount || '';
    const payment_method = data.payment_method || slotValues.payment_method || '';
    const status = data.status || '充值成功';
    return `充值成功，金额：${amount}元，方式：${payment_method}，状态：${status}`;
  }
  if (intent.businessKey === 'number_transfer') {
    return `号码过户成功，原号码：${data.original_phone || ''}，新机主证件号：${data.new_owner_id || ''}，状态：${data.status || ''}`;
  }
  if (intent.businessKey === 'roaming_enable') {
    return `国际漫游已开通，国家：${data.roaming_country || ''}，起止：${data.start_date || ''}~${data.end_date || ''}，状态：${data.status || ''}`;
  }
  if (intent.businessKey === 'points_exchange') {
    const exchange_type = data.exchange_type || slotValues.exchange_type || '';
    const exchange_quantity = data.exchange_quantity || slotValues.exchange_quantity || '';
    const status = data.status || '兑换成功';
    return `积分兑换成功，类型：${exchange_type}，数量：${exchange_quantity}，状态：${status}`;
  }
  if (intent.businessKey === 'notification_subscribe') {
    return `通知订阅成功，类型：${data.notification_type || ''}，状态：${data.status || ''}`;
  }
  if (intent.businessKey === 'package_unsubscribe') {
    return `套餐退订成功，类型：${data.package_type || ''}，状态：${data.status || ''}`;
  }
  if (intent.businessKey === 'broadband_upgrade') {
    return `宽带升级成功，账号：${data.broadband_account || ''}，类型：${data.upgrade_type || ''}，状态：${data.status || ''}`;
  }
  if (intent.businessKey === 'stop_resume') {
    return `业务办理成功，操作：${data.action || ''}，状态：${data.status || ''}`;
  }
  if (intent.businessKey === 'password_reset') {
    return `密码重置成功，状态：${data.status || ''}`;
  }
  if (intent.businessKey === 'chat_log') {
    return data.log || data.remark || data.msg || '对话日志操作完成';
  }
  if (intent.businessKey === 'feedback') {
    return `服务评价提交成功，评分：${data.score || ''}，内容：${data.comment || ''}`;
  }
  if (intent.businessKey === 'complaint') {
    return `投诉已受理，工单号：${data.complaint_id || ''}，类型：${data.complaint_type || ''}，优先级：${data.priority || ''}，预计处理时长：${data.estimated_time || ''}，状态：${data.status || ''}。${data.remark || ''}`;
  }
  if (intent.businessKey === 'value_added') {
    return `增值业务${data.service_name || ''}${data.action || ''}，状态：${data.status || ''}`;
  }
  if (intent.businessKey === 'faq') {
    return data.answer || data.msg || '这是一个模拟FAQ答案。';
  }
  if (intent.businessKey === 'address_modify') {
    const new_address = data.new_address || slotValues.new_address || '';
    const status = data.status || '修改成功';
    return `通信地址修改成功，新地址：${new_address}，状态：${status}`;
  }
  // 兜底：输出原始data内容，便于debug
  return `【原始业务数据】${JSON.stringify(data)}`;
}

// 判断是否为业务意图（非FAQ）
export function isBusinessIntent(input) {
  const intent = detectIntent(input);
  return intent && intent.businessKey && intent.businessKey !== 'faq';
}

// 支持传入intent参数，补全流程时优先用传入的intent
export async function handleBusinessInput({ input, slotValues = {}, mockSlots, intent: currentIntent }) {
  const intent = currentIntent || detectIntent(input);
  if (!intent || !intent.api) return { type: 'faq', text: '未识别到业务意图' };
  if (intent.businessKey === 'faq') {
    return { type: 'faq', text: slotValues.question || input };
  }
  let slotDefs = (mockSlots && intent.businessKey && mockSlots[intent.businessKey]?.slots) || {};
  let requiredKeys = Object.entries(slotDefs).filter(([k, v]) => v.required).map(([k]) => k);
  let missing = requiredKeys.filter(key => !slotValues[key]);
  if (missing.length > 0) {
    return { type: 'slot', missing, intent, slotDefs };
  }
  // 调用后端API
  const params = {};
  requiredKeys.forEach(key => { params[key] = slotValues[key]; });
  const res = await sendMessage(intent.api, params);
  const plainText = formatBusinessReply(intent, res.data.data, slotValues);
  return {
    type: 'business',
    plainText,
    data: res.data.data,
    intent,
    slotValues
  };
} 