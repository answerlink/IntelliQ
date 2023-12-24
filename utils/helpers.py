# encoding=utf-8
import json
import re
import requests
import config

from functools import lru_cache
from utils.send_llm import send_local_Qwen_message
from utils.send_llm import send_chatgpt_message

send_llm_req = {
    "Qwen": send_local_Qwen_message,
    "chatGPT": send_chatgpt_message
}

def filename_to_classname(filename):
    """
    Convert a snake_case filename to a CamelCase class name.

    Args:
    filename (str): The filename in snake_case, without the .py extension.

    Returns:
    str: The converted CamelCase class name.
    """
    parts = filename.split('_')
    class_name = ''.join(part.capitalize() for part in parts)
    return class_name


def load_scene_templates(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


@lru_cache(maxsize=100)
def send_message(message, user_input):
    """
    请求LLM函数
    """
    return send_llm_req.get(config.USE_MODEL, send_chatgpt_message)(message, user_input)


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
        new_item = {"name": item["name"], "desc": item["desc"], "type": item["type"], "value": ""}
        output_data.append(new_item)
    return output_data


def get_slot_update_json(slot):
    # 创建新的JSON对象
    output_data = []
    for item in slot:
        new_item = {"name": item["name"], "desc": item["desc"], "value": item["value"]}
        output_data.append(new_item)
    return output_data


def get_slot_query_user_json(slot):
    # 创建新的JSON对象
    output_data = []
    for item in slot:
        if not item["value"]:
            new_item = {"name": item["name"], "desc": item["desc"], "value":  item["value"]}
            output_data.append(new_item)
    return output_data


def update_slot(json_data, dict_target):
    """
    更新槽位slot参数
    """
    # 遍历JSON数据中的每个元素
    for item in json_data:
        # 检查value字段是否为空字符串
        if item['value'] != '':
            for target in dict_target:
                if target['name'] == item['name']:
                    target['value'] = item.get('value')
                    break


def format_name_value_for_logging(json_data):
    """
    抽取参数名称和value值
    """
    log_strings = []
    for item in json_data:
        name = item.get('name', 'Unknown name')  # 获取name，如果不存在则使用'Unknown name'
        value = item.get('value', 'N/A')  # 获取value，如果不存在则使用'N/A'
        log_string = f"name: {name}, Value: {value}"
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


