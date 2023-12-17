# encoding=utf-8
import json
import re
import requests
import config

from functools import lru_cache


def load_scenario_templates(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


@lru_cache(maxsize=100)
def send_message(message, user_input):
    """
    请求LLM函数
    """
    print('--------------------------------------------------------------------')
    if config.DEBUG:
        print('prompt输入:', message)
    elif user_input:
        print('用户输入:', user_input)
    print('----------------------------------')
    headers = {
        "Authorization": f"Bearer {config.API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{message}"}
        ]
    }

    try:
        response = requests.post(config.GPT_URL, headers=headers, json=data, verify=False)
        if response.status_code == 200:
            answer = response.json()["choices"][0]["message"]['content']
            print('LLM输出:', answer)
            print('--------------------------------------------------------------------')
            return answer
        else:
            print(f"Error: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None


def is_slot_fully_filled(json_data):
    """
    检查槽位是否完整填充
    """
    # 遍历JSON数据中的每个元素
    for item in json_data:
        # 检查value字段是否为空字符串
        if item.get('value') == '':
            return False  # 如果发现空字符串，返回False
    return True  # 如果所有value字段都非空，返回True


def get_raw_slot(parameters):
    # 创建新的JSON对象
    output_data = []
    for item in parameters:
        new_item = {"title": item["title"], "value": ""}
        output_data.append(new_item)
    return output_data


def update_slot(json_data, dict_target):
    """
    更新槽位slot参数
    """
    # 遍历JSON数据中的每个元素
    index = 0
    for item in json_data:
        # 检查value字段是否为空字符串
        if item['value'] != '':
            dict_target[index]['value'] = item.get('value')
        index += 1


def format_title_value_for_logging(json_data):
    """
    抽取参数名称和value值
    """
    log_strings = []
    for item in json_data:
        title = item.get('title', 'Unknown Title')  # 获取title，如果不存在则使用'Unknown Title'
        value = item.get('value', 'N/A')  # 获取value，如果不存在则使用'N/A'
        log_string = f"Title: {title}, Value: {value}"
        log_strings.append(log_string)
    return '\n'.join(log_strings)


def extract_json_from_string(input_string):
    """
    JSON抽取函数
    返回包含JSON对象的列表
    """
    try:
        # 正则表达式假设JSON对象由花括号括起来
        matches = re.findall(r'\{.*?\}', input_string, re.DOTALL)

        # 验证找到的每个匹配项是否为有效的JSON
        valid_jsons = []
        for match in matches:
            try:
                json_obj = json.loads(match)
                valid_jsons.append(json_obj)
            except json.JSONDecodeError:
                continue  # 如果不是有效的JSON，跳过该匹配项

        return valid_jsons
    except Exception as e:
        print(f"Error occurred: {e}")
        return []


