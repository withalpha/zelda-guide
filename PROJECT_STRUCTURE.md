# 项目结构说明

## 📁 目录结构

```
我的游戏网页/
├── src/                          # 源代码目录
│   ├── pages/                    # HTML页面
│   │   ├── index.html           # 首页
│   │   ├── about.html           # 关于我们
│   │   ├── mauyu-lost.html      # 魔犹伊的遗失物
│   │   ├── cooking.html         # 料理合成
│   │   ├── clothes.html         # 套装获取
│   │   ├── weapons.html         # 武器图鉴
│   │   ├── shrines.html         # 神庙挑战
│   │   ├── shrine-unlock.html   # 神庙开启
│   │   ├── roots.html           # 破魔树根
│   │   ├── main-quest.html      # 主线任务
│   │   ├── side-quest.html      # 情节挑战
│   │   ├── privacy.html         # 隐私政策
│   │   └── 404.html             # 404页面
│   ├── assets/                   # 资源文件
│   │   ├── images/              # 图片资源
│   │   ├── Items/               # 游戏物品图片
│   │   └── scripts/             # 脚本文件
│   │       ├── style.css        # 样式表
│   │       ├── main.js          # 主脚本
│   │       └── ...
│   └── data/                     # 数据文件
│       ├── correct_dishes_mapping.json
│       ├── dishes_output.js
│       ├── final_true_match.json
│       ├── pixel_match_result.json
│       └── true_match_result.json
├── tools/                        # 工具和脚本
│   ├── scripts/                  # Python脚本
│   │   ├── analyze_grid.py
│   │   ├── bg_match.py
│   │   ├── build_cook_mapping.py
│   │   ├── build_mapping.py
│   │   ├── count_records.py
│   │   ├── create_mapping.py
│   │   ├── deploy_names.py
│   │   ├── export_cook_mapping.py
│   │   ├── final_mapping.py
│   │   ├── final_ocr_mapping.py
│   │   ├── final_true_match.py
│   │   ├── fix_cooking_html.py
│   │   ├── fix_dishes_array.py
│   │   ├── generate_correct_dishes.py
│   │   ├── generate_dishes.py
│   │   ├── generate_json_mapping.py
│   │   ├── match_dishes.py
│   │   ├── ocr_and_match.py
│   │   ├── pixel_match.py
│   │   ├── precise_match.py
│   │   ├── reclassify.py
│   │   ├── true_pixel_match.py
│   │   ├── update_cooking.py
│   │   ├── verify_deploy.py
│   │   ├── verify_dishes.py
│   │   ├── verify_json.py
│   │   └── verify_mapping.py
│   └── debug/                    # 调试文件和临时数据
│       ├── col2_test/
│       ├── compare_view/
│       ├── debug_cells/
│       ├── grid_cells/
│       ├── grid_cells2/
│       ├── pixel_match_debug/
│       ├── true_match_debug/
│       ├── _data/
│       ├── _tools/
│       ├── bg_match_result.txt
│       ├── bg_match_result.json
│       ├── cooking照片命名说明.txt
│       ├── final_true_match.txt
│       ├── item_cook_mapping.txt
│       ├── item_cook_mapping.xlsx
│       └── true_match_result.txt
├── docs/                         # 文档
│   ├── README.md
│   ├── BUG_FIXES.md
│   ├── BUG_CHECK_REPORT_2026-05-28.md
│   └── MAPPING_REPORT.md
├── config/                       # 配置文件
│   ├── netlify.toml
│   ├── robots.txt
│   └── sitemap.xml
└── .vscode/                      # VS Code配置
```

## 📋 文件分类说明

### src/ - 源代码目录
- **pages/**: 所有HTML页面文件
- **assets/**: 网站资源
  - images/: 网站图片（背景、图标等）
  - Items/: 游戏物品高清图片
  - scripts/: CSS和JavaScript文件
- **data/**: 数据文件（JSON、JS数据）

### tools/ - 工具和脚本
- **scripts/**: Python脚本（数据处理、图片匹配等）
- **debug/**: 调试文件、临时数据、测试结果

### docs/ - 文档
- 项目文档、Bug报告、映射报告等

### config/ - 配置文件
- 部署配置（Netlify）
- SEO配置（robots.txt、sitemap.xml）

## 🔗 文件引用更新

### HTML文件中的引用需要更新为：
```html
<!-- 样式表 -->
<link rel="stylesheet" href="../assets/scripts/style.css">

<!-- 脚本 -->
<script src="../assets/scripts/main.js"></script>

<!-- 图片 -->
<img src="../assets/images/..." alt="...">
<img src="../assets/Items/..." alt="...">

<!-- 数据 -->
<script src="../data/dishes_output.js"></script>
```

## 📝 整理说明

### 整理日期
2026-05-28

### 整理内容
1. ✅ 创建了清晰的目录结构
2. ✅ 分离了源代码、工具和文档
3. ✅ 整理了调试文件和临时数据
4. ✅ 集中管理配置文件

### 下一步建议
1. 更新HTML文件中的资源引用路径
2. 更新Python脚本中的文件路径
3. 考虑添加.gitignore文件
4. 建立开发和生产环境的区分

## 🚀 快速开始

### 开发环境
```bash
# 进入项目目录
cd 我的游戏网页

# 查看源代码
cd src/pages/

# 查看脚本
cd tools/scripts/
```

### 部署
```bash
# 部署配置在 config/netlify.toml
# 确保部署时指向 src/ 目录
```

---

**整理人**: Kiro IDE  
**整理时间**: 2026-05-28  
**项目状态**: ✅ 已整理
