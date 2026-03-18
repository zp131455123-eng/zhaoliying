# Test DashScope Embedding API
$ApiKey = $env:DASHSCOPE_API_KEY
if (-not $ApiKey) {
    # Read from .env file
    $EnvFile = "$env:USERPROFILE\.openclaw\.env"
    if (Test-Path $EnvFile) {
        $Content = Get-Content $EnvFile -Raw
        if ($Content -match 'DASHSCOPE_API_KEY=(.+)') {
            $ApiKey = $Matches[1].Trim()
        }
    }
}

if (-not $ApiKey) {
    Write-Host "ERROR: DASHSCOPE_API_KEY not found" -ForegroundColor Red
    exit 1
}

Write-Host "Testing DashScope Embedding API..." -ForegroundColor Cyan
Write-Host "API Key: $($ApiKey.Substring(0,8))..." -ForegroundColor Gray
Write-Host ""

# Test 1: OpenAI Compatible Mode with different models
$Models = @(
    "text-embedding-v1",
    "text-embedding-v2", 
    "text-embedding-v3",
    "text-embedding-ada-002"
)

$BaseUrl = "https://dashscope.aliyuncs.com/compatible-mode/v1"

foreach ($Model in $Models) {
    Write-Host "Testing model: $Model" -NoNewline
    
    $Body = @{
        model = $Model
        input = "测试文本"
    } | ConvertTo-Json -Depth 10
    
    try {
        $Response = Invoke-RestMethod -Uri "$BaseUrl/embeddings" `
            -Method Post `
            -Headers @{
                "Authorization" = "Bearer $ApiKey"
                "Content-Type" = "application/json"
            } `
            -Body $Body `
            -TimeoutSec 10 `
            -ErrorAction Stop
        
        $Dimension = $Response.data[0].embedding.Count
        Write-Host " - SUCCESS (dimension: $Dimension)" -ForegroundColor Green
        
        # Found working model, save it
        Write-Host ""
        Write-Host "=== Working Configuration ===" -ForegroundColor Green
        Write-Host "Model: $Model"
        Write-Host "Dimension: $Dimension"
        Write-Host "Base URL: $BaseUrl"
        Write-Host ""
        exit 0
        
    } catch {
        $ErrorMsg = $_.Exception.Message
        if ($ErrorMsg -match '"code":"(.+?)"') {
            $Code = $Matches[1]
            Write-Host " - FAIL ($Code)" -ForegroundColor Red
        } else {
            Write-Host " - FAIL" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "All models failed. Please check:" -ForegroundColor Yellow
Write-Host "1. API Key is valid and has Embedding service enabled"
Write-Host "2. Visit: https://dashscope.console.aliyun.com/"
Write-Host "3. Check 'Model Service' > 'Embedding'"
Write-Host ""

exit 1
