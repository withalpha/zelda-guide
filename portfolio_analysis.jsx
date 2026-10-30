import { useState } from "react";

const positions = [
  { symbol: "QQQM", name: "纳斯达克100 ETF", value: 1495.62, currency: "USD", type: "科技股ETF", region: "美国", pnlPct: 36.9, risk: "高" },
  { symbol: "SPYM", name: "标普500 2x杠杆ETF", value: 1057.56, currency: "USD", type: "杠杆ETF", region: "美国", pnlPct: 18.0, risk: "极高" },
  { symbol: "005930", name: "三星电子", value: 1261.49, currency: "USD", type: "个股", region: "韩国", pnlPct: 10.8, risk: "高" },
  { symbol: "GOOG", name: "谷歌", value: 1131.79, currency: "USD", type: "个股", region: "美国", pnlPct: 54.4, risk: "中高" },
  { symbol: "NVDA", name: "英伟达", value: 1062.70, currency: "USD", type: "个股", region: "美国", pnlPct: 26.1, risk: "高" },
  { symbol: "META", name: "Meta", value: 632.17, currency: "USD", type: "个股", region: "美国", pnlPct: 2.5, risk: "中高" },
  { symbol: "MSFT", name: "微软", value: 995.87, currency: "USD", type: "个股", region: "美国", pnlPct: -0.4, risk: "中" },
  { symbol: "EWY", name: "韩国ETF", value: 824.00, currency: "USD", type: "ETF", region: "韩国", pnlPct: 10.8, risk: "高" },
  { symbol: "IAUM", name: "黄金ETF", value: 416.47, currency: "USD", type: "商品ETF", region: "全球", pnlPct: 15.2, risk: "低" },
  { symbol: "SCHD", name: "股息ETF", value: 472.95, currency: "USD", type: "股息ETF", region: "美国", pnlPct: 5.3, risk: "低中" },
  { symbol: "BND", name: "债券ETF", value: 497.62, currency: "USD", type: "债券ETF", region: "美国", pnlPct: -0.5, risk: "低" },
];

const totalValue = 9848.25;

const typeColors = {
  "科技股ETF": "#6366f1",
  "杠杆ETF": "#ef4444",
  "个股": "#f59e0b",
  "ETF": "#3b82f6",
  "商品ETF": "#f97316",
  "股息ETF": "#10b981",
  "债券ETF": "#14b8a6",
};

const riskColors = {
  "极高": "#ef4444",
  "高": "#f97316",
  "中高": "#f59e0b",
  "中": "#3b82f6",
  "低中": "#10b981",
  "低": "#14b8a6",
};

// Current allocation by category
const currentAlloc = [
  { label: "科技个股", pct: 38.3, color: "#f59e0b", items: "GOOG+NVDA+META+MSFT" },
  { label: "纳指/科技ETF", pct: 15.2, color: "#6366f1", items: "QQQM" },
  { label: "杠杆ETF", pct: 10.7, color: "#ef4444", items: "SPYM" },
  { label: "韩国资产", pct: 21.2, color: "#ec4899", items: "005930+EWY" },
  { label: "防御资产", pct: 14.2, color: "#10b981", items: "BND+SCHD+IAUM" },
];

// Recommended allocation
const recommendedAlloc = [
  { label: "宽基ETF (SPY/QQQ)", pct: 35, color: "#6366f1", detail: "核心压舱石，降低个股集中风险" },
  { label: "科技个股", pct: 20, color: "#f59e0b", detail: "保留GOOG/MSFT，减少单一持仓" },
  { label: "防御资产", pct: 20, color: "#10b981", detail: "BND+SCHD+黄金，缓冲下行" },
  { label: "韩国/新兴市场", pct: 10, color: "#ec4899", detail: "保持一定国际分散" },
  { label: "高增长个股", pct: 10, color: "#a855f7", detail: "NVDA等，控制仓位" },
  { label: "现金/类现金", pct: 5, color: "#64748b", detail: "应对机会，降低组合波动" },
];

