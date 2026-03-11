$sdkPath = "C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw\dist\plugin-sdk"
$extPath = "C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw\extensions"

$plugins = Get-ChildItem $sdkPath -Filter "*.js" | Where-Object { $_.Name -notmatch "^(index|compat|core)" }

$copied = 0

foreach ($plugin in $plugins) {
    $name = $plugin.BaseName
    $targetDir = Join-Path $extPath $name
    $targetFile = Join-Path $targetDir "index.js"
    $pkgFile = Join-Path $targetDir "package.json"
    
    if (-not (Test-Path $targetDir)) {
        Write-Host "SKIP: $name (no extension dir)" -ForegroundColor Yellow
        continue
    }
    
    Copy-Item $plugin.FullName $targetFile -Force
    
    if (Test-Path $pkgFile) {
        $pkg = Get-Content $pkgFile -Raw | ConvertFrom-Json
        if ($pkg.openclaw.extensions) {
            $pkg.openclaw.extensions = @("./index.js")
            $pkg | ConvertTo-Json -Depth 10 | Set-Content $pkgFile -Encoding UTF8
        }
    }
    
    Write-Host "COPIED: $name" -ForegroundColor Green
    $copied++
}

Write-Host "`nTotal copied: $copied" -ForegroundColor Magenta
