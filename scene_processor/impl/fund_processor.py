# encoding=utf-8
from scene_config import scene_prompts
from scene_processor.scene_processor import SceneProcessor
from utils.helpers import get_raw_slot


class FundProcessor(SceneProcessor):
    def __init__(self, parameters):
        self.slot_template = get_raw_slot(parameters)
        self.slot = get_raw_slot(parameters)
        self.scene_prompts = scene_prompts

    def process(self, user_input, context):
        # 处理用户输入，更新槽位，检查完整性，以及与用户交互
        pass
