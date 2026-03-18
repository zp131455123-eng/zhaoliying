# -*- coding: utf-8 -*-
# git-sync.ps1 - 自动同步工作空间到 GitHub
# 每天凌晨2点由任务计划执行

$workspace = "C:\Users\Administrator\Desktop\智能体"
$logFile = "$workspace\memory\logs\git-sync.log"
$date = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Set-Location $workspace

# 检查是否有改动
$status = git status --porcelain
if (-not $status) {
    Add-Content $logFile "[$date] No changes, skip."
    exit 0
}

# 提交并推送
git add .
$commitMsg = "auto-sync: $((Get-Date -Format 'yyyy-MM-dd HH:mm'))"
git commit -m $commitMsg
$pushResult = git push 2>&1

if ($LASTEXITCODE -eq 0) {
    Add-Content $logFile "[$date] OK: $commitMsg"
} else {
    Add-Content $logFile "[$date] FAIL: $pushResult"
}
