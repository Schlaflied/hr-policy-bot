HR Policy Bot / HR 政策问答机器人
An intelligent HR assistant based on Retrieval-Augmented Generation (RAG) to answer questions about Ontario's Employment Standards Act (ESA).

一个基于检索增强生成（RAG）技术的智能 HR 助手，专门用于回答有关加拿大安大略省《雇佣标准法》（ESA）的问题。

Features / 功能亮点
Accurate & Source-Based Answers: Utilizes a RAG pipeline to provide answers based solely on the official "Your guide to the Employment Standards Act" document, ensuring accuracy and reliability.

Source Citation: For every answer, the bot provides the specific page number(s) from the source document, making it easy to verify the information.

Bilingual Support: The core AI is capable of understanding and responding to questions in both English and Chinese.

Cloud-Ready: Designed with a flexible server configuration that automatically adapts to the port assigned by cloud platforms.

Professional HR Persona: The AI is prompted to act as a professional HR Compliance Assistant, ensuring the tone and quality of the responses are appropriate.

精准、有据可查的回答: 利用 RAG 技术，所有回答都严格基于官方的《雇佣标准法指南》文档，确保了信息的准确性和可靠性。

引用来源: 针对每一个回答，机器人都会提供来源文档中的具体页码，方便用户快速核实信息来源。

双语支持: 核心 AI 能够理解并回答中文和英文的提问。

为云端部署优化: 服务器启动方式灵活，可以自动适应云平台分配的端口，轻松部署。

专业 HR 角色: AI 被设定为专业的安大略省 HR 合规助理，确保回答的语气和质量都符合专业标准。

Tech Stack / 技术栈
Backend: Flask

CORS Handling: Flask-CORS

Environment Variables: python-dotenv

RAG Framework: LangChain

LLM: Google Gemini 1.5 Flash

PDF Loading: PyMuPDF

Vector Store: FAISS (Facebook AI Similarity Search)

Embeddings: Hugging Face Sentence Transformers (all-MiniLM-L6-v2)

How It Works / 工作原理
The project implements a classic Retrieval-Augmented Generation (RAG) pipeline:

本项目实现了一个经典的检索增强生成（RAG）流程：

Load & Split / 加载与分割: The ESA_guide.pdf is loaded and split into smaller, manageable chunks of text.
/ 首先，加载 ESA_guide.pdf 文件，并将其内容分割成更小、易于处理的文本块。

Index (Embed & Store) / 索引（嵌入与存储）: Each text chunk is converted into a numerical vector (embedding) using a sentence-transformer model and stored in a FAISS vector store. This creates a searchable index of the document's content.
/ 使用 sentence-transformer 模型将每个文本块转换为向量（Embedding），并存入 FAISS 向量数据库中。这个过程创建了一个可供快速检索的文档内容索引。

Retrieve / 检索: When a user asks a question, the same embedding model converts the question into a vector. The system then searches the vector store for the most semantically similar text chunks from the document.
/ 当用户提问时，系统使用相同的模型将问题也转换为一个向量，然后在向量数据库中检索与问题语义最相关的文本块。

Generate / 生成: The user's question and the retrieved text chunks (the context) are passed to the Gemini LLM. The model uses this context to generate a concise and accurate answer, citing the source pages.
/ 最后，将用户的问题和检索到的相关文本块（作为上下文）一同发送给 Gemini 大语言模型。模型会基于这些上下文信息，生成一个精准、简洁的回答，并附上来源页码。
