# encoding=utf-8
import logging

from config import RELATED_INTENT_THRESHOLD, NO_SCENE_RESPONSE
from scene_processor.impl.common_processor import CommonProcessor
from utils.data_format_utils import extract_continuous_digits, extract_float
from utils.helpers import send_message
from scene_config import scene_prompts


class ChatbotModel:
    def __init__(self, scene_templates: dict):
        self.scene_templates: dict = scene_templates
        self.current_purpose: str = ''
        self.last_recognized_scene: str = ''  # 记录上次识别到的场景
        self.processors = {}
        self.scene_slots = {}  # 新增：每个场景的槽位数据
        self.chat_history = []  # 添加聊天记录存储
        self.is_slot_filling = False  # 标记是否正在补槽阶段

    @staticmethod
    def load_scene_processor(self, scene_config):
        try:
            return CommonProcessor(scene_config)
        except (ImportError, AttributeError, KeyError):
            raise ImportError(f"未找到场景处理器 scene_config: {scene_config}")

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
        options_prompt += "\n0. 无场景/无法判断/没有符合的选项 - 请回复0"

        # 发送选项给AI，带上聊天记录
        last_scene_info = f"上次识别到的场景：{self.last_recognized_scene}" if self.last_recognized_scene else "上次识别到的场景：无"
        user_choice = send_message(
            f"有下面多种场景，需要你根据用户输入进行判断，以最新的聊天记录为准，只答选项\n{last_scene_info}\n{options_prompt}\n用户输入：{user_input}\n请回复序号：", 
            user_input,
            self.chat_history
        )

        logging.debug(f'purpose_options: %s', purpose_options)
        logging.debug(f'user_choice: %s', user_choice)

        user_choices = extract_continuous_digits(user_choice)

        # 根据用户选择获取对应场景
        if user_choices and user_choices[0] != '0':
            # 可以判断场景，更新当前场景
            new_purpose = purpose_options[user_choices[0]]
            if new_purpose != self.current_purpose:
                # 场景发生变化，重置补槽状态
                self.current_purpose = new_purpose
                self.last_recognized_scene = new_purpose  # 更新上次识别到的场景
                self.is_slot_filling = False
                # 清除之前的处理器
                if new_purpose in self.processors:
                    del self.processors[new_purpose]
            print(f"用户选择了场景：{self.scene_templates[self.current_purpose]['name']}")
        else:
            # 用户选择了"无场景/无法判断"
            if self.current_purpose and self.is_slot_filling:
                # 有当前场景且正在补槽阶段，保留当前场景
                print(f"无法判断意图，保留当前场景：{self.scene_templates[self.current_purpose]['name']}")
            else:
                # 没有当前场景或不在补槽阶段，清空场景
                self.current_purpose = ''
                self.is_slot_filling = False
                print("无法识别用户意图")

    def get_processor_for_scene(self, scene_name):
        if scene_name in self.processors:
            return self.processors[scene_name]

        scene_config = self.scene_templates.get(scene_name)
        if not scene_config:
            raise ValueError(f"未找到名为{scene_name}的场景配置")

        # 新增：为该场景初始化槽位数据
        from utils.helpers import get_raw_slot
        if scene_name not in self.scene_slots:
            self.scene_slots[scene_name] = get_raw_slot(scene_config["parameters"])

        # 修改：将槽位数据传递给CommonProcessor
        processor_class = self.load_scene_processor(self, scene_config)
        processor_class.slot = self.scene_slots[scene_name]  # 让处理器直接操作全局槽位
        self.processors[scene_name] = processor_class
        return self.processors[scene_name]

    def clear_current_scene(self):
        """清除当前场景，用于场景处理完成后"""
        self.current_purpose = ''
        self.last_recognized_scene = ''  # 清除上次识别到的场景记录
        self.is_slot_filling = False
        # 清除所有处理器
        self.processors.clear()
        logging.info("场景处理完成，已清除当前场景")

    def generate_no_scene_response(self, user_input):
        """生成无场景识别时的AI回复"""
        # 生成场景选项字符串
        purpose_description = {}
        index = 1
        for template_key, template_info in self.scene_templates.items():
            purpose_description[str(index)] = template_info["description"]
            index += 1
        options_prompt = "\n".join([f"{key}. {value}" for key, value in purpose_description.items()])
        options_prompt += "\n0. 无场景/无法判断"

        prompt = scene_prompts.no_scene_response.format(user_input, options_prompt)
        response = send_message(prompt, user_input, self.chat_history)
        return response if response else NO_SCENE_RESPONSE

    def detect_scene_switch(self, user_input):
        """检测用户是否有切换场景的意图"""
        if not self.current_purpose:
            return False
        
        current_scene_name = self.scene_templates[self.current_purpose]['name']
        last_scene_name = self.scene_templates[self.last_recognized_scene]['name'] if self.last_recognized_scene else "无"
        
        prompt = scene_prompts.scene_switch_detection.format(
            current_scene_name, 
            #last_scene_name, 
            user_input
        )
        
        response = send_message(prompt, user_input, self.chat_history)
        
        # 提取数字回复
        digits = extract_continuous_digits(response)
        if digits and digits[0] == '1':
            logging.info(f"检测到用户意图切换场景，当前场景：{current_scene_name}")
            return True
        
        return False

    def process_multi_question(self, user_input):
        """
        处理多轮问答
        :param user_input:
        :return:
        """
        # 添加用户输入到聊天记录
        self.chat_history.append({"role": "user", "content": user_input})

        # 如果没有当前场景，尝试识别意图
        if not self.current_purpose:
            self.recognize_intent(user_input)
        
        # 如果仍然没有场景，使用AI生成回复
        if not self.current_purpose:
            response = self.generate_no_scene_response(user_input)
            self.chat_history.append({"role": "assistant", "content": response})
            return response

        # 有场景，标记为补槽阶段
        self.is_slot_filling = True
        logging.info('current_purpose: %s', self.current_purpose)

        # 在提取用户信息前，先检测用户是否有切换场景的意图
        if self.detect_scene_switch(user_input):
            # 用户想要切换场景，清除当前场景并重新开始意图识别
            self.clear_current_scene()
            self.recognize_intent(user_input)
            
            # 如果重新识别到场景，继续处理；否则生成无场景回复
            if self.current_purpose:
                processor = self.get_processor_for_scene(self.current_purpose)
                response = processor.process(user_input, self.chat_history)
                
                if not response.startswith("请问") and not response.startswith("抱歉，无法找到场景"):
                    self.clear_current_scene()
                
                self.chat_history.append({"role": "assistant", "content": response})
                return response
            else:
                response = self.generate_no_scene_response(user_input)
                self.chat_history.append({"role": "assistant", "content": response})
                return response

        if self.current_purpose in self.scene_templates:
            # 根据场景模板调用相应场景的处理逻辑
            processor = self.get_processor_for_scene(self.current_purpose)
            # 调用抽象类process方法，传递聊天记录
            response = processor.process(user_input, self.chat_history)
            
            # 检查是否完成场景处理（通过检查响应内容是否包含错误信息或成功处理结果）
            if not response.startswith("请问") and not response.startswith("抱歉，无法找到场景"):
                # 场景处理完成，清除当前场景
                self.clear_current_scene()
            
            # 添加助手回复到聊天记录
            self.chat_history.append({"role": "assistant", "content": response})
            return response
        else:
            # 场景不存在的情况
            response = self.generate_no_scene_response(user_input)
            self.chat_history.append({"role": "assistant", "content": response})
            return response



