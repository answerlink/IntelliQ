# encoding=utf-8
import logging

from scene_processor.impl.WeatherSceneProcessor import WeatherSceneProcessor
from utils.helpers import send_message


class ChatbotModel:
    def __init__(self, scenario_templates):
        self.scene_templates: str = scenario_templates
        self.current_purpose: str = ''
        self.processors = {}

    def is_related_to_last_intent(self, user_input):
        """
        判断当前输入是否与上一次意图场景相关
        """
        if not self.current_purpose:
            return False
        prompt = f"判断当前用户输入内容与当前对话场景的关联性:\n\n当前对话场景: {self.scene_templates[self.current_purpose]['description']}\n当前用户输入: {user_input}\n\n这两次输入是否关联（仅回答是或否）？"
        result = send_message(prompt, None)
        return result == '是'

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

        print('purpose_options', purpose_options)
        print('user_choice', user_choice)
        # 根据用户选择获取对应场景
        if user_choice != '0':
            self.current_purpose = purpose_options[user_choice]

        if self.current_purpose:
            print(f"用户选择了场景：{self.scene_templates[self.current_purpose]['name']}")
            # 这里可以继续处理其他逻辑
        else:
            # 用户输入的选项无效的情况，可以进行相应的处理
            print("无效的选项，请重新选择")

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
            scene_info = self.scene_templates[self.current_purpose]
            parameters = scene_info.get("parameters", [])

            # 在这里可以根据 parameters 调用不同场景的处理逻辑
            if self.current_purpose == 'weather_query':
                if not self.processors.get(self.current_purpose):
                    self.processors[self.current_purpose] = WeatherSceneProcessor(parameters)
            elif self.current_purpose == 'fund_query':
                if not self.processors.get(self.current_purpose):
                    self.processors[self.current_purpose] = WeatherSceneProcessor(parameters)
            elif self.current_purpose == 'hotel_booking':
                if not self.processors.get(self.current_purpose):
                    self.processors[self.current_purpose] = WeatherSceneProcessor(parameters)
            # 调用抽象类process方法
            return self.processors[self.current_purpose].process(user_input)
        return '未命中场景'

