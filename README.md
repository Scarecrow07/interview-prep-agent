# AI 面试准备方案生成器

基于 **7步面试作战手册** 框架，上传 JD（职位描述）和简历，自动生成结构化面试准备方案。支持多LLM厂商，**DeepSeek API Key 内置**，可直接使用无需配置。

---

## 功能介绍

### 7 步完整流程

| 步骤 | 模块 | 内容 |
|------|------|------|
| **Step 1** | JD核心分析 | 岗位名称、行业、核心职责、硬技能（含熟练度/是否必备）、软技能、经验/学历要求、评价关键维度 |
| **Step 2** | 简历分析 | 工作年限、教育背景、工作经历、项目经历（含原文引用）、技术栈汇总、核心优势、潜在风险 |
| **Step 3** | 匹配度分析 | 总体匹配度评分（0-100）、技能逐项匹配状态、核心优势、差距与风险预警、个性化准备策略 |
| **Step 4** | 自我介绍方案 | 2-3版脚本（2分钟/3分钟），各有适用场景、完整脚本、关键亮点；**来源追溯防止编造** |
| **Step 5** | 项目介绍方案 | 2-4个核心项目深度讲解，含背景、技术挑战、解决方案、个人贡献；**必须来自简历原文** |
| **Step 6** | 面试问答库 | **20-30道题目**，涵盖技术深度、项目追问、系统设计、行为面试、动机匹配、短板应对六大类别 |
| **Step 7** | 笔试编码题 | **10-15道题目**（仅技术岗位），含LeetCode参考、题目描述、评分标准、面试追问建议 |
| **Step 8** | 学习资料推荐 | 按差距优先级推荐书籍、课程、文档、视频等，标注难度与预计耗时 |

### 核心特性

#### 🤖 多LLM厂商支持

| 厂商 | 默认模型 | 特点 | API Key |
|------|----------|------|---------|
| **DeepSeek**（默认） | deepseek-chat | 性价比高，内置API Key | ✅ 内置，可直接使用 |
| OpenAI | gpt-4o | 旗舰模型，生产级能力 | ❌ 需用户提供 |
| 智谱 GLM | glm-4 | 国产大模型，中文能力强 | ❌ 需用户提供 |
| 阿里云通义 | qwen-plus | 丰富模型选择，长上下文 | ❌ 需用户提供 |
| 自定义 | - | OpenAI兼容接口 | ❌ 需用户提供 |

#### 🔒 防编造机制

所有生成内容强制标注来源，防止AI编造：

| 模块 | 约束 |
|------|------|
| 自我介绍 | 核心卖点必须与JD硬性要求匹配，背景经历必须来自简历原文 |
| 项目介绍 | 所有项目必须来自简历projects字段，不得添加虚构项目或技能 |
| 面试问答 | 项目问题基于简历项目，技术问题覆盖JD核心栈，短板来自匹配分析 |
| 笔试题目 | 题目必须与JD技术栈强相关，算法题标注LeetCode参考 |

#### 📊 题目数量要求

| 模块 | 数量范围 | 说明 |
|------|----------|------|
| 面试问答 | 20-30道 | 专业技术类6-8道、项目深挖5-7道、系统设计3-5道、行为/软技能3-5道、动机2-3道、短板应对2-4道 |
| 笔试题目 | 10-15道 | 算法/数据结构5-8道、系统设计2-3道、案例分析1-2道、实战编程2-3道 |

#### 📁 文件上传支持

| 区域 | 支持格式 | 说明 |
|------|----------|------|
| JD 上传 | .txt / .pdf / .docx | 自动解析文本内容 |
| 简历上传 | .txt / .pdf / .docx | 自动解析文本内容 |

---

## 如何使用

### 方式一：Streamlit Web界面（推荐）

```bash
# 1. 克隆仓库
git clone https://github.com/Scarecrow07/interview-prep-agent.git
cd interview-prep-agent

# 2. 安装依赖
pip install -e .

# 3. 启动应用
streamlit run src/app.py

# 4. 浏览器打开 http://localhost:8501
```

