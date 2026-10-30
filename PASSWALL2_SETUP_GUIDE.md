# OpenWrt Passwall2 完整配置指南

## 前置准备

### 1. 连接到路由器

**方式A：通过Web界面（推荐新手）**
```
打开浏览器访问：http://192.168.1.1
输入用户名和密码（默认都是admin）
```

**方式B：通过SSH（推荐高级用户）**
```bash
ssh root@192.168.1.1
# 如果设置了SSH密钥，加上 -i 参数
```

---

## 配置步骤

### 步骤1：安装Passwall2及依赖

#### 通过Web界面安装：
1. 登录 http://192.168.1.1
2. 进入 **系统 → 软件包**
3. 点击 **更新列表**（等待完成）
4. 搜索并依次安装：
   - `luci-app-passwall2`
   - `libcares`
   - `libustream-wolfssl`
5. 安装后刷新页面

#### 通过SSH安装：
```bash
ssh root@192.168.1.1
opkg update
opkg install luci-app-passwall2 libcares libustream-wolfssl
```

---

### 步骤2：添加节点（手动方式）

1. 登录 http://192.168.1.1
2. 进入 **服务 → Passwall**
3. 点击左侧 **节点列表**
4. 点击 **添加**，选择 **Vless**

#### 填写以下信息：

**基础信息：**
| 字段 | 值 |
|------|-----|
| 备注 | Tokyo-3xUI |
| 地址 | 3.112.21.197 |
| 端口 | 443 |

**Vless配置：**
| 字段 | 值 |
|------|-----|
| UUID | 7199492d-996c-4488-bf79-0e75491a1a53 |
| 加密 | none |
| 流类型 | stream-one |

**TLS配置：**
| 字段 | 值 |
|------|-----|
| TLS | reality |
| TLS Host | www.amd.com |

**Reality配置：**
| 字段 | 值 |
|------|-----|
| Fingerprint | firefox |
| PublicKey | r5t(W)jTUN8HOpnQXn79t8c_DUewMfTu5X_TC6BKG5 |
| ShortId | /1wwa2b2d/d6 |
| SpiderX | /I00zrddA0VCqbq |

5. 点击 **保存**

---

### 步骤3：配置分流规则

1. 进入 **服务 → Passwall → 基本设置**
2. **启用Passwall**：勾选 ☑

3. **主要设置：**
   - TCP节点：选择 `Tokyo-3xUI`
   - UDP节点：选择 `Tokyo-3xUI`
   - 代理模式：选择 `代理大陆以外的IP`
   - 启用UDP：☑ 勾选
   - 启用DNS代理：☑ 勾选

4. 点击 **保存&应用**

---

### 步骤4：验证配置

#### 方式A：通过Web界面查看日志
1. 进入 **系统 → 系统日志**
2. 搜索 `passwall` 关键字
3. 查看是否有错误信息

#### 方式B：通过SSH查看实时日志
```bash
ssh root@192.168.1.1
tail -f /var/log/messages | grep -i passwall
```

#### 方式C：测试代理连通性
```bash
# 在路由器上测试
curl -x socks5://127.0.0.1:1080 https://www.google.com

# 如果显示 HTML 内容，说明成功！
```

---

## 使用自动化脚本（可选）

如果手动配置有问题，可以使用提供的脚本自动配置：

### SSH方式运行脚本：
```bash
# 1. 上传脚本到路由器
scp passwall2_config.sh root@192.168.1.1:/tmp/

# 2. SSH连接并运行
ssh root@192.168.1.1
chmod +x /tmp/passwall2_config.sh
/tmp/passwall2_config.sh
```

