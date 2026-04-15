#!/usr/bin/env python3
"""
自动生成硬件知识库的索引文件
用法: python scripts/generate_index.py
"""

import os
import re
from pathlib import Path

# 仓库根目录（脚本位于 scripts/ 下，向上两级）
REPO_ROOT = Path(__file__).parent.parent.resolve()
DOCS_DIR = REPO_ROOT / "docs"

# 需要跳过的文件名（不列入索引）
SKIP_FILES = {"README.md", "_index.md", ".DS_Store"}

# 可选：为每个分类添加一段描述（手动维护一个映射表）
CATEGORY_DESC = {
    "01_hardware_sensors": "传感器（IMU、温湿度、距离、电流等）",
    "02_hardware_microcontrollers": "微控制器 / 处理器",
    "03_hardware_actuators": "执行器（电机、舵机、电磁铁等）",
    "04_hardware_power": "电源管理（LDO、DCDC、充电保护等）",
    "05_hardware_communication": "通信接口 / 模块（UART、I2C、CAN、WiFi、BLE等）",
    "06_hardware_test_debug": "测试与调试工具（示波器、逻辑分析仪、焊接）",
    "07_software_os_middleware": "操作系统 / 中间件（ROS2、FreeRTOS、Linux）",
    "08_software_dev_tools": "开发工具（Git、Docker、VS Code、CMake）",
    "09_software_languages_libs": "编程语言 / 库（Python、C++ STL、OpenCV）",
    "99_misc": "其他（接插件、线材、散热、外壳）",
}

def extract_title_from_md(filepath):
    """从 Markdown 文件中提取第一个一级标题（# 开头）"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("# "):
                    return line[2:].strip()
    except Exception:
        pass
    # 没有找到标题，用文件名（去掉扩展名）
    return filepath.stem.replace("_", " ").title()

def generate_category_index(category_path):
    """为单个分类文件夹生成 README.md"""
    category_name = category_path.name
    desc = CATEGORY_DESC.get(category_name, "")
    
    # 收集所有 .md 文件（排除 README.md 自身）
    entries = []
    for md_file in sorted(category_path.glob("*.md")):
        if md_file.name in SKIP_FILES:
            continue
        title = extract_title_from_md(md_file)
        rel_path = md_file.name
        entries.append((title, rel_path))
    
    if not entries:
        # 没有条目，可以生成一个空索引或跳过
        return False
    
    # 生成 README 内容
    lines = [
        f"# {category_name.replace('_', ' ').title()}",
        "",
        f"> {desc}" if desc else "",
        "",
        "## 已收录条目",
        "",
    ]
    for title, rel_path in entries:
        lines.append(f"- [{title}](./{rel_path})")
    
    lines.append("\n---\n")
    lines.append("> 此文件由 `scripts/generate_index.py` 自动生成，请勿手动编辑。")
    lines.append("> 若要修改条目列表，请直接管理对应的 `.md` 文件，然后重新运行脚本。")
    
    readme_path = category_path / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    print(f"✅ 已生成: {readme_path}")
    return True

def generate_root_index():
    """生成根目录的总索引 INDEX.md，列出所有分类及其条目"""
    lines = [
        "# 知识库总索引",
        "",
        "> 此文件由脚本自动生成，列出所有已收录的硬件/软件条目。",
        "> 最后更新：" + os.popen("date '+%Y-%m-%d %H:%M:%S'").read().strip(),
        "",
        "## 分类目录",
        "",
    ]
    
    # 遍历 docs 下的一级子目录（按名称排序）
    categories = sorted([d for d in DOCS_DIR.iterdir() if d.is_dir()])
    for cat_dir in categories:
        cat_name = cat_dir.name
        desc = CATEGORY_DESC.get(cat_name, "")
        lines.append(f"### {cat_name.replace('_', ' ').title()}")
        if desc:
            lines.append(f"*{desc}*")
        lines.append("")
        
        # 收集该分类下的条目
        entries = []
        for md_file in sorted(cat_dir.glob("*.md")):
            if md_file.name in SKIP_FILES:
                continue
            title = extract_title_from_md(md_file)
            rel_path = f"./{cat_name}/{md_file.name}"
            entries.append((title, rel_path))
        
        if entries:
            for title, rel_path in entries:
                lines.append(f"- [{title}]({rel_path})")
        else:
            lines.append("*暂无条目*")
        lines.append("")
    
    lines.append("---")
    lines.append("> 提示：要更新此索引，请运行 `python scripts/generate_index.py`。")
    
    index_path = REPO_ROOT / "INDEX.md"
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ 已生成总索引: {index_path}")

if __name__ == "__main__":
    print("开始生成索引...")
    generated_any = False
    for category_dir in DOCS_DIR.iterdir():
        if category_dir.is_dir():
            if generate_category_index(category_dir):
                generated_any = True
    generate_root_index()
    print("完成。")