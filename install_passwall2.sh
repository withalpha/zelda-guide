#!/bin/sh
# Passwall2 完整安装脚本
# 使用方法：将此脚本上传到 OpenWrt 路由器，然后执行 sh install_passwall2.sh

echo "================================"
echo "Passwall2 自动安装脚本"
echo "================================"

# 1. 检查设备架构
echo ""
echo "[步骤 1/5] 检测设备架构..."
ARCH=$(opkg print-architecture | grep -v "all\|noarch" | awk '{print $2}' | head -n 1)
echo "检测到架构: $ARCH"

# 2. 更新软件源
echo ""
echo "[步骤 2/5] 更新软件源..."
opkg update

# 3. 尝试安装依赖（从官方源）
echo ""
echo "[步骤 3/5] 安装依赖包..."

# 基础依赖
echo "安装 coreutils 工具..."
opkg install coreutils coreutils-base64 coreutils-nohup 2>/dev/null || echo "部分 coreutils 已安装或需要手动下载"

# 其他依赖
DEPS="lyaml tcping"
for dep in $DEPS; do
    echo "尝试安装 $dep..."
    opkg install $dep 2>/dev/null || echo "$dep 需要从 Passwall 源安装"
done

# 4. 添加 Passwall 源（如果依赖安装失败）
echo ""
echo "[步骤 4/5] 配置 Passwall 软件源..."

# 备份原配置
cp /etc/opkg/customfeeds.conf /etc/opkg/customfeeds.conf.bak 2>/dev/null

# 添加 Passwall 源
cat >> /etc/opkg/customfeeds.conf << EOF

# Passwall2 依赖源
src/gz passwall_packages https://github.com/xiaorouji/openwrt-passwall-packages/releases/download/latest/${ARCH}
src/gz passwall2_luci https://github.com/Openwrt-Passwall/openwrt-passwall2/releases/latest/download/
EOF

echo "已添加 Passwall 源，重新更新..."
opkg update

# 再次尝试安装缺失的依赖
echo "再次尝试安装依赖..."
opkg install lyaml tcping geoview v2ray-geoip v2ray-geosite 2>/dev/null

# 5. 安装主程序和语言包
echo ""
echo "[步骤 5/5] 安装 Passwall2..."

# 检查当前目录是否有 ipk 文件
if [ -f "luci-app-passwall2_26.6.3-r1_all.ipk" ]; then
    echo "发现本地安装包，开始安装..."
    opkg install luci-app-passwall2_26.6.3-r1_all.ipk
    
    if [ -f "luci-i18n-passwall2-zh-cn_26.6.3_all.ipk" ]; then
        opkg install luci-i18n-passwall2-zh-cn_26.6.3_all.ipk
    fi
else
    echo "错误：未找到 luci-app-passwall2_26.6.3-r1_all.ipk"
    echo "请将 ipk 文件放在同一目录下"
    exit 1
fi

echo ""
echo "================================"
echo "安装完成！"
echo "================================"
echo ""
echo "请执行以下操作："
echo "1. 重启 LuCI: /etc/init.d/uhttpd restart"
echo "2. 在浏览器中访问 OpenWrt 管理界面"
echo "3. 在 服务 -> PassWall2 中配置"
echo ""
