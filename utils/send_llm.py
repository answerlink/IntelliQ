# encoding=utf-8
import json
import re
import requests
import config

def send_local_Qwen_message(message, user_input):
    """
    请求Qwen函数
    """
    print('--------------------------------------------------------------------')
    if config.DEBUG:
        print('prompt输入:', message)
        print('用户输入:', user_input)
    elif user_input:
        print('用户输入:', user_input)
    print('----------------------------------')
    headers = {
        # "Authorization": f"Bearer {config.API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "prompt": "system： '{message}', 用户内容： '{user_input}'".format(message=message, user_input=user_input),
        "history": [
            [
                "You are a helpful assistant.", ""
            ]
        ]      
    }


    try:
        response = requests.post(config.Qwen_URL, headers=headers, json=data, verify=False)
        if response.status_code == 200:
            answer = response.json()['data']
            print('LLM输出:', answer)
            print('--------------------------------------------------------------------')
            return answer
        else:
            print(f"Error: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None



def send_chatgpt_message(message, user_input):
    """
    请求chatGPT函数
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

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{message}"}
        ]
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
