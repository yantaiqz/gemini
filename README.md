# gemini [跨境法律合规查询](https://chuhai.streamlit.app/) 

为您生成针对该**跨境合规AI应用**的代码优化过的 SEO Readme 文件。

这个 Readme 重点突出了应用的核心功能（**文件审核**、**合规AI问答**、**多语言支持**）和使用的关键技术（**Gemini AI**、**Streamlit**），并包含了所有 SEO 关键词。

-----

# ⚖️ Cross-border Compliance Judi - 跨境合规专家AI

**Judi** 是一个由 **Google Gemini AI** 驱动的专业级跨境合规和法律文件风险审查工具。专为出海企业和国际商务人士设计，提供**多语言支持**、**法律文件分析**和**即时合规AI问答**，助您在全球市场中稳健前行。

🚀 **[点击此处访问应用]** (替换为您的 Streamlit App 链接)

## ✨ 核心功能 (SEO 关键词优化)

| 功能模块 | 描述 | 核心关键词 |
| :--- | :--- | :--- |
| **法律文件风险审核** | 直接上传 PDF, DOCX, TXT 文件，获取由 **AI 律师**提供的结构化**法律风险报告**、管辖权分析、终止条款审查和综合风险评级。 | **法律文件审核**, **合同风险审查**, **AI合规**, **PDF文件分析**, **国际法律文件** |
| **实时合规 AI 问答** | 针对企业出海过程中遇到的**国际法律**、**监管**、**商业资质**、**贸易壁垒**等问题，获得**专业级、有法律依据**的即时解答。 | **跨境合规**, **企业出海**, **国际贸易法律**, **监管咨询**, **商业资质查询** |
| **全球多语言支持** | UI 界面和 AI 回答支持 **中文、English、العربية (Arabic)、Português、Español** 五种语言，确保全球团队无障碍使用。 | **多语言法律工具**, **国际化合规**, **Arabic Legal AI**, **Spanish Compliance** |
| **企业信息查询 (See Nav)** | 集成了全球企业**征信情况**、**账期安全**等商业资质快速查询功能。 | **外企征信**, **商业资质查询**, **国际企业信用** |

-----

## 💻 技术栈

  * **AI Model:** Google Gemini 2.5 Pro / Flash (用于快速、专业的分析和问答)
  * **Frontend Framework:** Streamlit (快速构建交互式数据应用)
  * **File Handling:** `docx`, `io` (支持 PDF, DOCX, TXT 等主流法律文件格式的解析)
  * **Language Support:** Python Dict I18n (多语言集成)

## 快速部署 (Quick Start)

### 1\. 克隆仓库

```bash
git clone [您的仓库链接]
cd [您的仓库名]
```

### 2\. 环境设置

建议使用 `conda` 或 `venv` 创建虚拟环境：

```bash
# 创建环境
python -m venv venv
source venv/bin/activate # Linux/macOS
.\venv\Scripts\activate # Windows

# 安装依赖
pip install streamlit google-genai pydantic python-docx
```

### 3\. 配置 API Key

应用依赖 **Gemini API Key**。请在项目根目录创建 `.streamlit/secrets.toml` 文件，并填入您的密钥：

```toml
# .streamlit/secrets.toml
GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

### 4\. 运行应用

```bash
streamlit run app.py
```

## 🗺️ 导航栏链接概览 (Nav Bar Overview)

应用底部包含 8 个快捷导航链接，涵盖了跨境企业的核心需求：

| 链接名称 | 目标功能 | 关键信息 |
| :--- | :--- | :--- |
| **财富排行** | 🔗 外部链接 (`youqian.streamlit.app`) | 快速查看全球和地区财富排名。 |
| **世界房产** | 🔗 外部链接 (`fangchan.streamlit.app`) | 全球房产市场数据洞察。 |
| **城市房价** | 🔗 外部链接 (`fangjia.streamlit.app`) | 核心城市房价趋势分析。 |
| **全球法律** | **当前页面** (`chuhai.streamlit.app`) | 本AI应用的主入口，提供**法律合规**支持。 |
| **全球企业** | 🔗 外部链接 (`chuhai.streamlit.app`) | 国际企业名录与资质查询。 |
| **合同审查** | 🔗 外部链接 (`chuhai.streamlit.app`) | 专门的合同文档分析服务。 |
| **德国财税** | 🔗 外部链接 (`qfschina.streamlit.app`) | 针对德国市场的税务与财务咨询。 |
| **深圳房市** | 🔗 外部链接 (`fangjia.streamlit.app`) | 深圳本地房地产市场深度分析。 |

-----

## 🙋 常见问题 (FAQs)

**Q: Judi 可以审核哪些文件类型？**

**A:** 支持 **PDF**、**DOCX (Word)** 和 **TXT** 文件。Gemini AI 会提取文本并进行专业分析。

**Q: AI 提供的建议具有法律效力吗？**

**A:** **不具有。** Judi 提供的所有回复均为 AI 辅助参考，旨在帮助您识别风险和方向。最终的法律决策必须咨询专业律师。

**Q: 如何清空聊天记录？**

**A:** 点击聊天窗口下方的 `🧹 清空聊天记录` 按钮，将清除当前的对话历史和已上传的文件记录。
