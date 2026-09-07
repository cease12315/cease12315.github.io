import streamlit as st
from pypdf import PdfReader
import chromadb
import requests
import os

st.set_page_config(page_title="本地AI文献阅读器", layout="wide")
st.title("📑本地AI文献阅读工具｜无API密钥，本地运行")

# 向量数据库存放在本地硬盘文件夹 ./chroma_db
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="paper_store")

# PDF上传组件
uploaded_file = st.file_uploader("上传文字版PDF文献", type="pdf")

# 解析PDF，切分文本存入硬盘向量库
if uploaded_file is not None:
    if st.button("解析这篇PDF"):
        with st.spinner("正在解析文档，处理完成会保存到本地硬盘..."):
            reader = PdfReader(uploaded_file)
            all_text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    all_text += page_text

            # 简单切割文本片段
            chunk_size = 600
            chunks = []
            for i in range(0, len(all_text), chunk_size):
                chunks.append(all_text[i:i+chunk_size])

            ids = [f"doc_{i}" for i in range(len(chunks))]
            collection.add(documents=chunks, ids=ids)
        st.success("✅解析完成！数据保存本地硬盘，不需要重复上传")

# 用户提问
question = st.text_input("针对文献提问：")
if st.button("提问AI") and question.strip():
    with st.spinner("本地模型思考中..."):
        # 在本地向量库检索相关片段（读取硬盘数据）
        res = collection.query(query_texts=[question], n_results=3)
        context_text = "\n".join(res["documents"][0])

        prompt = f"""参考下面文献内容，回答用户问题。
文献内容：
{context_text}

用户问题：{question}
"""
        # 请求本地Ollama，keep_alive=0回答完立刻释放内存
        payload = {
            "model":"qwen:1.8b",
            "prompt": prompt,
            "stream":False,
            "keep_alive":0
        }
        r = requests.post("http://127.0.0.1:11434/api/generate", json=payload)
        answer = r.json()["response"]
    st.markdown("### AI回答")
    st.write(answer)

st.divider()
st.markdown("""
### 使用说明
1. Ollama软件必须后台运行（右下角托盘有图标）
2. 上传PDF，点击【解析这篇PDF】，解析结果保存在硬盘 chroma_db文件夹
3. 提问，全部运算本机完成，**无任何API、无额度**
4. keep_alive=0：回答结束立刻释放运行内存
""")
