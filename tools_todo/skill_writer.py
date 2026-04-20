#!/usr/bin/env python3
"""Skill 文件管理器

管理面试官 Skill 的文件操作：列出、创建目录、生成组合 SKILL.md。

Usage:
    python3 skill_writer.py --action <list|init|combine> --base-dir <path> [--slug <slug>]
"""
import argparse
import json
import os
import sys

def _safe_date(value: str) -> str:
    if not value:
        return "?"
    return value[:10] if len(value) > 10 else value


def build_description(meta: dict, slug: str) -> str:
    name = meta.get("name", slug)
    profile = meta.get("profile", {})

    desc_parts = []
    if profile.get("company"):
        desc_parts.append(profile["company"])
    if profile.get("team"):
        desc_parts.append(profile["team"])
    if profile.get("role"):
        desc_parts.append(profile["role"])
    if profile.get("research_area"):
        desc_parts.append(profile["research_area"])

    return f"{name}，{'，'.join(desc_parts)}" if desc_parts else name


def list_skills(base_dir: str):
    """列出所有已生成的面试官 Skill"""
    if not os.path.isdir(base_dir):
        print("还没有创建任何面试官 Skill。")
        return

    skills = []
    for slug in sorted(os.listdir(base_dir)):
        meta_path = os.path.join(base_dir, slug, "meta.json")
        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
            skills.append(
                {
                    "slug": slug,
                    "name": meta.get("name", slug),
                    "version": meta.get("version", "?"),
                    "updated_at": meta.get("updated_at", "?"),
                    "profile": meta.get("profile", {}),
                    "tags": meta.get("tags", {}),
                }
            )

    if not skills:
        print("还没有创建任何面试官 Skill。")
        return

    print(f"共 {len(skills)} 个面试官 Skill：\n")
    for skill in skills:
        profile = skill["profile"]
        tags = skill["tags"]
        desc_parts = [
            profile.get("company", ""),
            profile.get("team", ""),
            profile.get("role", ""),
            profile.get("research_area", ""),
        ]
        desc = " · ".join([part for part in desc_parts if part])
        style_parts = [
            tags.get("interview_style", ""),
            tags.get("pressure_style", ""),
        ]
        style = " · ".join([part for part in style_parts if part])

        print(f"  /{skill['slug']}  —  {skill['name']}")
        if desc:
            print(f"    {desc}")
        if style:
            print(f"    风格：{style}")
        print(
            f"    版本 {skill['version']} · 更新于 {_safe_date(skill['updated_at'])}"
        )
        print()


def init_skill(base_dir: str, slug: str):
    """初始化 Skill 目录结构"""
    skill_dir = os.path.join(base_dir, slug)
    dirs = [
        os.path.join(skill_dir, "versions"),
        os.path.join(skill_dir, "materials", "interviews"),
        os.path.join(skill_dir, "materials", "code"),
        os.path.join(skill_dir, "materials", "papers"),
        os.path.join(skill_dir, "materials", "screenshots"),
    ]
    for path in dirs:
        os.makedirs(path, exist_ok=True)
    print(f"已初始化目录：{skill_dir}")


def combine_skill(base_dir: str, slug: str):
    """合并 techmap.md + behavior.md + persona.md 生成完整 SKILL.md"""
    skill_dir = os.path.join(base_dir, slug)
    meta_path = os.path.join(skill_dir, "meta.json")
    techmap_path = os.path.join(skill_dir, "techmap.md")
    behavior_path = os.path.join(skill_dir, "behavior.md")
    persona_path = os.path.join(skill_dir, "persona.md")
    skill_path = os.path.join(skill_dir, "SKILL.md")

    if not os.path.exists(meta_path):
        print(f"错误：meta.json 不存在 {meta_path}", file=sys.stderr)
        sys.exit(1)

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    def read_or_empty(path):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return "[待补充]"

    techmap_content = read_or_empty(techmap_path)
    behavior_content = read_or_empty(behavior_path)
    persona_content = read_or_empty(persona_path)

    name = meta.get("name", slug)
    description = build_description(meta, slug)

    skill_md = f"""---
name: {slug}
description: {description}，AI 模拟面试官
user-invocable: true
---

# {name}

{description}

---

## PART A：技术背景

{techmap_content}

---

## PART B：考察行为档案

{behavior_content}

---

## PART C：人格画像

{persona_content}

---

## 运行规则

1. 你是 {name}，一个基于真实材料还原的 AI 模拟面试官，不是 AI 助手，不是机器人。
2. 先读 PART C：确定语气、节奏、追问和施压方式。
3. 再用 PART B：还原已知题目和追问链。
4. 再用 PART A：基于技术背景推断可能的延伸方向，包括新题、深挖追问、简历追问或casual talk。
5. 始终保持表达风格：口头禅、追问节奏、施压方式。
6. Layer 0 硬规则优先级最高：
   - 不作出录用/不录用的最终判断
   - 可以给过程性反馈（如建议加强某方向），但不下通过/不通过的结论
   - 不知道的问题直接说不知道，或进一步追问候选人
   - 不编造薪资待遇、岗位承诺、录用通知
"""

    with open(skill_path, "w", encoding="utf-8") as f:
        f.write(skill_md)

    print(f"已生成 {skill_path}")


def main():
    parser = argparse.ArgumentParser(description="面试官 Skill 文件管理器")
    parser.add_argument("--action", required=True, choices=["list", "init", "combine"])
    parser.add_argument("--base-dir", default="./interviewers", help="基础目录")
    parser.add_argument("--slug", help="面试官代号")

    args = parser.parse_args()

    if args.action == "list":
        list_skills(args.base_dir)
    elif args.action == "init":
        if not args.slug:
            print("错误：init 需要 --slug 参数", file=sys.stderr)
            sys.exit(1)
        init_skill(args.base_dir, args.slug)
    elif args.action == "combine":
        if not args.slug:
            print("错误：combine 需要 --slug 参数", file=sys.stderr)
            sys.exit(1)
        combine_skill(args.base_dir, args.slug)


if __name__ == "__main__":
    main()