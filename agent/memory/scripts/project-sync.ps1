# OpenClaw 项目文档同步脚本
# 用途: 将外部项目的文档同步到 memory/*-sync/ 目录
# 执行方式: powershell -ExecutionPolicy Bypass -File project-sync.ps1

$WorkspaceRoot = "C:\Users\Administrator\Desktop\智能体"
$SyncBaseDir = Join-Path $WorkspaceRoot "memory"

Write-Host "🔄 项目文档同步脚本" -ForegroundColor Cyan
Write-Host "同步时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host ""

# 项目配置列表
# 格式: @{ Name = "项目名"; Path = "项目路径"; Docs = "文档子目录（相对路径）" }
$Projects = @(
    # 示例配置（需要根据实际项目修改）
    # @{
    #     Name = "openclaw-docs"
    #     Path = "C:\Projects\openclaw"
    #     Docs = "docs"  # 同步 docs/ 目录
    # },
    # @{
    #     Name = "my-project"
    #     Path = "D:\workspace\my-project"
    #     Docs = "README.md,docs"  # 同步 README.md 和 docs/ 目录
    # }
)

# 如果没有配置项目，提示用户
if ($Projects.Count -eq 0) {
    Write-Host "⚠️  未配置任何项目" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "请在脚本中添加项目配置，例如:" -ForegroundColor Gray
    Write-Host '  @{' -ForegroundColor Gray
    Write-Host '      Name = "my-project"' -ForegroundColor Gray
    Write-Host '      Path = "D:\path\to\project"' -ForegroundColor Gray
    Write-Host '      Docs = "docs"  # 或 "README.md,docs"' -ForegroundColor Gray
    Write-Host '  }' -ForegroundColor Gray
    Write-Host ""
    Write-Host "配置后，该脚本会将项目文档同步到:" -ForegroundColor Gray
    Write-Host "  memory\<项目名>-sync\" -ForegroundColor Gray
    exit 0
}

# 同步函数
function Sync-Project {
    param (
        [string]$Name,
        [string]$Path,
        [string]$Docs
    )
    
    Write-Host "[$Name]" -NoNewline -ForegroundColor White
    
    # 检查项目路径是否存在
    if (-not (Test-Path $Path)) {
        Write-Host " ❌ 项目路径不存在: $Path" -ForegroundColor Red
        return $false
    }
    
    # 创建同步目标目录
    $SyncDir = Join-Path $SyncBaseDir "$Name-sync"
    if (-not (Test-Path $SyncDir)) {
        New-Item -ItemType Directory -Path $SyncDir -Force | Out-Null
    }
    
    # 解析文档路径（支持逗号分隔）
    $DocPaths = $Docs -split ","
    $SyncedFiles = 0
    
    foreach ($DocPath in $DocPaths) {
        $DocPath = $DocPath.Trim()
        $SourcePath = Join-Path $Path $DocPath
        
        if (-not (Test-Path $SourcePath)) {
            Write-Host " ⚠️ 文档路径不存在: $DocPath" -ForegroundColor Yellow
            continue
        }
        
        # 如果是文件，直接复制
        if (Test-Path $SourcePath -PathType Leaf) {
            $DestPath = Join-Path $SyncDir (Split-Path $DocPath -Leaf)
            Copy-Item -Path $SourcePath -Destination $DestPath -Force
            $SyncedFiles++
        }
        # 如果是目录，递归复制所有 .md 文件
        elseif (Test-Path $SourcePath -PathType Container) {
            $MarkdownFiles = Get-ChildItem -Path $SourcePath -Filter "*.md" -Recurse
            foreach ($File in $MarkdownFiles) {
                $RelativePath = $File.FullName.Substring($SourcePath.Length + 1)
                $DestPath = Join-Path $SyncDir $RelativePath
                $DestDir = Split-Path $DestPath -Parent
                
                if (-not (Test-Path $DestDir)) {
                    New-Item -ItemType Directory -Path $DestDir -Force | Out-Null
                }
                
                Copy-Item -Path $File.FullName -Destination $DestPath -Force
                $SyncedFiles++
            }
        }
    }
    
    # 写入同步时间戳
    $TimestampFile = Join-Path $SyncDir ".last-sync-ts"
    Get-Date -Format "yyyy-MM-dd HH:mm:ss" | Out-File -FilePath $TimestampFile -Encoding UTF8
    
    Write-Host " ✅ 同步完成 ($SyncedFiles 个文件)" -ForegroundColor Green
    return $true
}

# 执行同步
$SuccessCount = 0
$FailCount = 0

foreach ($Project in $Projects) {
    $Result = Sync-Project -Name $Project.Name -Path $Project.Path -Docs $Project.Docs
    if ($Result) {
        $SuccessCount++
    } else {
        $FailCount++
    }
}

# 总结
Write-Host ""
Write-Host "═══════════════════════════════════════" -ForegroundColor Cyan
Write-Host "同步结果: $SuccessCount 成功, $FailCount 失败" -ForegroundColor White
Write-Host "═══════════════════════════════════════" -ForegroundColor Cyan

if ($FailCount -gt 0) {
    exit 1
} else {
    exit 0
}
