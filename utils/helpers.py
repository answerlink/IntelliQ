# encoding=utf-8
import glob
import json
import re
import requests
import urllib3
import config

# 禁用SSL证书验证警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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


def load_all_scene_configs():
    """
    从本地scene_templates.json文件加载场景配置
    特殊处理common_fields通用字段，将其合并到每个场景的parameters中
    """
    print("从本地scene_templates.json加载场景配置")
    all_scene_configs = {}

    # 搜索目录下的所有json文件
    for file_path in glob.glob("scene_config/**/*.json", recursive=True):
        current_config = load_scene_templates(file_path)
        
        # 提取通用字段
        common_fields = current_config.get('common_fields', [])
        
        # 处理场景列表
        scene_list = current_config.get('scene_list', [])
        
        for scene in scene_list:
            scene_name = scene.get('scene_name')
            if scene_name and scene_name not in all_scene_configs:
                # 复制场景的parameters
                scene_parameters = scene.get('parameters', []).copy()
                
                # 将common_fields合并到parameters前面
                merged_parameters = common_fields.copy() + scene_parameters
                
                # 构建场景配置，添加scene_name字段
                all_scene_configs[scene_name] = {
                    "scene_name": scene_name,  # 添加英文场景名称
                    "name": scene.get('name', ''),
                    "description": scene.get('description', ''),
                    "parameters": merged_parameters,
                    "enabled": scene.get('enabled', False),
                    "example": scene.get('example', '')
                }
        
        # 处理其他非scene_list和common_fields的配置项
        for key, value in current_config.items():
            if key not in ['common_fields', 'scene_list'] and key not in all_scene_configs:
                # 为其他配置项也添加scene_name字段
                if isinstance(value, dict):
                    value['scene_name'] = key
                all_scene_configs[key] = value

    return all_scene_configs


def call_scene_api(scene_name, slots_data):
    """
    调用场景API
    :param scene_name: 场景名称（如broadband_repair）
    :param slots_data: 槽位数据
    :return: API响应结果
    """
    try:
        # 构建API URL
        api_url = config.SCENE_API_URL_TEMPLATE.format(scene_name=scene_name)
        
        # 准备请求头
        headers = {
            "Content-Type": "application/json"
        }
        
        # 发送POST请求，直接发送扁平化的slots_data
        print(f"调用场景API: {api_url}")
        print(f"请求体: {json.dumps(slots_data, ensure_ascii=False)}")
        response = requests.post(
            api_url, 
            headers=headers, 
            json=slots_data, 
            timeout=config.API_TIMEOUT
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"API调用成功: {json.dumps(result, ensure_ascii=False)}")
            return result
        else:
            print(f"API调用失败，状态码: {response.status_code}")
            return {"error": f"API调用失败，状态码: {response.status_code}"}
            
    except requests.RequestException as e:
        print(f"API请求异常: {e}")
        return {"error": f"API请求异常: {e}"}
    except Exception as e:
        print(f"处理API响应时出错: {e}")
        return {"error": f"处理API响应时出错: {e}"}


def process_api_result(api_result, chat_history=None):
    """
    处理API结果，通过AI生成用户友好的回复
    :param api_result: API返回的结果
    :param chat_history: 聊天记录
    :return: 处理后的用户友好回复
    """
    try:
        # 只取data部分发给AI
        data_part = api_result.get("data", api_result)
        prompt = config.API_RESULT_PROMPT.format(api_result=json.dumps(data_part, ensure_ascii=False))
        
        # 调用AI处理结果
        result = send_message(prompt, None, chat_history)
        
        if result:
            return result
        else:
            return "抱歉，处理结果时出现错误，请稍后重试。"
            
    except Exception as e:
        print(f"处理API结果时出错: {e}")
        return "抱歉，处理结果时出现错误，请稍后重试。"


def send_message(message, user_input, chat_history=None):
    """
    请求chatGPT函数，支持聊天记录
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

    # 构建消息列表
    messages = [{"role": "system", "content": config.SYSTEM_PROMPT}]
    
    # 添加聊天记录（如果提供）
    if chat_history:
        # 限制聊天记录数量
        limited_history = chat_history[-config.CHAT_HISTORY_COUNT:]
        for msg in limited_history:
            messages.append(msg)
    
    # 添加当前消息
    messages.append({"role": "user", "content": f"{message}"})

    data = {
        "model": config.MODEL,
        "messages": messages,
        "enable_thinking": False
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
        new_item = {"name": item["name"], "desc": item["desc"], "type": item["type"], "value": ""}
        output_data.append(new_item)
    return output_data


def get_dynamic_example(scene_config):
    # 创建新的JSON对象
    if 'example' in scene_config and scene_config['example'] != '':
        return scene_config['example']
    else:
        return "JSON：[{'name': 'phone', 'desc': '需要查询的手机号', 'value': ''}, {'name': 'month', 'desc': '查询的月份，格式为yyyy-MM', 'value': ''} ]\n输入：帮我查一下18724011022在2024年7月的流量\n答：{ 'phone': '18724011022', 'month': '2024-07' }"


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
        # 检查item是否包含必要的字段
        if not isinstance(item, dict) or 'name' not in item or 'value' not in item:
            continue
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
                try:
                    valid_jsons.append(fix_json(match))
                except json.JSONDecodeError:
                    continue  # 如果不是有效的JSON，跳过该匹配项
                continue  # 如果不是有效的JSON，跳过该匹配项

        return valid_jsons
    except Exception as e:
        print(f"Error occurred: {e}")
        return []


def fix_json(bad_json):
    # 首先，用双引号替换掉所有的单引号
    fixed_json = bad_json.replace("'", '"')
    try:
        # 然后尝试解析
        return json.loads(fixed_json)
    except json.JSONDecodeError:
        # 如果解析失败，打印错误信息，但不会崩溃
        print("给定的字符串不是有效的 JSON 格式。")

