import gradio as gr

def greet(name):
    return f"Hello {name}!"

# 创建简单的界面
demo = gr.Interface(
    fn=greet,
    inputs="text",
    outputs="text",
    title="Test Gradio"
)

if __name__ == "__main__":
    print("Starting Gradio app...")
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)
