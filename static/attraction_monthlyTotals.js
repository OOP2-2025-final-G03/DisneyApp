async function load() {
  const res = await fetch("/historys/api/attraction_monthly_totals");

  if (!res.ok) {
    const text = await res.text();
    console.error("API error:", res.status, text);
    return;
  }

  const data = await res.json();

  // 今月(YYYY-MM)
  const now = new Date();
  const ym = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}`;

  // 上位3
  const top3 = top3ByMonth(data, ym);

  // ランキング表に表示
  const tbody = document.querySelector("#top3Table tbody");
  if (!tbody) {
    console.error("table #top3Table が見つかりません");
    return;
  }

  tbody.innerHTML = "";

  if (top3.length === 0) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td colspan="3">${ym} の履歴データがありません</td>`;
    tbody.appendChild(tr);
    return;
  }

  top3.forEach((x, i) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${i + 1}</td>
      <td>${x.attraction_name}（id=${x.attraction_id}）</td>
      <td>${x.total}</td>
    `;
    tbody.appendChild(tr);
  });

  // もし「全件の月別表」が不要なら、ここにあった monthlyTotals 描画は消してOK
}

function top3ByMonth(data, ym /* "YYYY-MM" */) {
  const filtered = data.filter(r => r.month === ym);

  const totals = new Map();
  for (const r of filtered) {
    const id = r.attraction_id;
    const prev = totals.get(id) ?? {
      attraction_id: id,
      attraction_name: r.attraction_name,
      total: 0
    };
    prev.total += Number(r.total) || 0;
    totals.set(id, prev);
  }

  return [...totals.values()]
    .sort((a, b) => b.total - a.total)
    .slice(0, 3);
}

load().catch(console.error);