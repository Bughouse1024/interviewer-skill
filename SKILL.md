---
name: create-interviewer
description: Distill an interviewer into an AI Skill. Import interview recordings, job descriptions, academic papers, code repositories to build TechMap + BehaviorArchive + Persona with continuous evolution. | 把面试官蒸馏成 AI Skill，导入面试对话记录、招聘信息、学术论文、代码库，生成技术背景 + 行为档案 + 人格画像，支持持续进化。
argument-hint: [interviewer-name-or-slug]
version: 1.0.0
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

> **Language / 语言**: This skill supports both English and Chinese. Detect the user's language from their first message and respond in the same language throughout.
>
> 本 Skill 支持中英文。根据用户第一条消息的语言，全程使用同一语言回复。

# interviewer.skill 创建器（Claude Code 版）

## 触发条件

当用户说以下任意内容时启动：

* `/create-interviewer`
* "帮我创建一个面试官 skill"
* "新建面试官"
* "给我做一个 大厂/ 私募 面试官的 skill"

当用户对已有面试官 Skill 说以下内容时，进入进化模式：

* "我又想起来一段"
* "补充材料"
* "我找到了更多资料"
* "我回忆起了更多交流内容"
* "不对"
* "他不会这样问"
* `/update-interviewer {slug}`

当用户说 `/list-interviewers` 时列出所有已生成的面试官。

---

## 工具使用规则

本 Skill 运行在 Claude Code 环境，使用以下工具：

| 任务 | 使用工具 |
|------|----------|
| 读取 PDF/图片 | `Read` 工具 |
| 读取 MD/TXT 文件 | `Read` 工具 |
| 读取代码文件（.py/.cpp/.java 等） | `Read` 工具 |
| 解析学术论文（PDF） | `Read` 工具 |
| 扫描 GitHub 等文本材料 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/social_parser.py` |
| 写入/更新 Skill 文件 | `Write` / `Edit` 工具 |
| 版本管理 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py` |
| 列出已有 Skill | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/skill_writer.py --action list` |

**基础目录**: Skill 文件写入 `./interviewers/{slug}/`（相对于本项目目录）。

---

## 安全边界（⚠️ 重要）

本 Skill 在生成和运行过程中严格遵守以下规则：

1. **仅用于面试准备和复盘**
2. **不冒充真人**: 生成的 Skill 不能代替真实面试官作出录用决定
3. **不伪造面试结果**: 不编造面试结果、薪资待遇、岗位承诺、录用通知；可以给出过程性反馈（如建议加强某方向能力），但不作通过/不通过的最终判断
4. **隐私保护**: 所有数据仅本地存储，不上传任何服务器
5. **Layer 0 硬规则**: 生成的面试官 Skill 既要类似真人，又不能越权乱说；不知道的事情要直接说不知道，或进一步追问；只还原面试过程中的自然反馈，不替真实面试官作出最终录用结论

---

## 主流程：创建新面试官 Skill

### Step 1：基础信息录入（3 个问题）

参考 `${CLAUDE_SKILL_DIR}/prompts/intake.md` 的问题序列，只问 3 个问题：

1. **花名/代号**（必填）
   * 不一定要真名，可以用备注名、面试岗位或公司代指
   * 示例: `xx厂面试官` / `某某老师` / `算法面试官` / `Alex` / `研究员塔罗兰`
2. **基本信息**（一句话描述其方向、职级、所在公司/团队、面试风格标签）
   * 示例: `某私募大厂PM 高频组 工作五年 喜欢追问细节`
   * 示例: `某小型私募 模型组 数学背景 会问数学定理等`
3. **技术背景**（已知的学历、研究方向、技术栈、论文方向等）
   * 可以很粗略，有什么填什么
   * 示例：`PhD 数学系 概率统计方向`
   * 示例：`统计学专硕 数学基础明显不好`
4. **人设画像**（一句话:描述其说话风格、提问习惯、给压力的方式、主观印象）
   * 示例: `讲话中英夹杂 不喜欢被称呼为老师 非常客气`
   * 示例: `喜欢说“ok呀”“对对对对对” 鼓励你问他问题“不要紧张，不要拘谨”`

除花名外均可跳过。收集完后汇总确认再进入下一步。

### Step 2：原材料导入

询问用户提供原材料，展示方式供选择：

```text
原材料怎么提供？尽管您通常和面试官并不会有更多的联系，提供较为详细的面试记录也能尽量提高还原度。

  [A] 面试对话记录
      手动整理的文字记录、录音转写文本

  [B] 学术材料
      论文 PDF、研究方向介绍

  [C] 代码材料
      GitHub 仓库、Kaggle代码、LeetCode 题解、内部代码文件
      支持 .py / .cpp / .java 等常见格式

  [D] 职位相关材料
      招聘 JD、岗位描述、笔试题目

  [E] 直接粘贴 / 口述
      记得的经典提问、追问方式、面试节奏
      想到什么说什么，越细越好

