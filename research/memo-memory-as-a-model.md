# MEMO: Memory as a Model

> **论文来源**: arXiv:2605.15156v1
> **作者**: Ryan Wei Heng Quek, Sanghyuk Lee, Alfred Wei Lun Leong 等（NUS、MIT、东大、SMART 等机构）
> **主题**: 将新知识编码到专用 MEMORY 模型，保持 LLM 参数不变

---

## 一句话总结

MEMO 提出用一个小模型（MEMORY）专门存储知识，大的 EXECUTIVE 模型通过多轮查询协议从中检索，无需修改原 LLM 参数。

---

## 核心设计

### 架构：双模型分离

| 组件 | 角色 | 说明 |
|------|------|------|
| **MEMORY model** | 知识存储 | 小模型（如 1.5B），通过 SFT 编码知识 |
| **EXECUTIVE model** | 推理执行 | 任意 LLM（GPT-4、Qwen 等），查询 MEMORY 获取答案 |
| **Generator model** | 知识蒸馏 | 用于从语料生成 reflection QA 数据 |

### 关键概念：Reflection

**Reflection** = 从语料中合成的问答对，代表知识库中的知识。不依赖未来查询，是 MEMORY 模型和 EXECUTIVE 模型之间的共享接口。

---

## 数据合成 pipeline（5 步）

```
原始语料 → Chunk → GENERATOR → QA pairs
```

1. **Fact extraction** — 直接提取（explicit facts）+ 间接提取（inferred knowledge）
2. **Consolidation** — 合并冗余/重叠的 QA 对，形成复合问答
3. **Verification** — 自包含性检查：能否在没有原文的情况下回答？不可答的改写或丢弃
4. **Entity surfacing** — 为每个实体生成问答（缓解 reversal curse）
5. **Cross-document synthesis** — 跨文档综合，捕捉分布在多文档中的关系

**注意**：生成的 QA 对中不包含文档标识符，防止 MEMORY 模型利用 shortcut 信号。

---

## 训练方式

- MEMORY 模型通过 SFT 训练，最小化答案 token 的 next-token prediction loss
- 条件仅在 question + preceding answer tokens，从不让模型看到原文
- 这使得 MEMORY 模型必须将知识参数化内化，而非从检索上下文中复制

---

## 推理：多轮查询协议（3 阶段）

当 EXECUTIVE 收到复杂查询时：

| 阶段 | 动作 |
|------|------|
| **1. Grounding** | 拆解为原子子问题，MEMORY 独立回答，提供上下文 grounding |
| **2. Entity identification** | 基于 grounding 信息，缩小并锁定目标实体 |
| **3. Answer synthesis** | 收集支撑事实，综合生成最终答案 |

---

## 关键优势（Table 1 对比）

| 方法 | 冻结基础模型 | 无检索索引 | 黑盒兼容 | 无灾难性遗忘 | 常数内存大小 | 跨 LLM 可迁移 |
|------|:---:|:---:|:---:|:---:|:---:|:---:|
| **Non-parametric** (RAG, ICL) | ✓ | ✕ | ✓ | ✓ | ✕ | ✓ |
| **Parametric** (CPT, SFT) | ✕ | ✓ | ✕ | ✕ | ✕ | ✕ |
| **Latent memory** (Gist, ICAE) | ✓ | ✓ | ✕ | ✓ | ✓ | ✕ |
| **MEMO** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

MEMO 是唯一同时满足所有 6 项属性的方法。

---

## 实验结果

### 主结果（Table 2）

| Method | BrowseComp-Plus | NarrativeQA | MuSiQue |
|--------|:---:|:---:|:---:|
| Perfect Retrieval* | 79.67 | 51.42 | 62.83 |
| BM25 | 1.11 | 10.24 | 20.00 |
| NV-Embed-V2 | 50.67 | 20.59 | 37.47 |
| HippoRAG2 | 56.11 | 21.39 | 42.17 |
| **MEMO** | **54.22** | **26.85** | **48.30** |

- MEMO 在 NarrativeQA 和 MuSiQue 上显著领先（尤其 MuSiQue +4.13pp vs HippoRAG2）
- BrowseComp-Plus 略低于 HippoRAG2，但差距在可接受范围

### 抗干扰实验（Table 3）

添加干扰文档（1×N）时：
- RAG 方法性能下降 4-6 pp
- MEMO 性能基本持平（+0.55pp / -1.77pp）

说明 MEMO 对检索噪声具有强鲁棒性。

### 模型合并持续学习（Table 6）

| Method | 累计计算成本 | Qwen2.5-32B-I Acc. |
|--------|:---:|:---:|
| Full retrain | ~72 GPU-hours | **26.85** |
| Merge-TIES | ~48 GPU-hours | 15.81 |

- 模型合并节省 33% 计算量（K=2），K=10 时节省 5.5× 计算
- 性能差距 11pp，但仍然超过所有检索基线

---

## 局限性

1. **训练成本**：MEMORY 模型仍需 SFT，有计算开销
2. **评估范围**：仅在 3 个基准上验证
3. **扩展性**：MEMORY 模型容量能否随语料库规模扩展（Appendix B）
4. **模型合并精度损失**：合并后性能有下降

---

## 核心创新点总结

1. **Reflection interface** — 用合成的 QA 对作为知识接口，无需看到原文
2. **双模型分离** — 知识存储（MEMORY）与推理执行（EXECUTIVE）解耦
3. **黑盒兼容** — 不需要访问 LLM 权重或 logit，支持任意模型
4. **检索成本常数** — 推理时不随语料库规模增长
5. **模型合并扩展** — 支持增量知识整合，计算成本亚线性增长

---

## 存储信息

- **PDF**: `/tmp/paper.pdf`
- **首页图片**: `/tmp/paper_page-01.png`
- **归档位置**: investrepo/research/
- **arXiv ID**: 2605.15156v1