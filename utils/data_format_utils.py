# encoding=utf-8
import re


def extract_float(s):
    # 提取字符串中的第一个浮点型数字
    float_pattern = r'-?\d+(?:\.\d+)?'
    found = re.findall(float_pattern, s)
    if not found:  # 如果没有找到任何数字
        return 0.0
    else:
        return [float(num) for num in found][0]


def extract_floats(s):
    # 提取字符串中的所有浮点型数字
    float_pattern = r'-?\d+(?:\.\d+)?'
    found = re.findall(float_pattern, s)
    if not found:  # 如果没有找到任何数字
        return [0.0]
    else:
        return [float(num) for num in found]


def extract_continuous_digits(text):
    # 使用正则表达式找到所有连续的数字
    continuous_digits = re.findall(r'\d+', text)
    return continuous_digits


def clean_json_string(json_str):
    # 首先移除非 JSON 字符，然后查找 JSON 对象或数组
    cleaned_str = re.search(r'(\{.*\}|\[.*\])', json_str)
    if cleaned_str:
        return cleaned_str.group()
    else:
        return None