function DonutChart({ data, size = 160 }) {
  const cx = size / 2, cy = size / 2, r = size * 0.38, inner = size * 0.24;
  let cumAngle = -Math.PI / 2;
  const slices = data.map((d) => {
    const angle = (d.pct / 100) * 2 * Math.PI;
    const x1 = cx + r * Math.cos(cumAngle);
    const y1 = cy + r * Math.sin(cumAngle);
    cumAngle += angle;
    const x2 = cx + r * Math.cos(cumAngle);
    const y2 = cy + r * Math.sin(cumAngle);
    const ix1 = cx + inner * Math.cos(cumAngle - angle);
    const iy1 = cy + inner * Math.sin(cumAngle - angle);
    const ix2 = cx + inner * Math.cos(cumAngle);
    const iy2 = cy + inner * Math.sin(cumAngle);
    const largeArc = angle > Math.PI ? 1 : 0;
    const path = `M ${ix1} ${iy1} L ${x1} ${y1} A ${r} ${r} 0 ${largeArc} 1 ${x2} ${y2} L ${ix2} ${iy2} A ${inner} ${inner} 0 ${largeArc} 0 ${ix1} ${iy1} Z`;
    return { ...d, path };
  });

  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      {slices.map((s, i) => (
        <path key={i} d={s.path} fill={s.color} stroke="#0f172a" strokeWidth="1.5" opacity="0.92" />
      ))}
    </svg>
  );
}

function BarRow({ label, pct, color, detail, current = false }) {
  return (
    <div style={{ marginBottom: 10 }}>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 3 }}>
        <span style={{ fontSize: 12, color: "#cbd5e1", fontFamily: "monospace" }}>{label}</span>
        <span style={{ fontSize: 13, fontWeight: 700, color: color }}>{pct}%</span>
      </div>
      <div style={{ background: "#1e293b", borderRadius: 4, height: 7, overflow: "hidden" }}>
        <div style={{ width: `${pct}%`, height: "100%", background: color, borderRadius: 4, transition: "width 0.8s ease" }} />
      </div>
      {detail && <div style={{ fontSize: 11, color: "#64748b", marginTop: 3 }}>{detail}</div>}
    </div>
  );
}

