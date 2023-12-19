# encoding=utf-8
from scene_processor.scene_processor import SceneProcessor
from utils.date_utils import get_current_and_future_dates
from utils.file_utils import load_file_to_obj
from utils.helpers import get_raw_slot, update_slot, format_title_value_for_logging, is_slot_fully_filled, send_message, extract_json_from_string
import json


class HotelProcessor(SceneProcessor):
    def __init__(self, parameters):
        self.slot_template = get_raw_slot(parameters)
        self.slot = get_raw_slot(parameters)
        self.scene_prompts = load_file_to_obj('scene_config/scene_prompts.json')

    def process(self, user_input, context):
        # 处理用户输入，更新槽位，检查完整性，以及与用户交互
        print('HotelProcessor.process...')
        return '酒店预订成功'
