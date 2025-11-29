# -----------------------------------------------------------------------------
# |       HR Policy Bot - API 服务器 v2.0 (云端部署版)                        |
# |---------------------------------------------------------------------------|
# | Syna你好！这个版本已经为云端部署做好了准备。我们修改了服务器的启动方式，|
# | 让它可以自动适应云平台分配的端口。                                        |
# -----------------------------------------------------------------------------

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# --- RAG 技术栈的核心导入 ---
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

# --- 积木块 1 & 2: 加载并分割文档 ---
print("正在加载并分割 PDF 文档...")
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    script_dir = os.getcwd()
pdf_path = os.path.join(script_dir, "ESA_guide.pdf")
loader = PyMuPDFLoader(pdf_path)
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(documents)
print("文档加载并分割成功。")

# --- 积木块 3 & 4: 创建智能索引和检索器 ---
print("正在创建智能索引和检索器...")
model_name = "sentence-transformers/all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=model_name)
vectorstore = FAISS.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
print("智能索引和检索器创建成功！")

# --- 积木块 5: 搭建支持引用来源的问答生成链 ---
print("正在搭建最终的问答生成链...")
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key, temperature=0.3)

# Prompt 模板，只要求 AI 回答问题，不提引用
template = """
You are a professional HR Compliance Assistant for Ontario, Canada. 
Answer the user's question based only on the following context.
If the context doesn't contain the answer, state that you cannot find the information in the provided documents.
Provide a concise and clear answer. Do NOT mention the sources in your answer.

Context:
{context}

Question: 
{question}
"""
prompt = ChatPromptTemplate.from_template(template)

# RAG 链，它会并行处理并分别返回答案和来源
rag_chain_with_sources = RunnableParallel(
    {"context": retriever, "question": RunnablePassthrough()}
).assign(
    answer=(
        RunnablePassthrough.assign(
            context=(lambda x: "\n\n".join(doc.page_content for doc in x["context"]))
        )
        | prompt
        | llm
        | StrOutputParser()
    )
)
print("AI 大脑已完全准备就绪！")


# --- Flask 服务器部分 ---
app = Flask(__name__)
CORS(app)

@app.route('/ask', methods=['POST'])
def ask_agent():
    print("\n接收到来自客户端的请求...")
    request_data = request.get_json()
    user_prompt = request_data['prompt']
    print(f"收到的用户指令: {user_prompt}")
    
    try:
        # 调用 RAG 链
        result = rag_chain_with_sources.invoke(user_prompt)
        
        # 从来源文档的元数据中提取页码
        sources = []
        for doc in result["context"]:
            page_number = doc.metadata.get('page', -1) + 1 
            sources.append({"page": page_number})
        
        unique_sources = [dict(t) for t in {tuple(d.items()) for d in sources}]
        
        print(f"AI 生成的回复: {result['answer']}")
        print(f"引用的来源页码: {unique_sources}")
        
        # 将答案和来源作为两个独立的字段一起返回
        return jsonify({"answer": result['answer'], "sources": unique_sources})

    except Exception as e:
        print(f"处理请求时发生错误: {e}")
        return jsonify({"error": str(e)}), 500

# 【核心修改】为云端部署更新服务器启动方式
if __name__ == '__main__':
    # 云平台会通过 PORT 环境变量告诉我们用哪个端口
    port = int(os.environ.get('PORT', 5001)) 
    # 在本地运行时，它会继续使用 5001 端口
    app.run(host='0.0.0.0', port=port, debug=False)