export default function App() {
  const [tab, setTab] = useState("overview");

  const issues = [
    { icon: "⚠️", level: "danger", title: "杠杆ETF风险过高", desc: "SPYM 为标普500两倍杠杆，占仓10.7%。在市场下跌20%时将亏损约40%，建议替换为普通SPY/VOO。" },
    { icon: "🔴", level: "danger", title: "科技集中度过高", desc: "GOOG+NVDA+META+MSFT+QQQM合计超过53%，科技板块系统性下跌时回撤会非常显著。" },
    { icon: "🟡", level: "warn", title: "韩国资产集中", desc: "三星+EWY占约21%，单一国家风险较高，且韩元汇率波动会带来额外损失。" },
    { icon: "🟡", level: "warn", title: "防御仓位不足", desc: "BND+SCHD+IAUM合计仅14%，对抗市场下行的缓冲能力有限。建议提升至25-30%。" },
    { icon: "🟢", level: "ok", title: "已有初步分散", desc: "持有黄金(IAUM)、债券(BND)和股息(SCHD)，方向正确，需要加大比例。" },
  ];

  const actions = [
    { step: "1", action: "卖出 SPYM", detail: "替换为 SPYL(1x SPY)或直接买入VOO/SPY，消除杠杆风险", priority: "紧急" },
    { step: "2", action: "减持 NVDA/META", detail: "两者均有不错盈利，可获利了结部分，将集中度降至可控水平", priority: "较高" },
    { step: "3", action: "合并韩国敞口", detail: "三星+EWY存在重叠，建议保留其一或统一用EWY代替，降低单一国家风险", priority: "中等" },
    { step: "4", action: "加仓防御资产", detail: "将BND+SCHD+IAUM合计提升到25%以上，可分批定投", priority: "中等" },
    { step: "5", action: "留存现金缓冲", detail: "目前现金仅$298(约3%)，建议保持5-8%现金以应对机会和波动", priority: "建议" },
  ];

  return (
    <div style={{
      minHeight: "100vh", background: "#0a0f1e",
      fontFamily: "'DM Sans', 'Segoe UI', sans-serif",
      color: "#e2e8f0", padding: "0 0 40px"
    }}>
      {/* Header */}
      <div style={{
        background: "linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%)",
        borderBottom: "1px solid #1e293b",
        padding: "28px 32px 20px"
      }}>
        <div style={{ display: "flex", alignItems: "flex-end", gap: 16, flexWrap: "wrap" }}>
          <div>
            <div style={{ fontSize: 11, letterSpacing: "0.15em", color: "#6366f1", textTransform: "uppercase", marginBottom: 6 }}>
              IBKR Portfolio · 诊断报告
            </div>
            <div style={{ fontSize: 26, fontWeight: 800, letterSpacing: "-0.02em" }}>
              持仓分析 & 配置建议
            </div>
          </div>
          <div style={{ marginLeft: "auto", textAlign: "right" }}>
            <div style={{ fontSize: 11, color: "#64748b", marginBottom: 2 }}>净清算价值</div>
            <div style={{ fontSize: 24, fontWeight: 800, color: "#10b981" }}>$10,149.94</div>
            <div style={{ fontSize: 11, color: "#10b981" }}>未实现盈亏 +$1,466.05 (+16.9%)</div>
          </div>
        </div>

        {/* Tabs */}
        <div style={{ display: "flex", gap: 4, marginTop: 20 }}>
          {["overview", "risks", "recommend"].map((t) => (
            <button key={t} onClick={() => setTab(t)} style={{
              padding: "7px 18px", borderRadius: 8, border: "none", cursor: "pointer",
              background: tab === t ? "#6366f1" : "transparent",
              color: tab === t ? "white" : "#64748b",
              fontWeight: 600, fontSize: 13,
              transition: "all 0.2s"
            }}>
              {{ overview: "📊 持仓概览", risks: "⚠️ 风险诊断", recommend: "💡 调仓建议" }[t]}
            </button>
          ))}
        </div>
      </div>

      <div style={{ padding: "24px 32px", maxWidth: 900, margin: "0 auto" }}>

        {/* OVERVIEW TAB */}
        {tab === "overview" && (
          <div>
            {/* Position table */}
            <div style={{ background: "#0f172a", borderRadius: 12, border: "1px solid #1e293b", overflow: "hidden", marginBottom: 24 }}>
              <div style={{ padding: "16px 20px", borderBottom: "1px solid #1e293b", display: "flex", justifyContent: "space-between" }}>
                <span style={{ fontWeight: 700, fontSize: 15 }}>持仓明细</span>
                <span style={{ fontSize: 12, color: "#64748b" }}>共 {positions.length} 只</span>
              </div>
              <div style={{ overflowX: "auto" }}>
                <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
                  <thead>
                    <tr style={{ background: "#1e293b" }}>
                      {["代码", "名称", "类型", "市值(USD)", "占比", "盈亏%", "风险"].map((h) => (
                        <th key={h} style={{ padding: "10px 16px", textAlign: "left", color: "#64748b", fontWeight: 600, fontSize: 11, whiteSpace: "nowrap" }}>{h}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {positions.sort((a, b) => b.value - a.value).map((p, i) => {
                      const usdValue = p.symbol === "005930" ? (1902000 * 0.0006633) : p.value;
                      const pct = ((usdValue / totalValue) * 100).toFixed(1);
                      return (
                        <tr key={i} style={{ borderBottom: "1px solid #1e293b" }}>
                          <td style={{ padding: "11px 16px", fontWeight: 700, color: "#a5b4fc", fontFamily: "monospace" }}>{p.symbol}</td>
                          <td style={{ padding: "11px 16px", color: "#cbd5e1" }}>{p.name}</td>
                          <td style={{ padding: "11px 16px" }}>
                            <span style={{ background: typeColors[p.type] + "22", color: typeColors[p.type], padding: "2px 8px", borderRadius: 99, fontSize: 11, fontWeight: 600 }}>{p.type}</span>
                          </td>
                          <td style={{ padding: "11px 16px", fontWeight: 600 }}>${usdValue.toFixed(0)}</td>
                          <td style={{ padding: "11px 16px", color: "#94a3b8" }}>{pct}%</td>
                          <td style={{ padding: "11px 16px", color: p.pnlPct >= 0 ? "#10b981" : "#ef4444", fontWeight: 600 }}>
                            {p.pnlPct >= 0 ? "+" : ""}{p.pnlPct}%
                          </td>
                          <td style={{ padding: "11px 16px" }}>
                            <span style={{ background: riskColors[p.risk] + "22", color: riskColors[p.risk], padding: "2px 8px", borderRadius: 99, fontSize: 11, fontWeight: 600 }}>{p.risk}</span>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Allocation donut */}
            <div style={{ background: "#0f172a", borderRadius: 12, border: "1px solid #1e293b", padding: 20 }}>
              <div style={{ fontWeight: 700, fontSize: 15, marginBottom: 16 }}>当前资产分布</div>
              <div style={{ display: "flex", alignItems: "center", gap: 32, flexWrap: "wrap" }}>
                <DonutChart data={currentAlloc} size={180} />
                <div style={{ flex: 1, minWidth: 200 }}>
                  {currentAlloc.map((d, i) => (
                    <div key={i} style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 10 }}>
                      <div style={{ width: 12, height: 12, borderRadius: 3, background: d.color, flexShrink: 0 }} />
                      <span style={{ fontSize: 13, color: "#cbd5e1", flex: 1 }}>{d.label}</span>
                      <span style={{ fontSize: 13, fontWeight: 700, color: d.color }}>{d.pct}%</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* RISKS TAB */}
        {tab === "risks" && (
          <div>
            <div style={{ background: "#0f172a", borderRadius: 12, border: "1px solid #1e293b", padding: 20, marginBottom: 20 }}>
              <div style={{ fontWeight: 700, fontSize: 15, marginBottom: 4 }}>投资者画像匹配</div>
              <div style={{ fontSize: 13, color: "#94a3b8", marginBottom: 16 }}>目标：中等偏进取型 · 控制回撤 · 追求稳健增长</div>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 12 }}>
                {[
                  { label: "当前波动评分", value: "7.8 / 10", color: "#f97316", desc: "偏高" },
                  { label: "科技集中度", value: "53%", color: "#ef4444", desc: "过高" },
                  { label: "防御资产占比", value: "14%", color: "#f59e0b", desc: "不足" },
                ].map((m, i) => (
                  <div key={i} style={{ background: "#1e293b", borderRadius: 10, padding: 16, textAlign: "center" }}>
                    <div style={{ fontSize: 11, color: "#64748b", marginBottom: 4 }}>{m.label}</div>
                    <div style={{ fontSize: 22, fontWeight: 800, color: m.color }}>{m.value}</div>
                    <div style={{ fontSize: 11, color: m.color, marginTop: 2 }}>{m.desc}</div>
                  </div>
                ))}
              </div>
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {issues.map((issue, i) => (
                <div key={i} style={{
                  background: "#0f172a", borderRadius: 12,
                  border: `1px solid ${issue.level === "danger" ? "#ef444433" : issue.level === "warn" ? "#f59e0b33" : "#10b98133"}`,
                  padding: "16px 20px"
                }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 6 }}>
                    <span style={{ fontSize: 18 }}>{issue.icon}</span>
                    <span style={{ fontWeight: 700, fontSize: 14 }}>{issue.title}</span>
                  </div>
                  <div style={{ fontSize: 13, color: "#94a3b8", lineHeight: 1.6 }}>{issue.desc}</div>
                </div>
              ))}
            </div>

            {/* Stress test */}
            <div style={{ background: "#0f172a", borderRadius: 12, border: "1px solid #1e293b", padding: 20, marginTop: 20 }}>
              <div style={{ fontWeight: 700, fontSize: 15, marginBottom: 16 }}>📉 压力测试：市场下跌20%时的估算回撤</div>
              {[
                { label: "当前组合", pct: -32, color: "#ef4444" },
                { label: "调仓后组合", pct: -16, color: "#10b981" },
              ].map((s, i) => (
                <div key={i} style={{ marginBottom: 12 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
                    <span style={{ fontSize: 13, color: "#cbd5e1" }}>{s.label}</span>
                    <span style={{ fontWeight: 700, color: s.color }}>{s.pct}%</span>
                  </div>
                  <div style={{ background: "#1e293b", borderRadius: 4, height: 10, overflow: "hidden" }}>
                    <div style={{ width: `${Math.abs(s.pct) * 3}%`, height: "100%", background: s.color, borderRadius: 4 }} />
                  </div>
                </div>
              ))}
              <div style={{ fontSize: 12, color: "#64748b", marginTop: 8 }}>* 基于当前持仓结构和历史波动率的粗略估算，不构成精确预测。</div>
            </div>
          </div>
        )}

        {/* RECOMMEND TAB */}
        {tab === "recommend" && (
          <div>
            {/* Target allocation */}
            <div style={{ background: "#0f172a", borderRadius: 12, border: "1px solid #1e293b", padding: 20, marginBottom: 20 }}>
              <div style={{ fontWeight: 700, fontSize: 15, marginBottom: 4 }}>🎯 目标资产配置（中等偏进取型）</div>
              <div style={{ fontSize: 13, color: "#94a3b8", marginBottom: 16 }}>设计目标：年化回撤控制在15%以内，同时保留足够的上行空间</div>
              <div style={{ display: "flex", alignItems: "center", gap: 32, flexWrap: "wrap" }}>
                <DonutChart data={recommendedAlloc} size={180} />
                <div style={{ flex: 1, minWidth: 220 }}>
                  {recommendedAlloc.map((d, i) => (
                    <BarRow key={i} label={d.label} pct={d.pct} color={d.color} detail={d.detail} />
                  ))}
                </div>
              </div>
            </div>

            {/* Action steps */}
            <div style={{ background: "#0f172a", borderRadius: 12, border: "1px solid #1e293b", padding: 20, marginBottom: 20 }}>
              <div style={{ fontWeight: 700, fontSize: 15, marginBottom: 16 }}>🛠 分步调仓计划</div>
              {actions.map((a, i) => (
                <div key={i} style={{ display: "flex", gap: 16, marginBottom: 16, alignItems: "flex-start" }}>
                  <div style={{
                    width: 28, height: 28, borderRadius: "50%", background: "#6366f1",
                    display: "flex", alignItems: "center", justifyContent: "center",
                    fontWeight: 800, fontSize: 13, flexShrink: 0
                  }}>{a.step}</div>
                  <div style={{ flex: 1 }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 3 }}>
                      <span style={{ fontWeight: 700, fontSize: 14 }}>{a.action}</span>
                      <span style={{
                        fontSize: 10, fontWeight: 700, padding: "2px 7px", borderRadius: 99,
                        background: a.priority === "紧急" ? "#ef444422" : a.priority === "较高" ? "#f97316" + "22" : "#6366f122",
                        color: a.priority === "紧急" ? "#ef4444" : a.priority === "较高" ? "#f97316" : "#818cf8"
                      }}>{a.priority}</span>
                    </div>
                    <div style={{ fontSize: 13, color: "#94a3b8", lineHeight: 1.5 }}>{a.detail}</div>
                  </div>
                </div>
              ))}
            </div>

            {/* Principles */}
            <div style={{ background: "linear-gradient(135deg, #1e1b4b, #0f172a)", borderRadius: 12, border: "1px solid #312e81", padding: 20 }}>
              <div style={{ fontWeight: 700, fontSize: 15, marginBottom: 14, color: "#a5b4fc" }}>💎 给你的投资原则</div>
              {[
                ["避免杠杆", "杠杆产品在牛市加速盈利，但在震荡市和熊市会让回撤成倍放大，不适合中等风险偏好。"],
                ["宽基优于个股", "个股集中持仓会引入大量非系统性风险，宽基ETF用更低成本实现分散。"],
                ["防御不是保守", "持有20-30%防御资产不会大幅拖累收益，但能让你在市场暴跌时有底气加仓。"],
                ["定期再平衡", "每季度或半年检视一次仓位，将偏离目标配置超过5%的仓位调回来。"],
              ].map(([title, desc], i) => (
                <div key={i} style={{ display: "flex", gap: 12, marginBottom: 14 }}>
                  <div style={{ width: 4, background: "#6366f1", borderRadius: 2, flexShrink: 0 }} />
                  <div>
                    <div style={{ fontWeight: 700, fontSize: 13, color: "#c7d2fe", marginBottom: 3 }}>{title}</div>
                    <div style={{ fontSize: 12, color: "#64748b", lineHeight: 1.6 }}>{desc}</div>
                  </div>
                </div>
              ))}
              <div style={{ fontSize: 11, color: "#475569", borderTop: "1px solid #1e293b", paddingTop: 12, marginTop: 4 }}>
                ⚠️ 以上为参考分析，不构成投资建议。投资有风险，决策需结合自身实际情况。
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