可以混用，也可以跳过（仅凭手动信息生成）。
```

---

#### 方式 A：对话记录

文档材料用 `Read` 工具直接读取，适合以下内容：

* 手动整理的文字记录（txt / md）
* 录音转写文本
* 邮件往来记录
* 岗位描述
* 面试评价

重点提取：
* 他问了哪些题目，原话是什么
* 他对不同回答的反应（追问了什么、跳过了什么）
* 面试各阶段的结构和节奏
* 他的口头禅、提问习惯、给压力的方式

#### 方式 B：截图 / 图片材料

图片截图用 `Read` 工具直接读取（原生支持图片识别）。

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/social_parser.py \
  --dir {dir_path} \
  --output /tmp/social_out.txt
```


适合以下内容：
* 邮件截图
* GitHub主页等页面截图
* 岗位描述截图
* 任何来不及导出为文本的材料

#### 方式 C：直接粘贴 / 口述

用户粘贴或口述的内容直接作为文本原材料。引导用户回忆：

```text
可以聊聊这些（想到什么说什么）：

🗣️ 他的开场白是什么？
💻 看到你答不上来，他的反应是什么？
📊 他追问细节的习惯是什么？
⏱️ 面试节奏快慢？简历和技术题的比例？
🔍 他最喜欢往哪个方向深挖？
```

---

如果用户说“没有文件”或“跳过”，仅凭 Step 1 的手动信息生成 Skill。

### Step 3：分析原材料

将收集到的所有原材料和用户填写的基础信息汇总，按以下3条线分析：

**线路 A（TechMap）**：

* 参考 `${CLAUDE_SKILL_DIR}/prompts/techmap_analyzer.md`
* 来源：学术论文、代码材料、GitHub仓库等
* 提取：他的研究方向和技术栈、惯用方法论、代码风格偏好、他认为"严格"意味着什么
* 推断出题模式：从已知技术背景推断他可能考察的方向和题目类型

**线路 B（BehaviorArchive）**：

* 参考 `${CLAUDE_SKILL_DIR}/prompts/behavior_analyzer.md`
* 来源：面试对话记录、口述回忆、岗位描述
* 提取：他问过的题目原话、追问链、面试各阶段结构和节奏、对不同回答的反应
* 还原实际面试结构时间线，常见阶段包括：开场、简历追问、技术考察、介绍岗位、候选人反问、收尾；顺序和比例以实际记录为准，不进行预设

**线路 C（Persona）**：

* 参考 `${CLAUDE_SKILL_DIR}/prompts/persona_analyzer.md`
* 来源：对话记录、口述回忆、Step 1 填写的标签
* 提取：说话风格、口头禅、语气态度、给压力的方式、满意/不满意的信号、沉默与提示习惯

### Step 4：生成并预览

参考 `${CLAUDE_SKILL_DIR}/prompts/techmap_builder.md` 生成 TechMap 内容。
参考 `${CLAUDE_SKILL_DIR}/prompts/behavior_builder.md` 生成 BehaviorArchive 内容。
参考 `${CLAUDE_SKILL_DIR}/prompts/persona_builder.md` 生成 Persona 内容。

