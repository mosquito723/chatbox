"""
基于 Gradio 6.0 + DeepSeek API 的聊天机器人
使用方式:
    1. 安装依赖: pip install gradio openai
    2. 设置环境变量: set DEEPSEEK_API_KEY=your_api_key_here
    3. 运行: python deepseek_chatbot.py
"""

import os
import gradio as gr
from openai import OpenAI

# ============ 配置区域 ============
API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
API_BASE = "https://api.deepseek.com"
MODEL = "deepseek-v4-pro"        # deepseek-chat (DeepSeek-V3) 或 deepseek-reasoner (DeepSeek-R1)
MAX_HISTORY = 20               # 最大保留的对话轮数

# 初始化客户端
client = OpenAI(api_key=API_KEY, base_url=API_BASE)


def chat_with_deepseek(message, history, system_prompt, temperature, max_tokens):
    """
    与 DeepSeek API 进行对话
    
    参数:
        message: 用户当前输入的消息
        history: Gradio Chatbot 提供的对话历史 [(user_msg, bot_msg), ...]
        system_prompt: 系统提示词
        temperature: 生成温度 (0-2)
        max_tokens: 最大生成 token 数
    
    返回:
        更新后的对话历史
    """
    if not API_KEY:
        history.append([message, "⚠️ 错误: 未设置 DEEPSEEK_API_KEY 环境变量，请先设置 API Key！"])
        return history
    
    # 构建 OpenAI 格式的消息列表
    messages = []
    
    # 添加系统提示词
    if system_prompt.strip():
        messages.append({"role": "system", "content": system_prompt})
    
    # 添加历史对话（限制长度避免超出上下文）
    for msg in history[-MAX_HISTORY:]:
        if msg["role"] == "user":
            messages.append({"role": "user", "content": msg["content"]})
        elif msg["role"] == "assistant":
            messages.append({"role": "assistant", "content": msg["content"]})        
    
    # 添加当前用户消息
    messages.append({"role": "user", "content": message})
    
    try:
        # 调用 DeepSeek API
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=False,
        )
        
        # 提取回复内容
        reply = response.choices[0].message.content
        
        # 添加到历史
        #history.append((message, reply))
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": reply})
        
    except Exception as e:
        error_msg = f"❌ 请求出错: {str(e)}"
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": error_msg})
    
    return history


def clear_chat():
    """清空对话历史"""
    return []


def create_ui():
    """创建 Gradio 界面"""
    
    with gr.Blocks(title="DeepSeek 智能聊天机器人") as demo:
        
        # 页面标题
        gr.Markdown("""
        # 🤖 DeepSeek 智能聊天机器人
        
        基于 **DeepSeek API** + **Gradio** 构建的智能对话助手。
        """)
        
        with gr.Row():
            # 左侧: 对话区域
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(
                    label="对话记录",
                    height=550,
                    #bubble_full_width=False,
                )
                
                with gr.Row():
                    msg_input = gr.Textbox(
                        label="输入消息",
                        placeholder="请输入你的问题，按 Enter 发送...",
                        lines=1,
                        scale=4,
                        show_label=False,
                    )
                    send_btn = gr.Button("发送", variant="primary", scale=1)
                    clear_btn = gr.Button("清空对话", variant="secondary", scale=1)
            
            # 右侧: 设置面板
            with gr.Column(scale=1):
                gr.Markdown("### ⚙️ 参数设置")
                
                system_prompt = gr.Textbox(
                    label="系统提示词 (System Prompt)",
                    value="你是一个 helpful 的 AI 助手，擅长解答各种问题。",
                    lines=3,
                )
                
                temperature = gr.Slider(
                    label="Temperature (创造性)",
                    minimum=0.0,
                    maximum=2.0,
                    value=0.7,
                    step=0.1,
                )
                
                max_tokens = gr.Slider(
                    label="Max Tokens (最大输出长度)",
                    minimum=100,
                    maximum=4096,
                    value=2048,
                    step=100,
                )
                
                gr.Markdown("---")
                gr.Markdown(f"**当前模型**: `{MODEL}`")
                gr.Markdown(f"**API 状态**: {'✅ 已配置' if API_KEY else '❌ 未配置'}")
                
                if not API_KEY:
                    gr.Markdown("""
                    ⚠️ **未检测到 API Key**
                    
                    请在运行前设置环境变量:
                    ```bash
                    set DEEPSEEK_API_KEY=your_api_key
                    ```
                    """)
        
        # 事件绑定
        # 点击发送按钮
        send_btn.click(
            fn=chat_with_deepseek,
            inputs=[msg_input, chatbot, system_prompt, temperature, max_tokens],
            outputs=chatbot,
        ).then(
            fn=lambda: "",  # 发送后清空输入框
            outputs=msg_input,
        )
        
        # 按 Enter 发送
        msg_input.submit(
            fn=chat_with_deepseek,
            inputs=[msg_input, chatbot, system_prompt, temperature, max_tokens],
            outputs=chatbot,
        ).then(
            fn=lambda: "",
            outputs=msg_input,
        )
        
        # 清空对话
        clear_btn.click(
            fn=clear_chat,
            outputs=chatbot,
        )
    
    return demo


if __name__ == "__main__":
    demo = create_ui()
    
    # Gradio 6.0: theme 放在 launch() 中
    demo.launch(
        theme=gr.themes.Soft(),
        #server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
    )
