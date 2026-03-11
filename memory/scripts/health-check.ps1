# OpenClaw Memory System Health Check Script
# Usage: powershell -ExecutionPolicy Bypass -File health-check.ps1

$WorkspaceRoot = "C:\Users\Administrator\Desktop\智能体"
$ErrorCount = 0
$WarningCount = 0
$PassCount = 0

Write-Host "=== OpenClaw Memory System Health Check ===" -ForegroundColor Cyan
Write-Host "Check Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host ""

# Check 1: Today's log exists
Write-Host "[1/11] Checking today's log..." -NoNewline
$TodayLog = Join-Path $WorkspaceRoot "memory\logs\$(Get-Date -Format 'yyyy-MM-dd').md"
if (Test-Path $TodayLog) {
    Write-Host " PASS" -ForegroundColor Green
    $PassCount++
} else {
    Write-Host " FAIL - Today's log not found" -ForegroundColor Red
    $ErrorCount++
}

# Check 2: MEMORY.md line count
Write-Host "[2/11] Checking MEMORY.md size..." -NoNewline
$MemoryFile = Join-Path $WorkspaceRoot "MEMORY.md"
if (Test-Path $MemoryFile) {
    $LineCount = (Get-Content $MemoryFile).Count
    if ($LineCount -le 150) {
        Write-Host " PASS ($LineCount/150 lines)" -ForegroundColor Green
        $PassCount++
    } else {
        Write-Host " WARN - Exceeds 150 lines ($LineCount lines), needs archiving" -ForegroundColor Yellow
        $WarningCount++
    }
} else {
    Write-Host " FAIL - MEMORY.md not found" -ForegroundColor Red
    $ErrorCount++
}

# Check 3: Core files integrity
Write-Host "[3/11] Checking core files..." -NoNewline
$CoreFiles = @("MEMORY.md", "SOUL.md", "USER.md", "TOOLS.md", "AGENTS.md")
$MissingFiles = @()
foreach ($File in $CoreFiles) {
    if (-not (Test-Path (Join-Path $WorkspaceRoot $File))) {
        $MissingFiles += $File
    }
}
if ($MissingFiles.Count -eq 0) {
    Write-Host " PASS" -ForegroundColor Green
    $PassCount++
} else {
    Write-Host " FAIL - Missing: $($MissingFiles -join ', ')" -ForegroundColor Red
    $ErrorCount++
}

# Check 4: memory/ directory structure
Write-Host "[4/11] Checking memory/ directories..." -NoNewline
$RequiredDirs = @("memory\logs", "memory\archive", "memory\scripts")
$MissingDirs = @()
foreach ($Dir in $RequiredDirs) {
    if (-not (Test-Path (Join-Path $WorkspaceRoot $Dir))) {
        $MissingDirs += $Dir
    }
}
if ($MissingDirs.Count -eq 0) {
    Write-Host " PASS" -ForegroundColor Green
    $PassCount++
} else {
    Write-Host " FAIL - Missing: $($MissingDirs -join ', ')" -ForegroundColor Red
    $ErrorCount++
}

# Check 5: memory/ core files
Write-Host "[5/11] Checking memory/ files..." -NoNewline
$MemoryFiles = @(
    "memory\lessons.md",
    "memory\projects.md",
    "memory\tools-notes.md",
    "memory\evolution.md",
    "memory\archive-index.md"
)
$MissingMemoryFiles = @()
foreach ($File in $MemoryFiles) {
    if (-not (Test-Path (Join-Path $WorkspaceRoot $File))) {
        $MissingMemoryFiles += $File
    }
}
if ($MissingMemoryFiles.Count -eq 0) {
    Write-Host " PASS" -ForegroundColor Green
    $PassCount++
} else {
    Write-Host " FAIL - Missing: $($MissingMemoryFiles -join ', ')" -ForegroundColor Red
    $ErrorCount++
}

# Check 6: .env file
Write-Host "[6/11] Checking .env file..." -NoNewline
$EnvFile = "$env:USERPROFILE\.openclaw\.env"
if (Test-Path $EnvFile) {
    Write-Host " PASS - Configured" -ForegroundColor Green
    $PassCount++
} else {
    Write-Host " WARN - Not configured (may affect semantic search)" -ForegroundColor Yellow
    $WarningCount++
}

