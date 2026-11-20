/* collect.js — 收集记录导出 CSV（UTF-8 + BOM，Excel 直接打开不乱码）
   用法：exportToCSV(文件名, 列名数组, 每行值的数组) */
function exportToCSV(filename, headers, rows) {
  function esc(v) {
    if (v === null || v === undefined) return '';
    var s = String(v);
    if (/[",\n\r]/.test(s)) return '"' + s.replace(/"/g, '""') + '"';
    return s;
  }
  var lines = [];
  lines.push(headers.map(esc).join(','));
  for (var i = 0; i < rows.length; i++) {
    lines.push(rows[i].map(esc).join(','));
  }
  var blob = new Blob(['\ufeff' + lines.join('\r\n')], { type: 'text/csv;charset=utf-8;' });
  var a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  setTimeout(function() { URL.revokeObjectURL(a.href); }, 1000);
}
