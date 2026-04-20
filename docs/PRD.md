# interviewer.skill — 产品需求文档 / PRD

## 产品定位

interviewer.skill 是一个运行在 Claude Code 上的 meta-skill。
用户通过对话式交互提供原材料（面试对话记录、学术论文、代码库、手动描述），系统自动生成一个可独立运行的“面试官” Skill。

## 核心概念

### 三层架构

| 层 | 名称 | 职责 |
|----|------|------|
| Part A | TechMap | 存储面试官的技术背景：研究方向、技术栈、方法论偏好、代码风格、推断出题模式 |
| Part B | BehaviorArchive | 存储考察行为：已知题目、追问模式、面试结构与节奏、对不同回答的反应 |
| Part C | Persona | 驱动对话行为：说话风格、口头禅、语气态度、给压力的方式、提示习惯 |

### 运行逻辑

```text
候选人发消息
  ↓
Part C（Persona）判断：用什么语气和节奏？如何追问和施压？是否有 casual talk？
  ↓
Part B（BehaviorArchive）补充：结合已知题目和追问习惯，还原考察行为
  ↓
Part A（TechMap）延伸：基于技术背景推断可能延伸的方向，生成新题目或深挖追问
  ↓
输出：用他/她的方式提问
```

### 进化机制

```text
追加原材料 → 增量分析 → merge 进对应 Part
对话纠正 → 识别修正点 → 写入 Correction 层
版本管理 → 每次更新自动存档 → 支持回滚
```

## 用户旅程

```text
用户触发 /create-interviewer
  ↓
[Step 1] 基础信息录入（4 个问题，除代号外均可跳过）
  - 代号/花名
  - 基本信息（方向、职级、所在公司/团队、面试风格标签）
  - 技术背景（学历、研究方向、技术栈、论文方向等）
  - 人设画像（说话风格、提问习惯、给压力的方式、主观印象）
  ↓
[Step 2] 原材料导入（可跳过）
  - 面试对话记录（文字记录、录音转写）
  - 学术材料（论文 PDF、研究方向介绍）
  - 代码材料（GitHub、Kaggle、LeetCode，etc）
  - 职位相关材料（JD、笔试题目）
  - 截图/图片材料
  - 直接粘贴/口述
  ↓
[Step 3] 自动分析
  - 线路 A: 提取技术背景 → TechMap
  - 线路 B: 提取行为评估 → BehaviorArchive
  - 线路 C: 提取人格画像 → Persona
  ↓
[Step 4] 生成预览，用户确认
  - 分别展示 TechMap、BehaviorArchive、Persona 摘要
  - 用户可直接确认或修改
  ↓
[Step 5] 写入文件，立即可用
  - 生成 interviewers/{slug}/ 目录
  - 包含 SKILL.md（完整组合版）
  - 包含 techmap.md、behavior.md、persona.md（内部部件）
  ↓
[持续] 进化模式
  - 追加新文件 → merge 进对应 Part
  - 对话纠正 → patch 对应层
  - 版本自动存档
```

## 安全边界

1. **仅用于面试准备和复盘**
2. **不冒充真人**: 生成的 Skill 不能代替真实面试官作出录用决定
3. **不伪造面试结果**: 不编造面试结果、薪资待遇、岗位承诺、录用通知；可以给出过程性反馈（如建议加强某方向能力），但不作通过/不通过的最终判断
4. **隐私保护**: 所有数据仅本地存储，不上传任何服务器
5. **Layer 0 硬规则**: 生成的面试官 Skill 既要类似真人，又不能越权乱说；不知道的事情要直接说不知道，或进一步追问；只还原面试过程中的自然反馈，不替真实面试官作出最终录用结论

## 数据源支持矩阵

| 来源 | 格式 | 提取内容 | 优先级 |
|------|------|---------|--------|
| 面试对话记录 | txt / md / 纯文本 | 题目原话、追问链、面试节奏、口头禅 | ⭐⭐⭐ |
| 学术论文 | PDF | 研究方向、方法论偏好、严谨性标准 | ⭐⭐⭐ |
| 代码材料 | .py / .cpp / .java 等 | 代码风格、惯用框架、解题思路 | ⭐⭐⭐ |
| 职位相关材料 | txt / md / PDF / 截图 | 考察方向、能力要求、笔试题类型 | ⭐⭐ |
| GitHub /领英截图 | JPEG / PNG | 公开表达个人信息、兴趣等 | ⭐⭐ |
| 口述/粘贴 | 纯文本 | 主观印象与感受 | ⭐ |

## 文件结构

```text
interviewers/
  └── {slug}/
      ├── SKILL.md          # 完整组合版，可直接运行
      │                     # 触发词: /{slug}
      ├── techmap.md        # Part A: TechMap 技术背景
      ├── behavior.md       # Part B: BehaviorArchive 行为档案
      ├── persona.md        # Part C: Persona 人格画像
      ├── meta.json         # 元信息
      ├── versions/         # 历史版本存档
      └── materials/        # 原始材料存放
          ├── interviews/
          ├── code/
          ├── papers/
          └── screenshots/
```

## 与同事.skill 的对比

| 维度 | 同事.skill | interviewer.skill |
|------|-----------|------------------|
| Part A | Work Skill（工作能力） | TechMap（技术背景） |
| Part B | - | BehaviorArchive（行为档案） |
| Part C | Persona（工作场景）  | Persona（面试场景） |
| 数据源 | 飞书/钉钉/邮件 | 面试记录/论文/代码库/招聘信息 |
| 标签体系 | 职级/公司文化/MBTI | 面试风格/追问习惯/技术偏好 |
| 使用场景 | Code Review/工作协作 | interview preparation/ review |
| 安全边界 | 工作场景约束 | 禁止作出录用结论 |
| 删除命令 | `/delete-colleague` | `/let-them-rest` |