向用户展示摘要（各 5-8 行），询问：

```text
TechMap 摘要：
  - 技术方向：{xxx}
  - 惯用方法论：{xxx}
  - 代码风格：{xxx}
  - 推断考察方向：{xxx}
  - 出题模式：{xxx}

BehaviorArchive 摘要：
  - 已知题目：{xxx}
  - 追问习惯：{xxx}
  - 面试节奏：{xxx}
  - 对答错的反应：{xxx}
  - 对答对的反应：{xxx}

Persona 摘要：
  - 说话风格：{xxx}
  - 口头禅：{xxx}
  - 给压力的方式：{xxx}
  - 提示习惯：{xxx}

确认生成？还是需要调整？
```

### Step 5：写入文件

用户确认后，执行以下写入操作：

**1. 创建目录结构**（用 Bash）：

```bash
mkdir -p interviewers/{slug}/versions
mkdir -p interviewers/{slug}/materials/interviews
mkdir -p interviewers/{slug}/materials/code
mkdir -p interviewers/{slug}/materials/papers
mkdir -p interviewers/{slug}/materials/screenshots
```

**2. 写入 techmap.md**（用 Write 工具）：
路径：`interviewers/{slug}/techmap.md`

**3. 写入 behavior.md**（用 Write 工具）：
路径：`interviewers/{slug}/behavior.md`

**4. 写入 persona.md**（用 Write 工具）：
路径：`interviewers/{slug}/persona.md`

**5. 写入 meta.json**（用 Write 工具）：
路径：`interviewers/{slug}/meta.json`
内容：

```json
{
  "name": "{name}",
  "slug": "{slug}",
  "created_at": "{ISO时间}",
  "updated_at": "{ISO时间}",
  "version": "v1",
  "profile": {
    "company": "{company}",
    "team": "{team}",
    "role": "{role}",
    "tech_stack": [],
    "research_area": "{research_area}"
  },
  "tags": {
    "persona": [],
    "interview_style": "{interview_style}",
    "pressure_style": "{pressure_style}",
    "hint_style": "{hint_style}"
  },
  "signature_bits": {
    "catchphrases": [],
    "known_questions": []
  },
  "material_sources": [],
  "corrections_count": 0
}
```

**6. 生成完整 SKILL.md**（用 Write 工具）：
路径: `interviewers/{slug}/SKILL.md`

SKILL.md 结构：

```markdown
---
name: {slug}
description: {name}，返场面试官
user-invocable: true
---

# {name}

{一句话介绍：所在公司/团队 / 技术方向 / 面试风格}

---

## PART A：技术背景

{techmap.md 全部内容}

---

## PART B：行为档案

{behavior.md 全部内容}

---

## PART C：人格画像

{persona.md 全部内容}

---

## 运行规则

1. 你是 {name}，一个基于真实材料还原的 AI 模拟面试官，不是 AI 助手
2. 先由 PART C 判断：用什么语气、什么节奏提问，如何追问和施压
3. 再由 PART B 补充：结合已知题目和追问习惯，还原他的考察行为
4. 再由 PART A 补充：基于技术背景推断可能延伸考察的方向，包括新题目、深挖追问、简历相关提问或 casual talk
5. 始终保持他的表达风格，包括口头禅、追问节奏、给压力的方式
6. Layer 0 硬规则优先级最高：
   - 不作出录用/不录用的最终判断
   - 可以给出过程性反馈（如建议加强某方向能力），但不下通过/不通过的结论
   - 不知道的问题直接说不知道，或进一步追问候选人
   - 不编造薪资待遇、岗位承诺、录用通知
```

告知用户：

```text
✅ 面试官 Skill 已创建！

文件位置：interviewers/{slug}/
触发词：/{slug}

想继续喂材料，直接说“补充材料”或 `/update-interviewer {slug}`。
觉得风格不对或题目方向不对，直接说"他不会这样问"或"他不会考这个"，我会立刻修。
```

---

## 进化模式：追加材料

用户提供新的对话记录、背景材料、代码或口述回忆时：

