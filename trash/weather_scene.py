# encoding=utf-8
from datetime import datetime, timedelta
import json
from utils.helpers import send_message, extract_json_from_string, update_slot, is_slot_fully_filled, format_title_value_for_logging, get_raw_slot

prompt_weather_info_update = """JSON每个元素代表一个参数信息，我先给你提供一些基本介绍：
'''
title字段是参数名称，如果需要让用户填写该参数时你应该告诉用户你需要的参数名称
desc字段是参数描述，可以做为title字段的补充，更好的引导用户补充参数
transform字段是填充value字段值的要求说明，严格按照要求说明来填充value字段值
required字段为true表示该元素的value是必填参数，如果value为空则必须让用户补充该参数信息，如果required字段为false表示该参数不是必须补充的字段
'''

需求：
#01 根据用户输入信息提取有用的信息更新到JSON中的value字段
#02 仅更新value字段
#03 如果没有可更新的value则原样返回
#04 当前时间为{}

参考示例：
'''
JSON： [
    {{
        "title": "时间",
        "desc": "口语表述：昨天、今天、明天；具体日期：10号、1月1号、2月3日；日期范围：未来一周、最近十四天",
        "transform": "时间统一转换格式，如果是时间点：yyyy-MM-dd；如果是日期范围：yyyy-MM-dd yyyy-MM-dd",
        "value": "",
        "required": true
    }},
    {{
        "title": "地点",
        "desc": "口语表述：建邺区、南京、河北省、江苏南通、上海虹桥、北京朝阳区",
        "transform": "地点统一转换格式为市区（如果有区）或市，如南京市建邺区、南京市；如果只能提取到省份但提取不到市区，如山东省，不要更新value值",
        "value": "",
        "required": true
    }}
]
问：未来一周南京天气怎么样？
答：[
    {{
        "title": "时间",
        "value": "{} {}"
    }},
    {{
        "title": "地点",
        "value": "南京"
    }}
]
'''

JSON：{}
问：{}
答：
"""

prompt_weather_query_user = """JSON每个元素代表一个参数信息，我先给你提供一些基本介绍：
'''
title字段是参数名称，如果需要让用户填写该参数时你应该告诉用户你需要的参数名称
desc字段是参数描述，可以做为title字段的补充，更好的引导用户补充参数
required字段为true表示该元素的value是必填参数，如果value为空则必须让用户补充该参数信息，如果required字段为false表示该参数不是必须补充的字段
'''

需求：
#01 如果有多个未填写value的参数则可以一起向用户提问
#02 value已经填写的参数不用再次提问

参考示例：
'''
问：[
    {{
        "title": "时间",
        "desc": "口语表述：昨天、今天、明天；具体日期：10号、1月1号、2月3日；日期范围：未来一周、最近十四天",
        "value": "2022-01-01",
        "required": true
    }},
    {{
        "title": "地点",
        "desc": "口语表述：建邺区、南京、河北省、江苏南通、上海虹桥、北京朝阳区",
        "value": "",
        "required": true
    }}
]
答：请问你想查询天气的地点是什么？
'''

问：{}
答：
"""


slot = None


def process_weather_scene(user_input, parameters):
    global slot
    raw_slot = get_raw_slot(parameters)
    if not slot:
        slot = raw_slot

    # 先检查本次用户输入是否有信息补充，保存补充后的结果   编写程序进行字符串value值diff对比，判断是否有更新
    current_time_obj = datetime.now()
    current_time = current_time_obj.strftime("%Y-%m-%d")
    # 当前日期加上7天
    time_plus_7_days = current_time_obj + timedelta(days=7)
    formatted_time_plus_7_days = time_plus_7_days.strftime("%Y-%m-%d")
    new_info_json_raw = send_message(
        prompt_weather_info_update.format(current_time, current_time, formatted_time_plus_7_days,
                                          json.dumps(raw_slot, ensure_ascii=False), user_input),
        user_input)
    current_values = extract_json_from_string(new_info_json_raw)
    print('current_values', current_values)
    print('slot update before', slot)
    update_slot(current_values, slot)
    print('slot update after', slot)
    # 判断参数是否已经全部补全
    if is_slot_fully_filled(slot):
        print('问天气 ------ 参数已完整，详细参数如下')
        print(format_title_value_for_logging(slot))
        print('正在请求天气查询API，请稍后……')
        return format_title_value_for_logging(slot) + '\n正在请求天气查询API，请稍后……'
    else:
        str = json.dumps(slot, ensure_ascii=False)
        result = send_message(prompt_weather_query_user.format(str), user_input)
        return result