### 方式二：纯前端版本（无需后端）

访问 [在线版本](https://scarecrow07.github.io/interview-prep-agent/)，纯浏览器端运行。

### 使用步骤

1. **选择LLM厂商**：默认DeepSeek，内置API Key可直接使用
2. **配置API Key**：非DeepSeek厂商需在侧边栏输入API Key
3. **上传JD和简历**：拖拽或点击上传文件
4. **选择岗位类型**：技术岗位/非技术岗位/自动识别
5. **填写补充信息**（可选）：岗位画像、重点关注方向等
6. **点击生成**：等待7个模块依次生成完成
7. **下载报告**：HTML格式，可直接打印

---

## LLM配置

### DeepSeek（推荐，可直接使用）

内置API Key，无需配置：
- 选择 "DeepSeek（内置API Key，可直接使用）"
- 点击 "应用LLM配置"
- 直接开始生成

### 其他厂商

需自行获取API Key：
- [OpenAI](https://platform.openai.com/api-keys)
- [智谱 GLM](https://open.bigmodel.cn/)
- [阿里云百炼](https://bailian.console.aliyun.com/)

---

## 技术实现

### 后端架构（v0.2.0）

```
src/
├── agents/           # Agent模块
│   ├── prompts/      # 7个Prompt文件
│   ├── base.py       # LLM配置与调用封装
│   ├── jd_analyzer.py
│   ├── resume_analyzer.py
│   ├── gap_analyzer.py
│   ├── self_intro_agent.py
│   ├── project_intro_agent.py
│   ├── qa_generator.py
│   ├── coding_agent.py
│   └── resource_agent.py
├── models/           # Pydantic数据模型
│   ├── jd_analysis.py
│   ├── resume_analysis.py
│   ├── gap_analysis.py
│   ├── self_intro.py
│   ├── project_intro.py
│   ├── question_bank.py
│   └── coding_problem.py
├── graph/            # LangGraph工作流
│   ├── state.py
│   ├── nodes.py
│   ├── graph_builder.py
│   └── router.py
├── utils/            # 工具模块
│   ├── llm_config.py # 多厂商LLM配置
│   ├── cache.py
│   └── logger.py
├── report/           # HTML报告渲染
│   └── renderer.py
└── app.py            # Streamlit界面
```

### 核心依赖

- **LangGraph**: 工作流编排
- **LangChain-OpenAI**: LLM调用（兼容DeepSeek等其他厂商）
- **Pydantic**: 结构化数据模型
- **Streamlit**: Web界面

### 工作流顺序

```
输入校验 → JD分析 → 简历分析 → 匹配度分析 → 自我介绍 → 项目介绍 → 面试问答 → 笔试题目(技术岗) → 学习资源 → HTML报告
```

---

## 更新日志

### v0.2.0 (2026-06-30)

**重大更新：完整7步面试作战手册实现**

- ✅ 新增简历分析模块（Step 2）
- ✅ 新增项目介绍模块（Step 5）
- ✅ 面试问答优化：20-30道题目，来源追溯字段
- ✅ 笔试题目优化：10-15道题目，LeetCode题库参考
- ✅ 自我介绍优化：SourceReference来源追溯
- ✅ LLM配置模块：DeepSeek API Key内置，支持5个厂商
- ✅ 完整流程编排：LangGraph状态图

**约束实现：**
- 所有内容必须标注来源（JD/简历/匹配报告）
- 项目介绍不得编造，必须来自简历projects字段
- 面试问答覆盖JD核心技术栈
- 笔试题目标注LeetCode参考便于练习

### v0.1.0 (初始版本)

- 基础JD分析、匹配度分析
- 自我介绍、面试问答、笔试题目
- 纯前端实现

---

## 免责声明

本工具基于 LLM 自动分析生成内容，仅供参考，不构成面试结果承诺。请结合个人实际情况对生成内容进行判断。

---

## 许可

[MIT License](LICENSE)