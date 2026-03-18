# -*- coding: utf-8 -*-
"""主入口：串联执行 Step1 + Step2"""
import os, sys, subprocess, datetime

env_file = os.path.expanduser("~/.openclaw/.env")
env = os.environ.copy()
env["PYTHONIOENCODING"] = "utf-8"
if os.path.exists(env_file):
    with open(env_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env.setdefault(k.strip(), v.strip())

here = os.path.dirname(os.path.abspath(__file__))
today = datetime.date.today().strftime("%Y-%m-%d")

print("🚀 AI视频自动化流水线启动")
print("=" * 50)

# Step 1
print("\n--- Step 1: 热点抓取 ---")
r1 = subprocess.run(
    [sys.executable, os.path.join(here, "step1_hotspot.py")],
    env=env, capture_output=False, text=True, cwd=here
)
if r1.returncode != 0:
    print("❌ Step1 失败，终止")
    sys.exit(1)

hotspots_file = os.path.join(here, "output", today, "hotspots.json")
if not os.path.exists(hotspots_file):
    print(f"❌ 找不到热点输出文件: {hotspots_file}")
    sys.exit(1)

# Step 2
print("\n--- Step 2: 文案生成 ---")
r2 = subprocess.run(
    [sys.executable, os.path.join(here, "step2_script.py")],
    env=env, capture_output=False, text=True, cwd=here
)
if r2.returncode != 0:
    print("❌ Step2 失败，终止")
    sys.exit(1)

scripts_file = os.path.join(here, "output", today, "scripts.json")
print(f"\n\n✅ 全流程完成！输出目录: {os.path.join(here, 'output', today)}")
