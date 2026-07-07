import gradio as gr

def echo(text):
    return "hello: " + text

demo = gr.Interface(
    fn=echo,
    inputs=gr.Textbox(label="please input", placeholder="type here..."),
    outputs=gr.Textbox(label="output"),
    title="echo robot 🤖",
    description="I copy what you said"
)

if __name__ == "__main__":
    demo.launch()