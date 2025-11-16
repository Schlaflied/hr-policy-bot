# 🤖 HR Policy Bot / 人力资源政策机器人

这是一个基于 Python Flask 和 Google Gemini API 构建的 AI 驱动问答机器人。它专为 HR 政策问答设计，能够从大型政策文档中检索信息，提供准确且有据可依的回答。

This is an AI-powered Q&A bot built with Python Flask and the Google Gemini API. It is designed for HR policy inquiries, retrieving information from large policy documents to provide accurate and well-sourced answers.

## 核心功能 / Core Functionality

* **知识库检索 (RAG) / Knowledge Retrieval (RAG):** 利用 Gemini 模型对政策文档进行嵌入和检索，确保回答基于原文内容。/ Uses the Gemini model for embedding and retrieving information from policy documents, ensuring answers are based on the source text.
* **政策文档支持 / Policy Document Support:** 知识来源是上传的 PDF 文件，例如本项目的 **"ESA_guide.pdf"** (就业标准法指南)。/ The knowledge base consists of uploaded PDF files, such as the **"ESA_guide.pdf"** (Employment Standards Act guide) used in this project.
* **准确问答 / Accurate Q&A:** 接收自然语言问题，返回关于政策条款的直接答案。/ Receives natural language questions and returns direct answers regarding policy provisions.

## 技术栈 / Tech Stack

| 模块 / Module | 组件 / Component | 描述 / Description |
| :--- | :--- | :--- |
| **后端框架 / Backend** | Python, Flask | 轻量级 Web 服务框架。/ Lightweight web service framework. |
| **AI 引擎 / AI Engine** | `google-generativeai` | 用于嵌入（Embedding）和问答（Generation）。/ Used for embeddings and Q&A generation. |
| **文档处理 / Document Processing**| `pymupdf` (MuPDF) | 用于高效读取、解析和分块 PDF 文档。/ Used for efficient reading, parsing, and chunking of PDF documents. |

## API 端点 / API Endpoint

| 方法 / Method | 路径 / Path | 描述 / Description |
| :--- | :--- | :--- |
| `POST` | `/query` | 提交问题，获取 HR 政策的 AI 分析回复。/ Submit a question and receive the AI analysis response on HR policy. |

### `POST /query` 请求体示例 / Request Body Example

```json
{
  "question": "我在安大略省工作，病假可以请几天？"
}
