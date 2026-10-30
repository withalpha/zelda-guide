# 快速参考卡

## 🎯 项目整理完成

### 📁 新的目录结构

```
我的游戏网页/
├── src/                    # 源代码（网站文件）
│   ├── pages/             # 13个HTML页面
│   ├── assets/            # 资源（图片、样式、脚本）
│   └── data/              # 数据文件
├── tools/                 # 工具和脚本
│   ├── scripts/           # 27个Python脚本
│   └── debug/             # 调试文件和临时数据
├── docs/                  # 文档
├── config/                # 配置文件
└── .vscode/               # VS Code配置
```

## 🔗 文件位置速查

### HTML页面
```
src/pages/
├── index.html             # 首页
├── about.html             # 关于我们
├── mauyu-lost.html        # 魔犹伊的遗失物
├── cooking.html           # 料理合成
├── clothes.html           # 套装获取
├── weapons.html           # 武器图鉴
├── shrines.html           # 神庙挑战
├── shrine-unlock.html     # 神庙开启
├── roots.html             # 破魔树根
├── main-quest.html        # 主线任务
├── side-quest.html        # 情节挑战
├── privacy.html           # 隐私政策
└── 404.html               # 404页面
```

### 资源文件
```
src/assets/
├── images/                # 网站图片
├── Items/                 # 游戏物品高清图片
└── scripts/
    ├── style.css          # 样式表
    └── main.js            # 主脚本
```

### 数据文件
```
src/data/
├── correct_dishes_mapping.json
├── dishes_output.js
├── final_true_match.json
├── pixel_match_result.json
└── true_match_result.json
```

### Python脚本
```
tools/scripts/
├── analyze_grid.py
├── bg_match.py
├── build_cook_mapping.py
├── build_mapping.py
├── count_records.py
├── create_mapping.py
├── deploy_names.py
├── export_cook_mapping.py
├── final_mapping.py
├── final_ocr_mapping.py
├── final_true_match.py
├── fix_cooking_html.py
├── fix_dishes_array.py
├── generate_correct_dishes.py
├── generate_dishes.py
├── generate_json_mapping.py
├── match_dishes.py
├── ocr_and_match.py
├── pixel_match.py
├── precise_match.py
├── reclassify.py
├── true_pixel_match.py
├── update_cooking.py
├── verify_deploy.py
├── verify_dishes.py
├── verify_json.py
└── verify_mapping.py
```

## 📝 路径更新示例

### 在HTML中引用资源

**样式表**:
```html
<link rel="stylesheet" href="assets/scripts/style.css">
```

**脚本**:
```html
<script src="assets/scripts/main.js"></script>
```

**图片**:
```html
<img src="assets/images/..." alt="...">
<img src="assets/Items/..." alt="...">
```

**数据**:
```html
<script src="data/dishes_output.js"></script>
```

## 🚀 常用命令

### 查看项目结构
```bash
cd "c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页"
tree /F
```

### 运行Python脚本
```bash
cd tools/scripts
python script_name.py
```

### 本地测试网站
```bash
# 进入项目目录
cd "c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页"

# 使用Python启动HTTP服务器
python -m http.server 8000

# 访问 http://localhost:8000/src/pages/index.html
```

## 📊 项目统计

| 项目 | 数量 |
|------|------|
| HTML页面 | 13 |
| Python脚本 | 27 |
| 数据文件 | 5 |
| 文档 | 4 |
| 配置文件 | 3 |
| **总计** | **52** |

## ✅ 整理清单

- [x] 创建新的目录结构
- [x] 移动HTML页面到 src/pages/
- [x] 移动资源文件到 src/assets/
- [x] 移动数据文件到 src/data/
- [x] 移动Python脚本到 tools/scripts/
- [x] 移动调试文件到 tools/debug/
- [x] 移动文档到 docs/
- [x] 移动配置文件到 config/
- [ ] 更新HTML文件中的资源路径
- [ ] 测试所有页面
- [ ] 更新部署配置

## 📚 相关文档

- **PROJECT_STRUCTURE.md** - 详细的项目结构说明
- **UPDATE_PATHS.md** - 文件路径更新指南
- **BUG_CHECK_REPORT_2026-05-28.md** - Bug检查报告
- **BUG_FIXES.md** - Bug修复记录

## 💡 提示

1. **相对路径**: HTML文件在 `src/pages/` 中，所以引用资源时使用 `../assets/...`
2. **图片路径**: 所有图片都在 `src/assets/` 下，包括 `images/` 和 `Items/`
3. **数据文件**: 数据文件在 `src/data/` 中
4. **脚本**: Python脚本在 `tools/scripts/` 中，调试文件在 `tools/debug/` 中

## 🔧 故障排除

### 资源加载失败
- 检查HTML文件中的路径是否正确
- 确保使用相对路径而不是绝对路径
- 检查文件是否真的存在于指定位置

### 脚本不工作
- 检查 `main.js` 是否正确加载
- 检查浏览器控制台是否有错误信息
- 确保CSS文件也正确加载

### 图片不显示
- 检查图片路径是否正确
- 确保图片文件存在
- 检查文件名大小写是否匹配

---

**整理日期**: 2026-05-28  
**项目状态**: ✅ 已整理  
**最后更新**: 2026-05-28
