# encoding=utf-8
import logging

from scene_config import scene_prompts
from scene_processor.scene_processor import SceneProcessor
from utils.helpers import get_raw_slot, update_slot, format_name_value_for_logging, is_slot_fully_filled, send_message, \
    extract_json_from_string, get_dynamic_example, call_scene_api, process_api_result
from utils.prompt_utils import get_slot_update_message, get_slot_query_user_message


class CommonProcessor(SceneProcessor):
    def __init__(self, scene_config):
        parameters = scene_config["parameters"]
        self.scene_config = scene_config
        self.scene_name = scene_config["name"]
        self.slot_template = get_raw_slot(parameters)
        self.slot_dynamic_example = get_dynamic_example(scene_config)
        self.slot = get_raw_slot(parameters)
        self.scene_prompts = scene_prompts

    def process(self, user_input, context):
        # 处理用户输入，更新槽位，检查完整性，以及与用户交互
        # 先检查本次用户输入是否有信息补充，保存补充后的结果   编写程序进行字符串value值diff对比，判断是否有更新
        message = get_slot_update_message(self.scene_name, self.slot_dynamic_example, self.slot_template, user_input)  # 优化封装一下 .format  入参只要填input
        new_info_json_raw = send_message(message, user_input, context)  # 传递聊天记录
        current_values = extract_json_from_string(new_info_json_raw)
        # 新增：如果current_values为dict，转为[{name:..., value:...}]
        if current_values and isinstance(current_values[0], dict) and not ('name' in current_values[0] and 'value' in current_values[0]):
            # 说明是扁平结构
            flat = current_values[0]
            current_values = [{"name": k, "value": v} for k, v in flat.items()]
        logging.debug('current_values: %s', current_values)
        logging.debug('slot update before: %s', self.slot)
        update_slot(current_values, self.slot)
        logging.debug('slot update after: %s', self.slot)
        # 判断参数是否已经全部补全
        if is_slot_fully_filled(self.slot):
            return self.respond_with_complete_data(context)
        else:
            return self.ask_user_for_missing_data(user_input, context)

    def respond_with_complete_data(self, context):
        # 当所有数据都准备好后的响应
        logging.debug(f'%s ------ 参数已完整，详细参数如下', self.scene_name)
        logging.debug(format_name_value_for_logging(self.slot))
        logging.debug(f'正在请求%sAPI，请稍后……', self.scene_name)
        
        # 获取场景的真实名称（从场景配置中获取）
        scene_key = self._get_scene_key()
        if not scene_key:
            return f"抱歉，无法找到场景 '{self.scene_name}' 的配置信息。"
        
        # 准备槽位数据，使用英文键名
        slots_data = {}
        for slot in self.slot:
            if slot['value']:  # 只包含有值的槽位
                # 从场景配置中获取对应的英文键名
                slot_key = self._get_slot_key(slot['name'])
                if slot_key:
                    slots_data[slot_key] = slot['value']
        
        # 调用场景API
        api_result = call_scene_api(scene_key, slots_data)
        
        # 处理API结果
        if "error" in api_result:
            return f"抱歉，调用API时出现错误：{api_result['error']}"
        
        # 通过AI处理API结果，生成用户友好的回复
        user_friendly_response = process_api_result(api_result, context)
        
        return user_friendly_response

    def ask_user_for_missing_data(self, user_input, context):
        message = get_slot_query_user_message(self.scene_name, self.slot, user_input)
        # 请求用户填写缺失的数据，传递聊天记录
        result = send_message(message, user_input, context)
        return result
    
    def _get_scene_key(self):
        """
        根据场景配置获取场景的英文键名
        """
        # 直接从scene_config中获取scene_name字段
        return self.scene_config.get('scene_name')
    
    def _get_slot_key(self, slot_name):
        """
        直接使用参数的name字段
        """
        # 查找对应的参数配置
        for param in self.scene_config.get("parameters", []):
            if param.get("name") == slot_name:
                return param.get("name")
        
        # 如果找不到配置，直接返回原名称
        return slot_name
