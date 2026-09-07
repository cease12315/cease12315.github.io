# 本地AI文献阅读工具
> 基于Ollama + Streamlit + ChromaDB实现的RAG本地文档问答工具，无云端API，全部计算在本机完成。

## 项目简介
本项目实现PDF博士论文解析，把文献切分存入本地向量数据库，基于本地大模型完成文献问答。回答结束自动释放内存，模型可一键删除。适合学术文献快速入门阅读。

### 技术栈
- Python、Streamlit：网页UI界面
- PyPDF：PDF文本提取
- ChromaDB：本地向量数据库
- Ollama qwen:1.8b：本地大语言模型

## 运行步骤
1. 安装Ollama，执行 `ollama pull qwen:1.8b`
2. 安装依赖库
pip install streamlit pypdf chromadb requests
3. 启动项目
streamlit run app.py
4. 上传文字版PDF，解析文档，即可针对文献提问。

## 清理说明
1. 删除文献缓存：删除`chroma_db`文件夹
2. 删除大模型：`ollama rm qwen:1.8b`
