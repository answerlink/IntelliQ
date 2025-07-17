// frontend/src/utils/intentMap.js
export const intentMap = [
  {
    keywords: ['流量', '流量查询', '流量剩余', '查流量'],
    api: '/api/traffic_query',
    businessKey: 'traffic_query',
    slots: ['phone', 'month']
  },
  {
    keywords: ['套餐', '套餐变更', '5G套餐', '换套餐'],
    api: '/api/package_change',
    businessKey: 'package_change',
    slots: ['phone', 'package_type', 'effective_time']
  },
  {
    keywords: ['副卡', '副卡办理', '办副卡', '加副卡'],
    api: '/api/sub_card_apply',
    businessKey: 'sub_card_apply',
    slots: ['main_phone', 'sub_card_count', 'sub_package_type']
  },
  {
    keywords: ['宽带', '宽带报修', '宽带故障', '修宽带'],
    api: '/api/broadband_repair',
    businessKey: 'broadband_repair',
    slots: ['phone', 'broadband_account', 'address', 'fault_type']
  },
  {
    keywords: ['账单', '话费账单', '查账单'],
    api: '/api/account_bill',
    businessKey: 'account_bill',
    slots: ['phone', 'bill_period']
  },
  {
    keywords: ['实名认证', '实名', '查实名'],
    api: '/api/realname_query',
    businessKey: 'realname_query',
    slots: ['phone', 'id_number']
  },
  {
    keywords: ['积分兑换', '兑换积分', '积分换', '积分换话费', '兑换'],
    api: '/api/points_exchange',
    businessKey: 'points_exchange',
    slots: ['phone', 'exchange_type', 'exchange_quantity']
  },
  {
    keywords: ['积分查询', '积分'],
    api: '/api/points_query',
    businessKey: 'points_query',
    slots: ['phone']
  },
  {
    keywords: ['停机', '停机保号'],
    api: '/api/suspend_apply',
    businessKey: 'suspend_apply',
    slots: ['phone', 'suspend_duration']
  },
  {
    keywords: ['发票', '发票申请'],
    api: '/api/invoice_apply',
    businessKey: 'invoice_apply',
    slots: ['phone', 'invoice_type', 'mailing_address']
  },
  {
    keywords: ['投诉'],
    api: '/api/complaint',
    businessKey: 'complaint',
    slots: ['phone', 'complaint_type', 'complaint_content']
  },
  {
    keywords: ['客服', '在线客服'],
    api: '/api/customer_service',
    businessKey: 'customer_service',
    slots: ['phone', 'ticket_type', 'description']
  },
  {
    keywords: ['套餐余量', '余量', '查余量'],
    api: '/api/package_balance',
    businessKey: 'package_balance',
    slots: ['phone']
  },
  {
    keywords: ['地址修改', '通信地址', '改地址'],
    api: '/api/address_modify',
    businessKey: 'address_modify',
    slots: ['phone', 'new_address']
  },
  {
    keywords: ['实名状态', '实名查询'],
    api: '/api/realname_status',
    businessKey: 'realname_status',
    slots: ['phone']
  },
  {
    keywords: ['充值', '缴费'],
    api: '/api/recharge',
    businessKey: 'recharge',
    slots: ['phone', 'amount', 'payment_method']
  },
  {
    keywords: ['过户', '号码过户'],
    api: '/api/number_transfer',
    businessKey: 'number_transfer',
    slots: ['original_phone', 'new_owner_id']
  },
  {
    keywords: ['国际漫游', '漫游'],
    api: '/api/roaming_enable',
    businessKey: 'roaming_enable',
    slots: ['phone', 'roaming_country', 'start_date', 'end_date']
  },
  {
    keywords: ['通知订阅', '订阅'],
    api: '/api/notification_subscribe',
    businessKey: 'notification_subscribe',
    slots: ['phone', 'notification_type']
  },
  {
    keywords: ['套餐退订', '退订'],
    api: '/api/package_unsubscribe',
    businessKey: 'package_unsubscribe',
    slots: ['phone', 'package_type']
  },
  {
    keywords: ['宽带升级', '升级'],
    api: '/api/broadband_upgrade',
    businessKey: 'broadband_upgrade',
    slots: ['phone', 'broadband_account', 'upgrade_type']
  },
  {
    keywords: ['增值业务', '来电显示', '彩铃'],
    api: '/api/value_added',
    businessKey: 'value_added',
    slots: ['phone', 'service_name', 'action']
  },
  {
    keywords: ['停机办理', '复机办理', '停复机'],
    api: '/api/stop_resume',
    businessKey: 'stop_resume',
    slots: ['phone', 'action']
  },
  {
    keywords: ['密码重置', '重置密码'],
    api: '/api/password_reset',
    businessKey: 'password_reset',
    slots: ['phone', 'id_number']
  },
  {
    keywords: ['对话日志', '日志'],
    api: '/api/chat_log',
    businessKey: 'chat_log',
    slots: ['phone', 'action', 'log_content']
  },
  {
    keywords: ['评价', '服务评价'],
    api: '/api/feedback',
    businessKey: 'feedback',
    slots: ['phone', 'score', 'comment']
  },
  {
    keywords: ['人工', '转人工'],
    api: '/api/transfer_agent',
    businessKey: 'transfer_agent',
    slots: ['phone']
  },
  // 兜底FAQ，必须放最后
  {
    keywords: ['faq', '常见问题', '帮助', '问题', '咨询', '业务查询', '业务'],
    api: '/api/faq',
    businessKey: 'faq',
    slots: ['question']
  }
];

export function detectIntent(input) {
  for (const item of intentMap) {
    if (item.keywords.some(kw => input.includes(kw))) {
      return item;
    }
  }
  return intentMap[intentMap.length - 1];
} 