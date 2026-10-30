# 🚀 部署完整指南

## 总流程（按顺序做）

```
① 安装 Git → ② 推送 GitHub → ③ Cloudflare Pages 部署
→ ④ 买域名 → ⑤ 绑定域名 → ⑥ 申请 AdSense
```

---

## ① 安装 Git

1. 打开 https://git-scm.com/download/win
2. 下载安装，全部默认选项点 Next
3. 安装完后打开「命令提示符」输入 `git --version`，看到版本号说明成功

---

## ② 注册 GitHub 并推送代码

### 注册
1. 打开 https://github.com
2. 点右上角 **Sign up**，注册账号

### 创建仓库
1. 登录后点右上角 **+** → **New repository**
2. Repository name 填：`totk-guide`（或你喜欢的名字）
3. 选 **Public**（必须公开，Cloudflare 免费版需要）
4. 不要勾选任何初始化选项
5. 点 **Create repository**

### 推送代码
打开「命令提示符」，进入项目目录，依次运行：

```bash
cd "c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页"

git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/你的用户名/totk-guide.git
git push -u origin main
```

> 推送时会弹出 GitHub 登录窗口，登录即可。

---

## ③ Cloudflare Pages 部署（免费，全球 CDN）

1. 打开 https://pages.cloudflare.com
2. 注册/登录 Cloudflare 账号
3. 点 **Create a project** → **Connect to Git**
4. 授权连接你的 GitHub 账号
5. 选择刚才创建的 `totk-guide` 仓库
6. 配置如下：

   | 选项 | 填写 |
   |------|------|
   | Project name | totk-guide |
   | Production branch | main |
   | Build command | （留空） |
   | Build output directory | / |

7. 点 **Save and Deploy**
8. 等 1~2 分钟，部署完成后会给你一个免费域名，格式为：
   `https://totk-guide.pages.dev`

✅ **此时网站已上线，全球可访问！**

---

## ④ 购买域名（推荐）

### 推荐域名注册商

| 注册商 | 优点 | 链接 |
|--------|------|------|
| **Cloudflare Registrar** | 成本价，无溢价，管理最方便 | https://dash.cloudflare.com → Domains |
| **Namecheap** | 价格便宜，界面友好 | https://www.namecheap.com |
| **GoDaddy** | 知名度高，中文支持好 | https://www.godaddy.com |

### 域名选择建议

好域名的标准：
- 简短好记，最好 10 个字符以内
- 用 `.com` 或 `.net`（最通用）
- 避免数字和连字符

**推荐方向**（仅供参考，需要自己查是否可注册）：
```
totk-guide.com
totk-wiki.com
zelda-totk.com
hyrule-guide.com
```

> 💡 在 Cloudflare Registrar 买最省事，因为 DNS 和 CDN 都在同一个平台管理。

### 购买步骤（以 Cloudflare 为例）
1. 登录 https://dash.cloudflare.com
2. 左侧菜单 → **Domain Registration** → **Register Domains**
3. 搜索你想要的域名
4. 加入购物车，填写联系信息，付款
5. 域名会自动添加到你的 Cloudflare 账户

---

## ⑤ 绑定域名到 Cloudflare Pages

1. 进入 Cloudflare Pages → 你的项目 `totk-guide`
2. 点 **Custom domains** → **Set up a custom domain**
3. 输入你买的域名，例如 `www.totk-guide.com`
4. 点 **Continue**
5. 如果域名在 Cloudflare 注册，DNS 会**自动配置**
6. 如果在其他地方注册，按提示添加 CNAME 记录

### 同时绑定根域名（推荐）
重复上面步骤，再添加一次 `totk-guide.com`（不带 www）
Cloudflare 会自动把根域名重定向到 www

### 更新域名到代码里
买好域名后，在项目目录运行：
```powershell
.\set-domain.ps1 -Domain "www.totk-guide.com"
```
然后重新提交：
```bash
git add robots.txt sitemap.xml
git commit -m "update domain"
git push
```

---

## ⑥ 申请 Google AdSense（网站赚钱）

### 前提条件（必须满足）
- [ ] 网站已上线，有自己的域名（不能用 .pages.dev）
- [ ] 网站有实质内容（你的攻略内容完全满足）
- [ ] 有隐私政策页面（你已有 privacy.html ✅）
- [ ] 网站符合 Google 内容政策

### 申请步骤

1. 打开 https://www.google.com/adsense
2. 点 **开始使用**，用 Google 账号登录
3. 填写网站地址，例如 `https://www.totk-guide.com`
4. 选择国家/地区
5. 同意条款，点 **创建账号**

### 添加 AdSense 验证代码

申请后 Google 会给你一段代码，格式如下：
```html
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX"
     crossorigin="anonymous"></script>
```

需要把这段代码加到**所有页面**的 `<head>` 里。

> 告诉我你的 AdSense publisher ID（ca-pub-XXXXXXXX），
> 我帮你一次性更新所有 HTML 文件。

### 审核时间
- 提交后 Google 会审核网站，通常 **1~14 天**
- 审核通过后，可以在 AdSense 后台创建广告单元
- 把广告代码放到页面合适位置即可开始展示广告

### 广告位置建议
- 文章内容中间（效果最好）
- 侧边栏
- 页面底部
- 不要放太多，影响用户体验会降低收益

---

## 📋 完整检查清单

### 部署前
- [ ] 安装 Git
- [ ] 注册 GitHub 账号
- [ ] 创建 GitHub 仓库
- [ ] 推送代码到 GitHub

### 部署
- [ ] 注册 Cloudflare 账号
- [ ] 连接 GitHub 仓库
- [ ] 部署到 Cloudflare Pages
- [ ] 验证 .pages.dev 域名可以访问

### 域名
- [ ] 购买域名
- [ ] 在 Cloudflare Pages 绑定自定义域名
- [ ] 运行 set-domain.ps1 更新代码里的域名
- [ ] 重新推送代码

### AdSense
- [ ] 申请 Google AdSense
- [ ] 添加验证代码到所有页面
- [ ] 等待审核通过
- [ ] 创建广告单元并放置到页面

---

## 💰 预期费用

| 项目 | 费用 |
|------|------|
| Cloudflare Pages 托管 | **免费** |
| Cloudflare CDN 加速 | **免费** |
| 域名（.com，每年） | 约 **¥70~100/年** |
| Google AdSense | **免费**（Google 抽成） |

---

## ❓ 常见问题

**Q: 为什么选 Cloudflare Pages 而不是 Netlify？**
A: 你已经有 netlify.toml，两个都可以用。但 Cloudflare Pages 的 CDN 节点在中国大陆周边更多，访问速度更快，而且域名注册、DNS、CDN 全在一个平台，管理更方便。

**Q: AdSense 审核会被拒吗？**
A: 你的网站内容是原创攻略，有隐私政策页面，内容质量不错，通过率较高。被拒的话 Google 会说明原因，按要求修改后可以重新申请。

**Q: 多久能开始赚钱？**
A: 域名绑定后申请 AdSense，审核通过后立即可以展示广告。收益取决于流量，攻略类网站 SEO 起量需要 1~3 个月。

**Q: 需要备案吗？**
A: 服务器在境外（Cloudflare），不需要 ICP 备案。但如果你的目标用户主要在中国大陆，建议了解相关法规。