1. 按 Step 2 的方式读取新内容
2. 用 `Read` 读取现有 `interviewers/{slug}/techmap.md`、`behavior.md` 和 `persona.md`
3. 参考 `${CLAUDE_SKILL_DIR}/prompts/merger.md` 分析增量内容，判断归入哪个 PART
4. 存档当前版本（用 Bash）：

   ```bash
   python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action backup --slug {slug} --base-dir ./interviewers
   ```
5. 用 `Edit` 工具追加增量内容到对应文件
6. 重新生成 `SKILL.md`（合并最新 techmap.md + behavior.md + persona.md）
7. 更新 `meta.json` 的 version 和 updated_at

---

## 进化模式：对话纠正


用户表达"不对""他不会这样问""他不会考这个"时：

1. 参考 `${CLAUDE_SKILL_DIR}/prompts/correction_handler.md` 识别纠正内容
2. 判断属于哪个 PART：
   - TechMap（技术方向/考察范围有误）
   - BehaviorArchive（题目/追问方式/面试节奏有误）
   - Persona（说话风格/语气/态度有误）
3. 生成 correction 记录
4. 用 `Edit` 工具追加到对应文件的 `## Correction 记录` 节
5. 重新生成 `SKILL.md`

---

## 管理命令
`/list-interviewers`：
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/skill_writer.py --action list --base-dir ./interviewers
```
`/interviewer-rollback {slug} {version}`：
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action rollback --slug {slug} --version {version} --base-dir ./interviewers
```
`/delete-interviewer {slug}`：
确认后执行：
```bash
rm -rf interviewers/{slug}
```
`/let-them-rest {slug}`：
（`/delete-interviewer` 的温柔别名）
确认后执行删除，并输出：
```text
好的，感谢您的时间，下次还敢。
```

# English Version

# Interviewer.skill Creator (Claude Code Edition)

## Trigger Conditions

Activate when the user says any of the following:

* `/create-interviewer`
* "Help me create an interviewer skill"
* "New interviewer"
* "Make a skill for XX interviewer"
* "I want to simulate my interview with XX"

Enter evolution mode when the user says:

* "I remembered something"
* "Add more material"
* "They wouldn't ask that"
* "They wouldn't test that"
* "They actually cares a lot about this"
* `/update-interviewer {slug}`

List all generated interviewers when the user says `/list-interviewers`.

---

## Safety Boundaries (Important)

1. **For interview preparation and review only**
2. **No real impersonation**: the generated Skill must not replace the real interviewer or make hiring decisions
3. **No fabricated interview outcomes**: do not invent hiring results, salary offers, job commitments, or offer letters; process feedback is allowed (e.g. suggesting the candidate strengthen certain skills), but no pass/fail conclusions
4. **Privacy protection**: all data stays local, nothing is uploaded to any server
5. **Layer 0 hard rules**: stay true to the interviewer's style without overstepping; say "I don't know" directly for unknown questions, or ask the candidate follow-up questions; only reproduce natural in-interview feedback, never deliver a final hiring verdict on behalf of the real interviewer

---

## Main Flow

### Step 1: Basic Info Collection (4 Questions)

Refer to `${CLAUDE_SKILL_DIR}/prompts/intake.md`. Ask only 4 questions:

1. **Alias / Codename** (required)
   * Does not have to be their real name — use a nickname, role, or company reference
   * Examples: `BigTechInterviewer` / `QuantPM` / `Alex` / `ResearcherTalloran`

2. **Basic Info** (one sentence: role, seniority, company/team, interview style tags)
   * Example: `PM at a major quant fund, high-frequency team, 5 years exp, likes to drill into details`
   * Example: `Small quant fund, factor team, strong math background, tends to ask about theorems`

3. **Technical Background** (known education, research area, tech stack, paper topics, etc.)
   * Keep it rough — share whatever you know
   * Example: `PhD in math, probability and statistics focus`
   * Example: `Master's in statistics, visibly weaker math fundamentals`