### 或者直接在路由器上粘贴命令：
```bash
# SSH连接后直接粘贴以下命令
cat > /tmp/config.sh << 'EOF'
uci set passwall2.@servers[0]=servers
uci set passwall2.@servers[0].remarks="Tokyo-3xUI"
uci set passwall2.@servers[0].type="Vless"
uci set passwall2.@servers[0].address="3.112.21.197"
uci set passwall2.@servers[0].port="443"
uci set passwall2.@servers[0].uuid="7199492d-996c-4488-bf79-0e75491a1a53"
uci set passwall2.@servers[0].encryption="none"
uci set passwall2.@servers[0].flow="stream-one"
uci set passwall2.@servers[0].tls="reality"
uci set passwall2.@servers[0].tls_host="www.amd.com"
uci set passwall2.@servers[0].reality_fingerprint="firefox"
uci set passwall2.@servers[0].reality_pubkey="r5t(W)jTUN8HOpnQXn79t8c_DUewMfTu5X_TC6BKG5"
uci set passwall2.@servers[0].reality_shortid="/1wwa2b2d/d6"
uci set passwall2.@servers[0].reality_spiderx="/I00zrddA0VCqbq"
uci commit passwall2
/etc/init.d/passwall2 restart
EOF

chmod +x /tmp/config.sh
/tmp/config.sh
```

---

## 常见问题排查

### ❌ 无法连接代理

**症状：** 连接超时或无响应

**解决步骤：**
```bash
# 1. 检查节点是否在线
ping 3.112.21.197

# 2. 检查防火墙规则
ufw status
# 或
iptables -L -n | grep 443

# 3. 重启Passwall服务
/etc/init.d/passwall2 restart

# 4. 检查日志
logread | tail -20
```

### ❌ 分流不生效（所有流量都走代理）

**症状：** 国内网站也很慢

**解决方案：**
```bash
# 1. 检查代理模式设置
uci get passwall2.@global[0].proxy_mode

# 应该是 "chn" 或 "gfw"，不应该是 "global"

# 2. 如果不对，改为分流模式
uci set passwall2.@global[0].proxy_mode="chn"
uci commit passwall2
/etc/init.d/passwall2 restart
```

### ❌ DNS污染导致某些网站无法访问

**解决方案：**
```bash
# 启用DNS代理和防污染
uci set passwall2.@global[0].dns_forward="1"
uci set passwall2.@global[0].enable_rules="1"
uci commit passwall2
/etc/init.d/passwall2 restart
```

### ⚠️ 某些APP连接不上（如Netflix、YouTube）

**解决方案：**
- 检查是否启用了UDP：`uci get passwall2.@global[0].udp_node`
- 应该返回你的节点名称，如果为空就是禁用了

```bash
uci set passwall2.@global[0].udp_node="Tokyo-3xUI"
uci commit passwall2
/etc/init.d/passwall2 restart
```

---

## 高级配置

### 自定义分流规则

编辑分流文件：
```bash
vi /etc/passwall2/rules/chn_ip.txt
```

添加需要走代理的IP段或域名。

### 设置开机自启
```bash
/etc/init.d/passwall2 enable
```

### 禁用Passwall
```bash
/etc/init.d/passwall2 disable
```

---

## 性能优化建议

1. **启用硬件NAT加速（如果支持）**
   ```bash
   uci set network.@device[0].hwnat="1"
   uci commit network
   ```

2. **调整UDP缓冲**
   ```bash
   echo "net.core.rmem_max=134217728" >> /etc/sysctl.conf
   sysctl -p
   ```

3. **定期清理缓存**
   ```bash
   /etc/init.d/passwall2 restart
   ```

---

## 备份配置

```bash
# 备份Passwall配置
scp root@192.168.1.1:/etc/config/passwall2 ./passwall2_backup

# 恢复配置
scp ./passwall2_backup root@192.168.1.1:/etc/config/passwall2
ssh root@192.168.1.1 "/etc/init.d/passwall2 restart"
```

---

## 需要帮助？

如遇问题，请收集以下信息：
1. 错误日志：`logread | tail -50`
2. Passwall配置：`uci show passwall2`
3. 网络状态：`ifconfig` 和 `route -n`
4. 防火墙规则：`iptables -L -n`

然后提供给我分析。
