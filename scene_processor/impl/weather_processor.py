# encoding=utf-8
import logging

from scene_processor.scene_processor import SceneProcessor
from utils.date_utils import get_current_and_future_dates
from utils.file_utils import load_file_to_obj
from utils.helpers import get_raw_slot, update_slot, format_title_value_for_logging, is_slot_fully_filled, send_message, extract_json_from_string
import json


class WeatherProcessor(SceneProcessor):
    def __init__(self, parameters):
        self.slot_template = get_raw_slot(parameters)
        self.slot = get_raw_slot(parameters)
        self.scene_prompts = load_file_to_obj('scene_config/scene_prompts.json')

    def process(self, user_input, context):
        # 处理用户输入，更新槽位，检查完整性，以及与用户交互
        # 先检查本次用户输入是否有信息补充，保存补充后的结果   编写程序进行字符串value值diff对比，判断是否有更新
        current_date, future_date = get_current_and_future_dates(days=7)
        new_info_json_raw = send_message(
            self.scene_prompts['weather_info_update'].format(current_date, current_date, future_date,
                                              json.dumps(self.slot_template, ensure_ascii=False), user_input),
            user_input)
        current_values = extract_json_from_string(new_info_json_raw)
        logging.debug('current_values: %s', current_values)
        logging.debug('slot update before: %s', self.slot)
        update_slot(current_values, self.slot)
        logging.debug('slot update after: %s', self.slot)
        # 判断参数是否已经全部补全
        if is_slot_fully_filled(self.slot):
            return self.respond_with_complete_data()
        else:
            return self.ask_user_for_missing_data(user_input)

    def respond_with_complete_data(self):
        # 当所有数据都准备好后的响应
        print('问天气 ------ 参数已完整，详细参数如下')
        print(format_title_value_for_logging(self.slot))
        print('正在请求天气查询API，请稍后……')
        return format_title_value_for_logging(self.slot) + '\n正在请求天气查询API，请稍后……'

    def ask_user_for_missing_data(self, user_input):
        # 请求用户填写缺失的数据
        result = send_message(
            self.scene_prompts['weather_query_user'].format(json.dumps(self.slot, ensure_ascii=False)), user_input)
        return result
