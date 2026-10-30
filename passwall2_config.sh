#!/bin/bash
# OpenWrt Passwall2 自动配置脚本
# 用于配置3x-ui Vless节点

set -e

echo "========================================="
echo "OpenWrt Passwall2 节点配置脚本"
echo "========================================="

# 配置变量
SERVER_IP="3.112.21.197"
SERVER_PORT="443"
USER_UUID="7199492d-996c-4488-bf79-0e75491a1a53"
ENCRYPTION="none"
STREAM_TYPE="stream-one"
TLS_TYPE="reality"
SNI="www.amd.com"
FINGERPRINT="firefox"
PUBLIC_KEY="r5t(W)jTUN8HOpnQXn79t8c_DUewMfTu5X_TC6BKG5"
SHORT_ID="/1wwa2b2d/d6"
SOLDIER_X="/I00zrddA0VCqbq"

echo "Step 1: 检查并安装依赖包..."

# SSH连接到路由器后执行
# 如果在路由器上直接运行，取消注释下面这行
# opkg update

# 检查Passwall2是否已安装
if ! opkg list-installed | grep -q "passwall2"; then
    echo "正在安装 passwall2..."
    opkg install luci-app-passwall2 libcares libustream-wolfssl
else
    echo "✓ Passwall2 已安装"
fi

echo ""
echo "Step 2: 配置UCI设置..."

# 配置Passwall2节点
uci -q delete passwall2.@servers[0] 2>/dev/null || true

# 添加新节点
uci set passwall2.@servers[0]=servers
uci set passwall2.@servers[0].remarks="Tokyo-3xUI"
uci set passwall2.@servers[0].type="Vless"
uci set passwall2.@servers[0].address="${SERVER_IP}"
uci set passwall2.@servers[0].port="${SERVER_PORT}"
uci set passwall2.@servers[0].uuid="${USER_UUID}"
uci set passwall2.@servers[0].encryption="${ENCRYPTION}"
uci set passwall2.@servers[0].flow="${STREAM_TYPE}"
uci set passwall2.@servers[0].tls="${TLS_TYPE}"
uci set passwall2.@servers[0].tls_host="${SNI}"
uci set passwall2.@servers[0].reality_fingerprint="${FINGERPRINT}"
uci set passwall2.@servers[0].reality_pubkey="${PUBLIC_KEY}"
uci set passwall2.@servers[0].reality_shortid="${SHORT_ID}"
uci set passwall2.@servers[0].reality_spiderx="${SOLDIER_X}"

echo "✓ 节点配置完成"

echo ""
echo "Step 3: 配置分流规则..."

# 启用分流
uci set passwall2.@global[0]=global
uci set passwall2.@global[0].enabled="1"
uci set passwall2.@global[0].tcp_node="0"
uci set passwall2.@global[0].udp_node="0"
uci set passwall2.@global[0].dns_forward="1"
uci set passwall2.@global[0].proxy_mode="chn"

echo "✓ 分流规则配置完成"

echo ""
echo "Step 4: 提交配置..."

uci commit passwall2
/etc/init.d/passwall2 restart

echo ""
echo "========================================="
echo "✓ 配置完成！"
echo "========================================="
echo ""
echo "配置信息："
echo "  服务器: ${SERVER_IP}:${SERVER_PORT}"
echo "  节点类型: Vless"
echo "  TLS: ${TLS_TYPE}"
echo "  代理模式: 分流模式 (国内走原路由，国外走代理)"
echo ""
echo "后续操作："
echo "1. 登录路由器WebUI: http://192.168.1.1"
echo "2. 进入 服务 → Passwall → 基本设置"
echo "3. 启用Passwall2服务"
echo "4. 如需调整，进入 分流设置 配置规则"
echo ""
echo "查看日志: logread -f | grep passwall"
