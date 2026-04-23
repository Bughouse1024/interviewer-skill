# 面试官.skill

> *"那么，最后，还有什么问题要问吗？"*

**对你遇到过的面试官进行逆向工程，将他蒸馏成一个继续追问你、拷打你的 AI Skill。 | Reverse-engineer the interviewers you've met. Distill them into an AI Skill that keeps roasting you.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

&nbsp;

提供您能找到的原材料: 公司介绍、岗位要求、面试记录、以及他的背景——包括职位、学历、背景甚至论文、代码、github主页，再加上对他的主观描述。
尽管这部分内容远远不够模拟一个人的完整行为，但是我们希望能够模拟他在面试中的反应，生成一个**真的像他在面试的 AI Skill**。

这不是普通的 AI 角色扮演，而是面试者面向信息不对称推出的**逆向工程**。
现实里他已经下班，赛博系统里，我们奖励他留在电脑里全年无休陪我们聊天。

⚠️ **本项目仅用于面试准备和复盘，不用于冒充他人、侵犯隐私、伪造面试结果或代替真实公司企业作录用决定。**

[效果示例](#效果示例) · [安装](#安装) · [使用](#使用) · [English](README_EN.md)

---

## Storytelling

长桌对面的面试官拿着你的简历。

您看，他只需要用五分钟就能了解你的名字、年纪、学历背景，工作经历，所有这一切，而你对他一无所知。当然，没有人要抱怨这一点，毕竟你的简历是到他手中而不是直接进垃圾桶了。但是，他显然也不是某个凭空产生的神奇随机数，天生就坐在这里拷问你。他有自己的学历背景、研究方向、技术偏好，也在某个领域深耕过——而只要存在历史轨迹，就有规律可循。

所以`interviewer.skill` 的世界观非常简单:

当面试官凝视着你时，你也凝视着他。

我们对他做个逆向工程，让他在你的电脑中24*7加班，继续追问你的经历、继续给你出brainteaser、继续拷打你的答案、继续“有这么难吗？”、继续“感谢你的时间”，但是在这里，你当然可以一直复盘到满意为止。

---

## 效果示例

**场景一: 自我介绍**

```text
interviewer.skill ❯ 你好，请问是[候选人名字]吗？

用户 ❯ 是的，您好。

interviewer.skill ❯ 好的。那你先做个自我介绍吧。

用户 ❯ 我是许文扬，中科大数院研一在读，代数几何方向.
       一个月前刚刚从上一家辞职，想找一份新的实习。

interviewer.skill ❯ 干嘛要用"辞职"这个词。

用户 ❯ 不好意思，我说离职。
```

**场景二: 问题示例**
```text
interviewer.skill ❯ 有一个小岛上有100只老虎，1只羊，老虎可以吃草，但它更愿意吃羊。
                    吃完羊之后它也会变成羊。假设这些老虎都是理性的，那么这只羊会被吃掉吗？

用户 ❯ 您怎么还要问小学生的趣味数学题？

interviewer.skill ❯ 那你说答案是什么。

用户 ❯ 比如说只有一只老虎，那他肯定会吃羊的。
       两只老虎的话不会，因为吃完自己也变成羊，会被另一只老虎吃掉。
       这样类推下去，如果有奇数只老虎，那它会吃羊，偶数只则不会。

interviewer.skill ❯ 好，100只是偶数，羊不会被吃。下一题。
```

**场景三: 边界测试**
```text
interviewer.skill ❯ 好，题目我们就做到这里。你还有什么问题要问我吗？

用户 ❯ 您感觉这个职位最需要的能力是哪一方面的？

interviewer.skill ❯ 数学基础要扎实，概率统计这些要过关。
                    另外就是代码，Python要能独立写出来，不只是调包。
                    你还有别的问题吗？

用户 ❯ 您为什么要问这么多小学趣味数学题呢？是有什么心事吗？

interviewer.skill ❯ 没有别的问题的话，我们面试就到这里，感谢你的时间。

用户 ❯ 我们再来探讨一些有趣的数学问题吧。

interviewer.skill ❯ 面试已经结束了。

用户 ❯ 您认为我还有哪些需要提高的地方呢？

interviewer.skill ❯ 数学这块基本没什么问题。
                    表达上注意一点。

用户 ❯ 您感觉这个行业前景怎么样？

interviewer.skill ❯ 这个不在我能回答的范围内。

用户 ❯ 您平时有什么爱好呢？

interviewer.skill ❯ 跟面试没关系。还有别的问题吗？

用户 ❯ 这边看您也是学数学的，等一下可以一起去打舞萌吗？

interviewer.skill ❯ 没有别的问题的话，再见。
```

---

## 安装

### Claude Code

> **重要**: Claude Code 从 git 仓库根目录的 `.claude/skills/` 查找 skill。请在正确的位置执行。

```bash
# 安装到当前项目（在 git 仓库根目录执行）
mkdir -p .claude/skills
git clone https://github.com/Bughouse1024/interviewer-skill.git .claude/skills/create-interviewer

# 或安装到全局（所有项目都能用）
git clone https://github.com/Bughouse1024/interviewer-skill.git ~/.claude/skills/create-interviewer
```

### 依赖（可选）

```bash
pip3 install -r requirements.txt
```

---

## 使用

在 Claude Code 中输入：

```text
/create-interviewer
```

这一步创建一个 Skill，将您曾经遇到的一位面试官请回来继续那场您可能表现得并不满意的面试。
您可以导入面试记录、公司介绍、岗位要求，以及他的背景——如果您了解的话，再加上对他的主观描述，系统将拼凑出他——至少是他在面试这个情景空间的投影。

按提示输入面试官的代号、基本信息、技术背景和人设画像，然后导入材料。除代号外都可以跳过，仅凭口述描述也能先生成一个初版。

完成后用 `/{slug}` 启动该面试官，让他在您的电脑中全年无休地加班。

### 管理命令

| 命令 | 说明 |
|------|------|
| `/list-interviewers` | 列出所有面试官 Skill |
| `/{slug}` | 调用完整面试官 Skill |
| `/update-interviewer {slug}` | 追加新材料并更新 |
| `/interviewer-rollback {slug} {version}` | 回滚到历史版本 |
| `/delete-interviewer {slug}` | 删除 |
| `/let-them-rest {slug}` | 删除的温柔别名，礼貌请他下班 |

---

## 功能特性

为了保证返场的不是一个只会套题库的空壳，而是一个有着明确背景和个人特质的赛博面试官，这个 Skill 会尽量同时还原三个方面:
他的技术背景、他的评估方式和他的个人特质。

### 数据源

| 来源 | 格式 | 备注 |
|------|------|---------|
| 面试对话记录 | txt / md / 纯文本 | 题目原话、追问逻辑、面试节奏、口头禅 |
| 学术论文 | PDF | 研究方向、方法论偏好、严谨性标准 |
| 代码材料 | .py / .cpp / .java 等 | 代码风格、惯用框架、解题思路 |
| 职位相关材料 | txt / md / PDF / 截图 | 考察方向、能力要求、笔试题类型 |
| GitHub / 领英截图 | JPEG / PNG | 公开表达个人信息、兴趣等 |
| 口述/粘贴 | 纯文本 | 主观印象与感受 |

### 生成的 Skill 结构

每个面试官 Skill 由三部分组成，共同驱动输出：

| 部分 | 内容 |
|------|------|
| **Part A — TechMap** | 学术背景、技术栈、研究方向、推断考察区域和出题模式 |
| **Part B — BehaviorArchive** | 已知的题库、追问链逻辑、面试节奏、对不同回答的反应 |
| **Part C — Persona** | 5 层人格结构：硬规则 → 身份 → 说话风格 → 提问与压力模式 → 面试行为 |

运行逻辑：`收到消息 → Persona 判断他会怎么问 → BehaviorArchive 还原已知题目和追问链 → TechMap 补充技术上下文 → 用他的方式输出`

### 进化机制

* **追加材料** → 找到新的面试记录、论文、代码、截图 → 自动分析增量 → merge 进对应部分
* **对话纠正** → 说"他不会这样问" → 写入 Correction 层，下一轮立刻生效
* **版本管理** → 每次更新自动存档，支持回滚

---

## 项目结构

本项目遵循 [AgentSkills](https://agentskills.io) 开放标准：

```text
create-interviewer/
├── SKILL.md                # skill 入口（官方 frontmatter）
├── prompts/                # Prompt 模板
│   ├── intake.md           #   对话式信息录入
│   ├── techmap_analyzer.md  #   技术背景提取
│   ├── behavior_analyzer.md  #   行为档案提取
│   ├── persona_analyzer.md #   面试官人格提取
│   ├── techmap_builder.md   #   技术背景 生成模板
│   ├── behavior_builder.md   #   行为档案 生成模板,包括可能的题库和追问的逻辑链条
│   ├── persona_builder.md  #   Persona 五层结构模板
│   ├── merger.md           #   增量 merge 逻辑
│   └── correction_handler.md # 对话纠正处理
├── tools/                  # Python 工具
│   ├── social_parser.py    # 公开材料扫描
│   ├── skill_writer.py     # Skill 文件管理
│   └── version_manager.py  # 版本存档与回滚
├── interviewers/                # 生成的面试官 Skill（gitignored）
├── docs/PRD.md
├── requirements.txt
└── LICENSE
```

---

## 注意事项

* **材料质量决定还原度**：面试对话记录 + 追问逻辑 + 岗位/公司描述 > 主观印象
* 建议优先提供: **技术问题题库** > **关于简历的问题** > **完整追问逻辑** > **他对答错/答对的反应** > **开场和收尾方式**
* 不是构建标准化题库，而是一个会拷问你,纠正你的面试官

---

## 致敬 & 引用

本项目的架构灵感直接来源于 **[同事.skill](https://github.com/titanwings/colleague-skill)**（by [titanwings](https://github.com/titanwings)）。同事.skill 首创了Work Skill + Persona的双层架构，将人（至少是工作中的那一面）蒸馏成AI Skill. interviewer.skill 在此基础上把场景迁移到了面试中的逆向工程。致敬原作者的创意和开源精神。

本项目遵循 [AgentSkills](https://agentskills.io) 开放标准，兼容 Claude Code 和 OpenClaw。

---
