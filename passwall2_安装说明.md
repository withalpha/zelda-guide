# Passwall2 完整安装指南

## 📋 你需要的文件

从 [GitHub Release 26.6.3-1](https://github.com/Openwrt-Passwall/openwrt-passwall2/releases/tag/26.6.3-1) 下载：

1. ✅ **主程序**（你已有）：`luci-app-passwall2_26.6.3-r1_all.ipk`
2. ✅ **语言包**（你已有）：`luci-i18n-passwall2-zh-cn_26.6.3_all.ipk`
3. ❌ **依赖包**（缺少，需要下载）

## 🔴 缺少的依赖包

你的错误提示需要这些依赖：
- coreutils-base64
- coreutils-nohup
- lyaml
- tcping
- geoview
- v2ray-geoip
- v2ray-geosite

## 🚀 方案一：使用自动安装脚本（推荐）

### 步骤 1：上传文件到路由器

将以下文件上传到路由器的 `/tmp` 目录：
- `install_passwall2.sh`（我已生成）
- `luci-app-passwall2_26.6.3-r1_all.ipk`
- `luci-i18n-passwall2-zh-cn_26.6.3_all.ipk`

### 步骤 2：SSH 连接路由器并执行

```bash
# 进入文件目录
cd /tmp

# 给脚本执行权限
chmod +x install_passwall2.sh

# 运行安装脚本
sh install_passwall2.sh
```

脚本会自动：
1. 检测你的设备架构
2. 更新软件源
3. 尝试安装依赖
4. 添加 Passwall 专用源
5. 安装主程序和语言包

---

## 🛠️ 方案二：手动安装（如果脚本失败）

### 步骤 1：检查架构

```bash
opkg print-architecture
```

记住输出中优先级最高的架构（数字最大的），例如：
- `aarch64_cortex-a53`
- `x86_64`
- `mipsel_24kc`

### 步骤 2：添加 Passwall 源

```bash
# 编辑配置文件
vi /etc/opkg/customfeeds.conf
```

添加以下内容（**替换 YOUR_ARCH 为你的架构**）：

```
src/gz passwall_packages https://github.com/xiaorouji/openwrt-passwall-packages/releases/download/latest/YOUR_ARCH
```

例如，如果架构是 `aarch64_cortex-a53`：
```
src/gz passwall_packages https://github.com/xiaorouji/openwrt-passwall-packages/releases/download/latest/aarch64_cortex-a53
```

### 步骤 3：更新源并安装依赖

```bash
# 更新
opkg update

# 安装基础工具
opkg install coreutils coreutils-base64 coreutils-nohup

# 安装 Passwall 依赖
opkg install lyaml tcping geoview v2ray-geoip v2ray-geosite
```

### 步骤 4：安装主程序和语言包

```bash
cd /tmp

# 安装主程序
opkg install luci-app-passwall2_26.6.3-r1_all.ipk

# 安装语言包
opkg install luci-i18n-passwall2-zh-cn_26.6.3_all.ipk
```

---

## 🔧 方案三：从 GitHub 手动下载所有依赖包

如果上面的源都无法访问，需要手动下载所有依赖的 `.ipk` 文件：

### 依赖包下载地址（根据你的架构选择）

访问以下页面下载对应架构的包：

1. **Passwall 依赖包**：
   https://github.com/xiaorouji/openwrt-passwall-packages/releases

2. **OpenWrt 官方包**：
   https://downloads.openwrt.org/releases/

需要下载的具体文件：
- `coreutils-base64_xxx.ipk`
- `coreutils-nohup_xxx.ipk`
- `lyaml_xxx.ipk`
- `tcping_xxx.ipk`
- `geoview_xxx.ipk`
- `v2ray-geoip_xxx.ipk`
- `v2ray-geosite_xxx.ipk`

全部下载后上传到路由器，然后：

```bash
cd /tmp

# 一次性安装所有依赖
opkg install *.ipk
```

---

## ✅ 安装完成后

```bash
# 重启 LuCI 服务
/etc/init.d/uhttpd restart

# 或者重启路由器
reboot
```

然后在浏览器访问路由器管理界面，在 **服务** → **PassWall2** 中进行配置。

---

## 🆘 如果还是失败

请执行以下命令并把输出发给我：

```bash
# 1. 查看架构
opkg print-architecture

# 2. 查看 OpenWrt 版本
cat /etc/openwrt_release

# 3. 查看可用的包
opkg update
opkg list | grep -E "coreutils|lyaml|tcping|geoview|v2ray"
```

我会根据你的具体情况给出精确的下载链接。
