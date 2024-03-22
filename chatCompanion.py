import streamlit as st
from llama_cpp import Llama
import findFiles
import staticData

# please download the model from: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/resolve/main/llama-2-7b-chat.ggmlv3.q8_0.bin?download=true and paste the downloaded model with the same name in ./Models/ Folder

# model_path = "C:/Users/abhij/AppData/Local/llama_index/models/ggml-model-gpt4all-falcon-q4_0.bin"
# model_path = "C:/Users/abhij/AppData/Local/llama_index/models/ggml-vicuna-13b-4bit-rev1.bin"
# model_path = "C:/Users/abhij/AppData/Local/llama_index/models/GPT4All-13B-snoozy.ggmlv3.q8_0.bin"
model_path = "C:/Users/abhij/AppData/Local/llama_index/models/llama-2-7b-chat.ggmlv3.q8_0.bin"

def chat():
    llm = Llama(
        model_path= model_path)
    enquiry = st.text_input("Ask us anything related to AI Music Therapy 😊",
                            placeholder="What would you like to know?", key="enquiry")
    colb1, colb2 = st.columns([1, 1])
    load_box = st.empty()
    res_box = st.empty()
    ask = colb1.button("Ask", type='primary', use_container_width=True)
    stop = colb2.button("Stop", use_container_width=True)
    if ask:
        load_box.text('Generating Response...')
        resp = []
        # print(prompter('Music', enquiry))
        for output in llm(
            # f"Question: {prompter(emotion, job='student', feeling='depleted')} Answer:",
            f"Question: {staticData.prompter('Music', enquiry)}? Answer:",
            max_tokens=0,
            # stop=[" \n", "Question:", "Q:"],
            stream=True,
        ):
            if stop:
                break
            resp.append(output["choices"][0]["text"])
            result = "".join(resp).strip()
            # result = result.replace("\n", "")
            res_box.markdown(f"{result}")
        load_box.empty()
        st.markdown('----')
        return
