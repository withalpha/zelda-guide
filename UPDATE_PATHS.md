# 文件路径更新指南

## ⚠️ 重要：需要更新的文件引用

由于文件已重新组织，需要更新HTML文件中的资源引用路径。

### 更新规则

#### 1. 样式表引用
**旧路径**:
```html
<link rel="stylesheet" href="style.css">
```

**新路径**:
```html
<link rel="stylesheet" href="assets/scripts/style.css">
```

#### 2. JavaScript引用
**旧路径**:
```html
<script src="main.js"></script>
```

**新路径**:
```html
<script src="assets/scripts/main.js"></script>
```

#### 3. 图片引用
**旧路径**:
```html
<img src="images/clothes/..." alt="...">
<img src="Items/..." alt="...">
```

**新路径**:
```html
<img src="assets/images/clothes/..." alt="...">
<img src="assets/Items/..." alt="...">
```

#### 4. 数据文件引用
**旧路径**:
```html
<script src="dishes_output.js"></script>
```

**新路径**:
```html
<script src="data/dishes_output.js"></script>
```

## 📝 需要更新的HTML文件

以下文件需要更新资源引用路径：

- [ ] src/pages/index.html
- [ ] src/pages/about.html
- [ ] src/pages/mauyu-lost.html
- [ ] src/pages/cooking.html
- [ ] src/pages/clothes.html
- [ ] src/pages/weapons.html
- [ ] src/pages/shrines.html
- [ ] src/pages/shrine-unlock.html
- [ ] src/pages/roots.html
- [ ] src/pages/main-quest.html
- [ ] src/pages/side-quest.html
- [ ] src/pages/privacy.html
- [ ] src/pages/404.html

## 🔧 自动更新脚本

如果需要自动更新所有HTML文件中的路径，可以运行以下PowerShell脚本：

```powershell
$pagesPath = "c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\src\pages"

Get-ChildItem -Path $pagesPath -Filter "*.html" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    
    # 更新样式表
    $content = $content -replace 'href="style\.css"', 'href="../assets/scripts/style.css"'
    
    # 更新主脚本
    $content = $content -replace 'src="main\.js"', 'src="../assets/scripts/main.js"'
    
    # 更新图片路径
    $content = $content -replace 'src="images/', 'src="../assets/images/'
    $content = $content -replace 'src="Items/', 'src="../assets/Items/'
    
    # 更新数据文件
    $content = $content -replace 'src="dishes_output\.js"', 'src="../data/dishes_output.js"'
    
    # 保存更新
    Set-Content -Path $_.FullName -Value $content
    Write-Host "✓ 已更新: $($_.Name)" -ForegroundColor Green
}

Write-Host "`n✅ 所有HTML文件路径已更新！" -ForegroundColor Green
```

## 📋 检查清单

更新完成后，请检查以下项目：

- [ ] 所有HTML文件都能正确加载CSS样式
- [ ] 所有JavaScript功能都能正常工作
- [ ] 所有图片都能正确显示
- [ ] 所有数据文件都能正确加载
- [ ] 网站在浏览器中能正常访问
- [ ] 所有链接都能正确跳转

## 🚀 部署注意事项

### Netlify部署
如果使用Netlify部署，需要更新`config/netlify.toml`中的构建设置：

```toml
[build]
  command = "echo 'Building...'"
  publish = "src"
```

### 本地测试
在本地测试时，可以使用简单的HTTP服务器：

```bash
# 使用Python
python -m http.server 8000

# 或使用Node.js
npx http-server
```

然后访问 `http://localhost:8000/src/pages/index.html`

---

**更新日期**: 2026-05-28  
**状态**: ⏳ 待执行
