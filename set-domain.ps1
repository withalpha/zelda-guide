# ============================================================
# 用法：在项目根目录运行
#   .\set-domain.ps1 -Domain "www.yourdomain.com"
# ============================================================
param(
    [Parameter(Mandatory=$true)]
    [string]$Domain
)

$base = $PSScriptRoot
$files = @("robots.txt", "sitemap.xml")

foreach ($f in $files) {
    $path = Join-Path $base $f
    if (Test-Path $path) {
        $content = Get-Content $path -Raw -Encoding UTF8
        $updated = $content -replace "YOUR_DOMAIN", $Domain
        Set-Content -Path $path -Value $updated -Encoding UTF8 -NoNewline
        Write-Host "✓ 已更新 $f" -ForegroundColor Green
    }
}

Write-Host "`n✅ 域名已设置为: $Domain" -ForegroundColor Cyan
Write-Host "   记得重新提交到 GitHub！" -ForegroundColor Yellow