# Check 7: .gitignore
Write-Host "[7/11] Checking .gitignore..." -NoNewline
$GitignoreFile = Join-Path $WorkspaceRoot ".gitignore"
if (Test-Path $GitignoreFile) {
    $Content = Get-Content $GitignoreFile -Raw
    if ($Content -match "\.env") {
        Write-Host " PASS" -ForegroundColor Green
        $PassCount++
    } else {
        Write-Host " WARN - Missing .env entry" -ForegroundColor Yellow
        $WarningCount++
    }
} else {
    Write-Host " FAIL - .gitignore not found" -ForegroundColor Red
    $ErrorCount++
}

# Check 8: Recent logs (last 7 days)
Write-Host "[8/11] Checking recent logs..." -NoNewline
$LogsDir = Join-Path $WorkspaceRoot "memory\logs"
if (Test-Path $LogsDir) {
    $RecentLogs = Get-ChildItem $LogsDir -Filter "*.md" | Where-Object {
        $_.LastWriteTime -gt (Get-Date).AddDays(-7)
    }
    if ($RecentLogs.Count -gt 0) {
        Write-Host " PASS ($($RecentLogs.Count) recent logs)" -ForegroundColor Green
        $PassCount++
    } else {
        Write-Host " WARN - No logs in last 7 days" -ForegroundColor Yellow
        $WarningCount++
    }
} else {
    Write-Host " FAIL - logs directory not found" -ForegroundColor Red
    $ErrorCount++
}

# Check 9: Vector database
Write-Host "[9/11] Checking vector database..." -NoNewline
$VectorDB = "$env:USERPROFILE\.openclaw\memory\main.sqlite"
if (Test-Path $VectorDB) {
    $Size = (Get-Item $VectorDB).Length / 1KB
    Write-Host " PASS ($([math]::Round($Size, 1)) KB)" -ForegroundColor Green
    $PassCount++
} else {
    Write-Host " WARN - Vector DB not initialized" -ForegroundColor Yellow
    $WarningCount++
}

# Check 10: Git repository status
Write-Host "[10/11] Checking Git status..." -NoNewline
Push-Location $WorkspaceRoot
if (Test-Path ".git") {
    $GitStatus = git status --porcelain 2>$null
    if ($LASTEXITCODE -eq 0) {
        if ([string]::IsNullOrWhiteSpace($GitStatus)) {
            Write-Host " PASS - No uncommitted changes" -ForegroundColor Green
            $PassCount++
        } else {
            $Changes = ($GitStatus -split "`n").Count
            Write-Host " WARN - $Changes files uncommitted" -ForegroundColor Yellow
            $WarningCount++
        }
    } else {
        Write-Host " WARN - Git command failed" -ForegroundColor Yellow
        $WarningCount++
    }
} else {
    Write-Host " SKIP - Git not initialized" -ForegroundColor Gray
    $PassCount++
}
Pop-Location

# Check 11: OpenClaw Gateway status
Write-Host "[11/11] Checking OpenClaw Gateway..." -NoNewline
try {
    $GatewayCheck = openclaw status 2>&1 | Out-String
    if ($GatewayCheck -match "OK|Running") {
        Write-Host " PASS - Running" -ForegroundColor Green
        $PassCount++
    } else {
        Write-Host " WARN - Status unknown" -ForegroundColor Yellow
        $WarningCount++
    }
} catch {
    Write-Host " FAIL - Cannot check" -ForegroundColor Red
    $ErrorCount++
}

# Summary
Write-Host ""
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "Summary:" -ForegroundColor White
Write-Host "  PASS: $PassCount" -ForegroundColor Green
Write-Host "  WARN: $WarningCount" -ForegroundColor Yellow
Write-Host "  FAIL: $ErrorCount" -ForegroundColor Red
Write-Host "=======================================" -ForegroundColor Cyan

# Exit code
if ($ErrorCount -gt 0) {
    exit 1
} elseif ($WarningCount -gt 0) {
    exit 2
} else {
    exit 0
}
