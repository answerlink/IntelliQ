# encoding=utf-8
import logging

from config import RELATED_INTENT_THRESHOLD
from scene_processor.impl.common_processor import CommonProcessor
from utils.data_format_utils import extract_continuous_digits, extract_float
from utils.helpers import send_message


class ChatbotModel:
    def __init__(self, scene_templates: dict):
        self.scene_templates: dict = scene_templates
        self.current_purpose: str = ''
        self.processors = {}

    @staticmethod
    def load_scene_processor(self, scene_config):
        try:
            return CommonProcessor(scene_config)
        except (ImportError, AttributeError, KeyError):
            raise ImportError(f"未找到场景处理器 scene_config: {scene_config}")

    def is_related_to_last_intent(self, user_input):
        """
        判断当前输入是否与上一次意图场景相关
        """
        if not self.current_purpose:
            return False
        prompt = f"判断当前用户输入内容与当前对话场景的关联性:\n\n当前对话场景: {self.scene_templates[self.current_purpose]['description']}\n当前用户输入: {user_input}\n\n这两次输入是否关联（仅用小数回答关联度，得分范围0.0至1.0）"
        result = send_message(prompt, None)
        return extract_float(result) > RELATED_INTENT_THRESHOLD

    def recognize_intent(self, user_input):
        # 根据场景模板生成选项
        purpose_options = {}
        purpose_description = {}
        index = 1
        for template_key, template_info in self.scene_templates.items():
            purpose_options[str(index)] = template_key
            purpose_description[str(index)] = template_info["description"]
            index += 1
        options_prompt = "\n".join([f"{key}. {value} - 请回复{key}" for key, value in purpose_description.items()])
        options_prompt += "\n0. 其他场景 - 请回复0"

        # 发送选项给用户
        user_choice = send_message(f"有下面多种场景，需要你根据用户输入进行判断，只答选项\n{options_prompt}\n用户输入：{user_input}\n请回复序号：", user_input)

        logging.debug(f'purpose_options: %s', purpose_options)
        logging.debug(f'user_choice: %s', user_choice)

        user_choices = extract_continuous_digits(user_choice)

        # 根据用户选择获取对应场景
        if user_choices and user_choices[0] != '0':
            self.current_purpose = purpose_options[user_choices[0]]

        if self.current_purpose:
            print(f"用户选择了场景：{self.scene_templates[self.current_purpose]['name']}")
            # 这里可以继续处理其他逻辑
        else:
            # 用户输入的选项无效的情况，可以进行相应的处理
            print("无效的选项，请重新选择")

    def get_processor_for_scene(self, scene_name):
        if scene_name in self.processors:
            return self.processors[scene_name]

        scene_config = self.scene_templates.get(scene_name)
        if not scene_config:
            raise ValueError(f"未找到名为{scene_name}的场景配置")

        processor_class = self.load_scene_processor(self, scene_config)
        self.processors[scene_name] = processor_class
        return self.processors[scene_name]

    def process_multi_question(self, user_input):
        """
        处理多轮问答
        :param user_input:
        :return:
        """

        # 检查当前输入是否与上一次的意图场景相关
        if self.is_related_to_last_intent(user_input):
            pass
        else:
            # 不相关时，重新识别意图
            self.recognize_intent(user_input)
        logging.info('current_purpose: %s', self.current_purpose)

        if self.current_purpose in self.scene_templates:
            # 根据场景模板调用相应场景的处理逻辑
            self.get_processor_for_scene(self.current_purpose)
            # 调用抽象类process方法
            return self.processors[self.current_purpose].process(user_input, None)
        return '未命中场景'



