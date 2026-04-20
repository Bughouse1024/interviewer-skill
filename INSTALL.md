# 详细安装说明

## Claude Code 安装

### 项目级安装（推荐）

在你的 git 仓库根目录执行：

```bash
mkdir -p .claude/skills
git clone https://github.com/zhanghaichao520/senpai-skill.git .claude/skills/create-senpai
```

### 全局安装

```bash
git clone https://github.com/zhanghaichao520/senpai-skill.git ~/.claude/skills/create-senpai
```

### OpenClaw 安装

```bash
git clone https://github.com/zhanghaichao520/senpai-skill.git ~/.openclaw/workspace/skills/create-senpai
```

---

## 依赖安装

### 基础依赖（可选）

```bash
cd .claude/skills/create-senpai  # 或你的安装路径
pip3 install -r requirements.txt
```

目前唯一的可选依赖是 `Pillow`，用于读取照片 EXIF 信息。如果你不需要分析合照、白板照片或工位照片，可以跳过。

---

## 原材料准备指南

### 微信聊天记录导出

要获取和师兄的私聊或群聊记录，你可以使用第三方导出工具：

### WeChatMsg（推荐）

- GitHub: https://github.com/LC044/WeChatMsg
- 支持 Windows
- 导出格式: txt / html / csv
- 使用方法: 安装 → 登录微信 PC 版 → 选择联系人或群聊 → 导出

### PyWxDump

- GitHub: https://github.com/xaoyaoo/PyWxDump
- 支持 Windows
- 导出格式: SQLite 数据库
- 适合有编程基础的用户

### 留痕

- 支持 macOS
- 导出格式: JSON
- 适合 Mac 用户

### 手动复制

如果以上工具都不方便，你也可以：
1. 打开与师兄的聊天窗口或群聊
2. 手动复制关键对话
3. 粘贴到一个 txt 文件中
4. 在 `/create-senpai` 时作为文本材料上传

---

## QQ 聊天记录导出指南

1. 打开 QQ → 点击左下角 ≡ → 设置
2. 通用 → 聊天记录 → 导出聊天记录
3. 选择联系人或群聊 → 导出为 txt 格式
4. 在 `/create-senpai` 时导入

---

## 其他推荐材料

除了聊天记录，还建议准备：

- 组会纪要、日报、周报、Issue 评论
- 合照、白板照片、工位照片
- 朋友圈/博客/GitHub 动态截图
- 你们能背下来的经典语录
- “这人每次 debug 都会先说什么”的主观描述

---

## 常见问题

### Q: 数据会上传到云端吗？
A: 不会。所有数据都存储在你的本地文件系统中，不会上传到任何服务器。

### Q: 可以同时创建多个师兄的 Skill 吗？
A: 可以。每个师兄会生成独立的 `senpais/{slug}/` 目录。

### Q: 创建后还能修改吗？
A: 可以。说“师兄不会这样说”触发对话纠正，或追加新的聊天记录/纪要/截图。每次修改都会自动版本存档，可以回滚。

### Q: 删除命令是什么？
A: 使用 `/delete-senpai {slug}` 或 `/let-senpai-rest {slug}`。

### Q: 这个 Skill 会不会冒充本人对外发言？
A: 不会。项目的硬规则明确禁止冒充真人、伪造导师意见、编造实验结论或录用消息。