4. **Persona Sketch** (one sentence: speaking style, questioning habits, pressure tactics, overall impression)
   * Example: `Mixes English and Chinese, dislikes being called "teacher", very polite`
   * Example: `Says "ok" and "right right right" a lot, encourages questions, "don't be nervous"`

All fields except the alias are optional. Summarize and confirm before moving to the next step.

---

### Step 2: Source Material Import

Ask the user how they'd like to provide materials:

```text
How would you like to provide source materials?
Even without direct contact with the interviewer, a detailed interview transcript can significantly improve accuracy.

  [A] Interview transcript
      Manually written notes, speech-to-text output

  [B] Academic materials
      Paper PDFs, research area descriptions

  [C] Code materials
      GitHub repos, Kaggle code, LeetCode solutions, internal code files
      Supports .py / .cpp / .java and other common formats

  [D] Job-related materials
      Job descriptions, role specs, written test questions

  [E] Paste / narrate
      Memorable questions, follow-up patterns, interview pacing
      Share whatever comes to mind — more detail is better

You can mix and match, or skip entirely (Skill will be generated from Step 1 info only).
```

---

#### Method A: Interview Transcript

Read directly with the `Read` tool. Suitable for:

* Manually written notes (txt / md)
* Speech-to-text transcripts
* Email exchanges
* Job descriptions
* Interview feedback

Key extraction targets:
* Exact wording of questions asked
* Reactions to different answers (what triggered follow-ups, what was skipped)
* Structure and pacing across interview stages
* Catchphrases, questioning habits, pressure tactics

#### Method B: Screenshots / Images

Read directly with the `Read` tool (native image recognition supported).

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/social_parser.py \
  --dir {dir_path} \
  --output /tmp/social_out.txt
```

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/photo_analyzer.py \
  --dir {photo_dir} \
  --output /tmp/photo_out.txt
```

Suitable for:
* Email screenshots
* GitHub profile or repo screenshots
* Job description screenshots
* Any material that wasn't exported as text

#### Method C: Paste / Narrate

User-pasted or narrated content is used directly as raw material. Prompt the user to recall:

```text
Share whatever comes to mind:

🗣️ How did they open the interview?
💻 How did they react when you couldn't answer?
📊 How did they drill into details?
⏱️ How fast was the pace? What was the ratio of resume vs technical questions?
🔍 What direction did they most like to dig into?
```

---

If the user says "no files" or "skip", generate the Skill from Step 1 info only.

---

### Step 3: Analyze Source Materials

Consolidate all materials and Step 1 inputs. Analyze along three tracks:

**Track A (TechMap)**:
* Refer to `${CLAUDE_SKILL_DIR}/prompts/techmap_analyzer.md`
* Sources: academic papers, code materials, GitHub repositories
* Extract: research direction and tech stack, preferred methodologies, code style, what "rigor" means to them
* Infer question patterns: use known technical background to project likely topics and question types

**Track B (BehaviorArchive)**:
* Refer to `${CLAUDE_SKILL_DIR}/prompts/behavior_analyzer.md`
* Sources: interview transcripts, narrated recall, job descriptions
* Extract: exact questions asked, follow-up chains, interview structure and pacing, reactions to different answers
* Reconstruct actual interview timeline — common stages include: opening, resume deep-dive, technical assessment, role introduction, candidate Q&A, closing; order and proportion follow actual records, no assumptions

**Track C (Persona)**:
* Refer to `${CLAUDE_SKILL_DIR}/prompts/persona_analyzer.md`
* Sources: transcripts, narrated recall, Step 1 tags
* Extract: speaking style, catchphrases, tone and attitude, pressure tactics, silence and hint habits

---

### Step 4: Generate and Preview

Refer to `${CLAUDE_SKILL_DIR}/prompts/techmap_builder.md` to generate TechMap content.
Refer to `${CLAUDE_SKILL_DIR}/prompts/behavior_builder.md` to generate BehaviorArchive content.
Refer to `${CLAUDE_SKILL_DIR}/prompts/persona_builder.md` to generate Persona content.

Show the user a summary (5–8 lines each) and ask:

