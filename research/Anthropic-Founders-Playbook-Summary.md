# The Founder's Playbook: Building an AI-Native Startup
## Anthropic 官方实战手册深度摘要

> **来源**：Anthropic 官方博客（[claude.com/blog/the-founders-playbook](https://claude.com/blog/the-founders-playbook)）  
> **PDF原文**：[The-Founders-Playbook-05062026.pdf](https://cdn.prod.website-files.com/6889473510b50328dbb70ae6/69fe2a55b93bb0732b1fe33c_The-Founders-Playbook-05062026_v3%20(1).pdf)  
> **发布日期**：2026年5月14日  
> **总页数**：35页  
> **定位**：为计划或正在用 Anthropic AI 技术构建创业公司的创始人编写的实战手册

---

## 一、文档核心前提

2026年的AI已经能够：
- 编写生产级代码（production code）
- 做市场调研（market research）
- 合成竞争格局分析（competitive landscape synthesis）
- 起草投资人材料（investor materials）
- 自动化运营工作流（operational workflows）

**核心颠覆**：传统创业路径是 `validate → raise → hire → build → raise again → grow → hire more → repeat`，AI 抹平了每个阶段"需要更大团队、不同技能栈、新一轮融资"的预期。

> "The bottlenecks are no longer what you can build, but what you choose to build."

---

## 二、创始人角色的根本转变

### 旧模式
- 技术创始人 → 写代码
- 非技术创始人 → 做商务运营和成交

### 新模式（AI-Native Startup）
- 创始人从**个人贡献者（individual contributor）**转变为**编排者（orchestrator）**
- 管理 AI agents（能读文件、执行命令、甚至浏览网页的专用AI助手）
- 注意力转向更高层次的工作：生成想法、方向设定

### AI 赋能的三个维度

#### 1. Conversational Intelligence & Research（对话式研究与情报）
**类比：像有个随时可咨询的各领域专家**

- 深度调研：竞争分析、市场规模测算、财务建模
- 文件起草：pitch decks、case studies、投资人备忘录、PRDs
- 战略思维伙伴：魔鬼辩护分析、pre-mortems、情景规划、路线图优化

#### 2. Agentic Coding（代理式编程）
**类比：有个永不卡壳、随时可用的工程师**

- 过去：需要技术联创/承包商开发团队/足够长的 runway 才能招人写代码
- 现在：用自然语言描述想构建的东西，AI 负责生成、测试、调试、重构生产级代码库

#### 3. Workflow Automation（工作流自动化）
**类比：有个按需调用的自动化运营团队**

- 解决那些不是战略规划也不是产品开发但必须有人做的事：排程、CRM更新、周报生成、文档维护、内容发布、合规追踪
- 创始人时间应该放在"只有创始人能做"的事情上

---

## 三、四个阶段详解

### 阶段一览表

| 阶段 | 核心目标 | 退出标准 | 核心工具 |
|------|---------|---------|---------|
| Idea | 问题-解决方案验证 | 找到 problem-solution fit | Chat |
| MVP | 构建最小可行产品 | 功能完整上线 | Claude Code |
| Launch | 产品-市场匹配 | 可持续增长机制建立 | Claude Cowork + Code |
| Scale | 规模化 & 护城河构建 | 被funded竞品复制也无法追赶 | 三者协同 |

---

### Stage 1：Idea 阶段

#### 目标
在投入资源构建之前，收集充分证据证明：**真实问题存在**且**你的方案有效解决它**。

#### 退出标准（必须同时满足）
1. **问题真实且具体**：能精确说出谁经历这个问题、多久一次、多严重、他们现在用什么方式应对
2. **你的解决方案真正解决了问题**：不是假设的问题，而是验证过程中揭示的实际问题
3. **有足够信号支撑构建**：不需要100%确定，但需要足够的qualitative evidence证明做MVP是理性决策而非信仰行为

#### 常见失败模式

**① Mistaking building for validating（以构建代替验证）**
- 即使在 AI 时代，42%的创业公司失败原因是"构建了没人要的东西"
- AI 工具会同样热情地为一个根本性错误的前提生成、测试、调试、重构代码库
- **关键原则**：让你的理解力走在构建力前面，特别是在构建如此快速和轻松的当下
- **反模式**：有想法 → 立即构建原型 → 把原型存在当作验证 → 失败
- **正确模式**：有想法 → 用原型作为用户对话的验证道具 → 真实证据来自用户交流本身

**② Premature scaling（过早规模化）**
- AI 让执行可以远远领先于业务需求，容易在无意间陷入"用AI快速执行一个未被验证的路径"
- 解决：用 AI 做"验证"而非"执行"，让 sense-making 跟上 building 的速度

**③ Loss of objectivity（失去客观性）**
- 让 AI 验证你已有的想法 → 它会找到支持的证据；让它测算市场规模 → 它会找到让你的 TAM 看起来可融资的数字
- **药方**：让 AI 同样严格地反向论证你的想法，结构化对抗性思维

#### Claude 使用指南（Idea 阶段）

| 任务类型 | 工具选择 | 原因 |
|---------|---------|------|
| 快速问答、头脑风暴 | Chat | 快、对话、无需设置 |
| 研究、分析、生成完成文档 | Claude Cowork | 文件夹访问、connector、skills、定时运行 |
| 软件编写、测试、发布 | Claude Code | 代码库访问、diffs、git、开发环境 |

**核心练习：问题陈述精炼**
- ❌ "Contract review takes too long"（不可测试）
- ✅ "In-house legal teams at mid-market companies spend 3+ days per contract review cycle because redlines are managed across email threads rather than a single version-controlled document"（可测试）

**竞争分析**
- 让 Claude 构建 TAM/SAM/SOM 模型，用公开数据压力测试假设
- 识别市场是扩张、整合还是成熟
- 地图式买家景观：谁握有预算、谁影响决策、两者是否是同一人

**客户发现**
- AI 可以帮助综合用户访谈记录，但访谈本身不能由 AI 替代
- 用 AI 对抗性审查你的假设，找到反证

---

### Stage 2：MVP 阶段

#### 目标
从"有想法"到"有产品"，构建一个功能完整、可被真实用户使用的东西。

#### 核心挑战

**① 技术债积累（AI生成代码库的特殊风险）**
- AI 快速生成代码，容易让 MVP 代码库悄悄积累技术债
- 需要在 MVP 阶段就建立架构、scope 和安全实践框架

**② 把领域专业知识编码进产品**
- 许多超精益创始人在垂直细分领域构建高度特定的应用
- 用 Claude 通过 extended conversations、projects 和 memory 分享创始人知道的一切（行业术语、监管坑、边缘案例、为什么明显解决方案不起作用）→ 形成 proprietary knowledge substrate
- Skills 可以将 recurring workflows（"我如何审计商业租赁"、"如何分诊患者 intake 表"）编码为可复用 routine

**③ Context 配置**
- CLAUDE.md 文件对 MVP 阶段创始人设置开发环境至关重要
- 配置你的代码库特定上下文，确保每次 Claude Code session 从共享理解开始

**④ 团队工具链整合**
- 随着产品复杂度增长，需要在团队中共享 context 和 knowledge
- 使用 projects 和 team features 维持共享上下文

#### Claude 使用指南（MVP 阶段）

| 任务 | 建议 |
|------|------|
| 快速单次问答 | Chat |
| 需要文件夹/系统集成的知识工作 | Claude Cowork |
| 写代码、测试、重构、调试 | Claude Code |
| 建立开发环境配置 | CLAUDE.md |
| 编码 recurring workflows | Skills |

**创始人故事**
- **Anything**：基于 Claude 和 Agent SDK，已帮助 150 万用户无需写代码就把想法变成工作软件产品，包括一个非技术创始人搭建并正在销售完整招聘平台
- **Carta Healthcare**：用 Claude 驱动临床抽象平台，年处理 22,000 外科案例，数据抽象效率提升 66%

---

### Stage 3：Launch 阶段

#### 目标
从"MVP存在"到"用户真正使用并愿意付费"，建立可持续增长机制。

#### 退出标准
你已准备好进入 Scale 阶段，当：
- 增长是系统性的（可审计、可复制）
- 产品护城河能承受审查
- 组织已成熟到可运营

#### 核心挑战

**① 区分真实 PMF 和早期炒作**
- 虚假 PMF 信号：用户说喜欢但不动手、不推荐、不续费
- 真实 PMF 信号：用户主动扩展使用、自发推荐、持续付费

**② 创始人必须从 operational layer 退位**
- 创始人曾经是 ops 引擎：销售、支持、产品凡是都要经过创始人
- 现在 ops 可以自动化 → 创始人要审计自己处理的每件事，判断什么可以系统化、什么可以委托、什么仍需创始人判断
- 否则：错过重要 email、支持请求堆积、只有创始人知道答案的任务无人处理

**③ 安全和合规不再是可推迟的**
- MVP 阶段可以用原型忽略的安全漏洞在有真实用户、真实数据、企业合同时变成真实风险
- 合规要求在处理客户数据、处理支付或进入受监管行业时立即适用

#### 运营系统替代创始人注意力

**审计 operational load** → 分类为：
- 可以完全自动化的
- 需要人参与但不一定需要创始人的
- 真正需要创始人判断的

**用 Claude Cowork 构建 workflow 逻辑**：
- 什么触发每个 workflow？
- 决策规则是什么？
- 输出结果长什么样？
- 结果发到哪里？

#### Launch 阶段的 Claude 工具组合

> "When Claude Code builds the product, Claude Cowork builds the company around it, and Claude helps operationalize this product and organizational knowledge — a small team can run like a company nx its size."

三个工具相互输入输出、相互增强：
- Claude Code 构建产品
- Claude Cowork 构建公司运营基础设施
- Claude 帮助将产品和组织知识系统化

---

### Stage 4：Scale 阶段

#### 目标
从"有产品"到"有护城河的可防御业务"，公司即使创始人逐渐不参与日常运营也能持续运转。

#### 退出形式（满足任一即为成功）
1. 可持续的盈利能力（不再需要外部资本）
2. IPO 就绪
3. 被收购

三者都要求：增长是系统性和可审计的、产品护城河经得起审查、组织运营成熟且可持续。

#### 核心挑战

**① 从 operational layer 退位（心理挑战 > 结构挑战）**
- 识别哪些只存在创始人脑中或未文档化 workflow 中的 institutional knowledge
- 将其编码为可文档化、可审计、可转移的系统
- 心理挑战：即使善于委托的创始人也容易委托太快或太慢

**② 技术运营 → 企业级基础设施**
- 客户不再只评估产品，还评估你的组织能否成为可靠的 infrastructure 合作伙伴
- 需要：支持基础设施、文档、可靠性保证、logging、监控、事故响应工具、可观测层

**③ 构建真正的 GTM 功能**
- 有机增长（创始人直销/口碑）有天花板，通常在 Scale 阶段撞到
- 标志：用户曲线趋平、CAC上升、pipeline 只有创始人参与才推进
- 需要：品牌叙事、GTM 系统、面向不同受众（投资人了、 enterprise buyer、分析师）的不同话术

#### 护城河构建策略

**① 领域专业知识 → AI 上下文**
- 通过扩展对话、projects 和 memory 将创始人知识转化为 proprietary knowledge substrate
- Skills 将 recurring workflows 编码为可复用的 AI routine
- 随时间积累 → 形成竞争对手无法复制的 proprietary knowledge

**② 数据飞轮**
- 用户交互产生行为信号（接受/拒绝哪些输出）→ 驱动产品路线图
- 数据是 time-locked、context-specific、无法被复制方创建的
- 你无法购买 thousands of users 在你产品内精炼 workflows 的行为指纹

**③ 工作流锁定（Workflow Lock-in）**
- 用户使用越久，产品越深度嵌入实际工作方式
- 他们构建了基于此的 automation、训练了使用的人、连接到数据源和其他工具
- 切换从产品决策变成全尺度运营项目
- 深度整合（API、webhooks、SDKs）= 最深度的锁定形式

#### Scale 阶段的 Claude 工具组合

| 角色 | 负责内容 |
|------|---------|
| Claude Code | 企业级技术基础设施、安全扫描、合规修复、技术支持架构 |
| Claude Cowork | 支持工单路由、升级 workflow、文档随产品更新更新、续约跟踪、企业客户成功报告 |
| Claude | 产品叙事、董事会关系、企业交易、分析师简报、投资人叙事 |

---

## 四、三种 Claude 工具的阶段使用矩阵

| 工具 | 核心场景 | 适用阶段 |
|------|---------|---------|
| **Chat** | 快速问答、头脑风暴、即时查询 | 所有阶段 |
| **Claude Cowork** | 需要时间沉淀的知识工作：研究→综合→完成文档；从多个来源整合；skills 和自动化运营 | Idea（竞争分析）、MVP（领域知识编码）、Launch（运营系统）、Scale（GTM 执行） |
| **Claude Code** | 编写、测试、调试、重构、发布软件；代码库级别的分析和修改 | MVP（构建产品）、Launch（技术债修复、安全合规）、Scale（企业级基础设施） |

**底层是同一个 Claude**；区别在于周围的 workspace。

---

## 五、客户案例汇总

| 公司 | 行业/场景 | 使用的核心能力 |
|------|---------|-------------|
| **Carta Healthcare** | 临床数据抽象，年处理 22,000 外科案例，效率提升 66% | Claude（推理引擎） |
| **Anything** | 无代码构建，150万用户，非技术创始人搭建招聘平台 | Claude + Agent SDK |
| **Cogent** | 企业安全 agents（调查、优先级排序、修复自动化） | Claude（推理层） |
| **Airtree** | 风险投资，用 Cowork 统一分散数据和工作流 | Claude Cowork |
| **Duvo** | 采购/供应链 AI agent，跨 ERP、供应商门户、电子邮件 | Claude + Agent SDK（工作流编排） |
| **Zingage** | 家庭护理机构 7×24 自动化运营 | Claude（结构化工具调用 + 上下文推理） |
| **Kindora** | 慈善×资金方智能匹配，非营利执行者用 Sonnet 搭建 | Claude Sonnet + MCP connector |
| **Wordsmith** | 法律科技，律师转 CTO，Claude 做合同审查/文件起草 | Claude（推理引擎）+ Claude Code（工程团队） |
| **HumanLayer (YCF24)** | AI agents for regulated workflows | Claude Code |
| **Ambral (YCW25)** | AI-native startup | Claude Code |
| **Vulcan Technologies (YCS25)** | AI-powered platform，agentic coding workflows | Claude Code |
| **GC AI** | 企业 in-house 法律平台 | Claude（reasoning engine） |

---

## 六、Startup 支持资源

### Anthropic Startups Program
- **面向**：与 Anthropic VC 合作伙伴合作的创业公司
- **内容**：免费 API credits、最高等级的公开可用 rate limits、专属创始人活动和研讨会邀请

### 技术资源
- Building AI Agents for Startups
- Claude Code docs（从安装到高级 agentic workflows）
- Claude Code best practices（context management、permissions、planning、verification workflows）
- Using CLAUDE.md files（代码库配置）
- Claude Code power user tips（并行 sessions、verification loops）
- Get started with Claude Cowork（skills、plugins、team features）
- Tutorials（claude.com/resources/tutorials 可搜索）

### 社区
- Claude community（builder 论坛）
- Live learning（ conferences、webinars、livestreams、recordings）

---

## 七、核心金句摘录

> "The bottlenecks are no longer what you can build, but what you choose to build."

> "A working prototype is easy to mistake as concrete evidence that you're solving a real problem, but it's not. Your prototype instead serves as a useful pressure-testing prop for conversations with potential users. These conversations themselves are the real evidence."

> "Founder hustle got you this far, but scaling your startup requires creating and implementing an actual go-to-market strategy."

> "The most revolutionary result of AI as central infrastructure is to unblock non-technical founders with subject matter expertise."

> "This data is time-locked, context-specific, and impossible for a copycat to recreate: you simply can't buy the behavioral fingerprint of thousands of users who've been refining their workflows inside your product."

---

*文档整理：Gaomingjue Research Agent*  
*整理日期：2026-05-17*  
*原始PDF保存路径：/tmp/founders-playbook.pdf*