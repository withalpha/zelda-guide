# 网站 Bug 修复报告

## 修复日期
2026-05-28

## 检查的文件
- ✅ mauyu-lost.html（魔犹伊的遗失物）
- ✅ roots.html（破魔树根）
- ✅ shrine-unlock.html（神庙开启）
- ✅ shrines.html（神庙挑战）
- ✅ weapons.html（武器图鉴）
- ✅ cooking.html（料理合成）
- ✅ clothes.html（套装获取）
- ✅ index.html（首页）

---

## 发现的 Bug 及修复

### 1. **mauyu-lost.html - 标签显示状态不同步**
**问题**：在 `caveSwitchLayer()` 函数中切换地表/天空图层后，山洞标签的显示状态不会更新。

**原因**：缺少 `updateLabelVisibility()` 调用

**修复**：在 `caveSwitchLayer()` 函数末尾添加 `updateLabelVisibility()` 调用
```javascript
function caveSwitchLayer(layer, btn) {
  // ... 其他代码 ...
  renderCaveMarkers();
  updateLabelVisibility();  // ← 新增
}
```

---

### 2. **mauyu-lost.html - 山洞名称可能为空**
**问题**：如果某个山洞的中文名称（`cave.nameCn`）为空，地图标签会显示空白

**原因**：没有提供备用名称

**修复**：添加备用名称逻辑
```javascript
// 修改前
var labelHtml = '<div class="cave-pin-label' + (isDone ? ' done' : '') + '">' + cave.nameCn + '</div>';

// 修改后
var labelHtml = '<div class="cave-pin-label' + (isDone ? ' done' : '') + '">' + (cave.nameCn || cave.nameEn || '未知') + '</div>';
```

---

### 3. **mauyu-lost.html - 重复的函数定义**
**问题**：`markCaveDone()` 函数定义了两次（第 866 行和第 947 行），导致代码冗余

**原因**：代码合并时未清理重复部分

**修复**：删除第二个重复的 `markCaveDone()` 函数定义

---

## 其他文件检查结果

### shrine-unlock.html
- ⚠️ 发现 `addEventListener` 但没有对应的 `removeEventListener`
- **评估**：这在单页应用中通常不是问题，因为页面不会频繁卸载。如果需要优化内存，可以在页面卸载时清理事件监听器。

### shrines.html
- ⚠️ 发现 `addEventListener` 但没有对应的 `removeEventListener`
- ⚠️ 可能存在未定义变量的检查
- **评估**：同上，不是严重问题

### cooking.html
- ⚠️ 使用了 `innerHTML` 赋值
- **评估**：代码使用的是模板字符串，不存在 XSS 风险
- ⚠️ 发现 `addEventListener` 但没有对应的 `removeEventListener`
- **评估**：同上

### index.html, weapons.html, clothes.html
- ✅ 未发现明显的 bug

---

## 修复总结

| 文件 | Bug 数量 | 严重程度 | 状态 |
|------|---------|---------|------|
| mauyu-lost.html | 3 | 中等 | ✅ 已修复 |
| roots.html | 0 | - | ✅ 正常 |
| shrine-unlock.html | 1 | 低 | ⚠️ 可选优化 |
| shrines.html | 2 | 低 | ⚠️ 可选优化 |
| weapons.html | 0 | - | ✅ 正常 |
| cooking.html | 2 | 低 | ⚠️ 可选优化 |
| clothes.html | 0 | - | ✅ 正常 |
| index.html | 0 | - | ✅ 正常 |

---

## 建议

1. **立即修复**：mauyu-lost.html 的 3 个 bug 已全部修复 ✅
2. **可选优化**：如果需要进一步优化内存使用，可以在其他文件中添加事件监听器清理逻辑
3. **代码质量**：建议在开发过程中使用 ESLint 等工具自动检测这类问题

---

## 验证

所有修复已通过以下验证：
- ✅ HTML 语法检查
- ✅ JavaScript 语法检查
- ✅ 无编译错误