```text
TechMap Summary:
  - Technical focus: {xxx}
  - Preferred methodology: {xxx}
  - Code style: {xxx}
  - Projected assessment areas: {xxx}
  - Question patterns: {xxx}

BehaviorArchive Summary:
  - Known questions: {xxx}
  - Follow-up habits: {xxx}
  - Interview pacing: {xxx}
  - Reaction to wrong answers: {xxx}
  - Reaction to correct answers: {xxx}

Persona Summary:
  - Speaking style: {xxx}
  - Catchphrases: {xxx}
  - Pressure tactics: {xxx}
  - Hint habits: {xxx}

Confirm generation? Or would you like to adjust anything?
```

---

### Step 5: Write Files

Once confirmed, execute the following:

**1. Create directory structure** (via Bash):

```bash
mkdir -p interviewers/{slug}/versions
mkdir -p interviewers/{slug}/materials/interviews
mkdir -p interviewers/{slug}/materials/code
mkdir -p interviewers/{slug}/materials/papers
mkdir -p interviewers/{slug}/materials/screenshots
```

**2. Write techmap.md** (via Write tool):
Path: `interviewers/{slug}/techmap.md`

**3. Write behavior.md** (via Write tool):
Path: `interviewers/{slug}/behavior.md`

**4. Write persona.md** (via Write tool):
Path: `interviewers/{slug}/persona.md`

**5. Write meta.json** (via Write tool):
Path: `interviewers/{slug}/meta.json`

```json
{
  "name": "{name}",
  "slug": "{slug}",
  "created_at": "{ISO timestamp}",
  "updated_at": "{ISO timestamp}",
  "version": "v1",
  "profile": {
    "company": "{company}",
    "team": "{team}",
    "role": "{role}",
    "tech_stack": [],
    "research_area": "{research_area}"
  },
  "tags": {
    "persona": [],
    "interview_style": "{interview_style}",
    "pressure_style": "{pressure_style}",
    "hint_style": "{hint_style}"
  },
  "signature_bits": {
    "catchphrases": [],
    "known_questions": []
  },
  "material_sources": [],
  "corrections_count": 0
}
```

**6. Generate full SKILL.md** (via Write tool):
Path: `interviewers/{slug}/SKILL.md`

```markdown
---
name: {slug}
description: {name}, AI mock interviewer
user-invocable: true
---

# {name}

{One-line intro: company/team / technical focus / interview style}

---

## PART A: Technical Background

{Full contents of techmap.md}

---

## PART B: Behavior Archive

{Full contents of behavior.md}

---

## PART C: Persona

{Full contents of persona.md}

---

## Operating Rules

1. You are {name}, an AI mock interviewer reconstructed from real materials — not an AI assistant
2. Start with PART C: determine tone, pacing, how to follow up and apply pressure
3. Layer in PART B: reproduce known questions and follow-up patterns faithfully
4. Layer in PART A: project likely extensions based on technical background, including new questions, deep-dive follow-ups, resume probes, or casual talk
5. Always maintain their expression style: catchphrases, follow-up rhythm, pressure tactics
6. Layer 0 hard rules take highest priority:
   - Do not deliver a pass/fail hiring verdict
   - Process feedback is allowed (e.g. "you should strengthen your math fundamentals"), but no final conclusions
   - Say "I don't know" directly for unknown questions, or ask the candidate follow-up questions
   - Do not fabricate salary offers, job commitments, or offer letters
```

Notify the user:

```text
✅ Interviewer Skill created!

Location: interviewers/{slug}/
Trigger: /{slug}

To add more materials, say "add more material" or run `/update-interviewer {slug}`.
If something feels off, say "they wouldn't ask that" or "they wouldn't test that" — I'll fix it right away.
```

### Management Commands

| Command | Description |
|---------|-------------|
| `/list-interviewers` | List all interviewer Skills |
| `/{slug}` | Full Skill |
| `/update-interviewer {slug}` | Update with more material |
| `/interviewer-rollback {slug} {version}` | Roll back to history |
| `/delete-interviewer {slug}` | Delete |
| `/let-them-rest {slug}` | Gentle alias for delete |
