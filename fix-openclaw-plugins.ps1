$extensionsPath = "C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw\extensions"
$pluginSdkPath = "C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw\dist\plugin-sdk"

$extensions = Get-ChildItem $extensionsPath -Directory

$fixed = 0
$skipped = 0

foreach ($ext in $extensions) {
    $pkgPath = Join-Path $ext.FullName "package.json"
    $pluginName = $ext.Name
    $compiledPlugin = Join-Path $pluginSdkPath "$pluginName.js"
    
    if (-not (Test-Path $pkgPath)) {
        Write-Host "SKIP: $pluginName (no package.json)" -ForegroundColor Yellow
        $skipped++
        continue
    }
    
    if (-not (Test-Path $compiledPlugin)) {
        Write-Host "SKIP: $pluginName (no compiled file)" -ForegroundColor Yellow
        $skipped++
        continue
    }
    
    $pkg = Get-Content $pkgPath -Raw | ConvertFrom-Json
    
    if ($pkg.openclaw.extensions -and $pkg.openclaw.extensions[0] -eq "./index.ts") {
        $pkg.openclaw.extensions = @("../../dist/plugin-sdk/$pluginName.js")
        $pkg | ConvertTo-Json -Depth 10 | Set-Content $pkgPath -Encoding UTF8
        Write-Host "FIXED: $pluginName" -ForegroundColor Green
        $fixed++
    } else {
        Write-Host "SKIP: $pluginName (already fixed or different entry)" -ForegroundColor Cyan
        $skipped++
    }
}

Write-Host "`n=== Summary ===" -ForegroundColor Magenta
Write-Host "Fixed: $fixed" -ForegroundColor Green
Write-Host "Skipped: $skipped" -ForegroundColor Yellow
