from app.gradio_app import demo


demo.launch(server_name="127.0.0.1", 
            server_port=8000, 
            share=True,
            show_api=False)
