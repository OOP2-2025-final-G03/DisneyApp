// Chart.js のインスタンスを保持（再描画時に destroy するため）
let top3Chart = null;

// APIの全データ（全月分）を保持
let cachedData = null;

function top3ByMonth(data, ym /* "YYYY-MM" */) {
    // 1) 月で絞る
    const filtered = data.filter((r) => r.month === ym);

    // 2) attraction_id ごとに合算（保険）
    const totals = new Map(); // key: id, value: {attraction_id, attraction_name, total}
    for (const r of filtered) {
        const id = r.attraction_id;
        const prev =
            totals.get(id) ?? {
                attraction_id: id,
                attraction_name: r.attraction_name,
                total: 0,
            };
        prev.total += Number(r.total) || 0;
        totals.set(id, prev);
    }

    // 3) total降順にして上位3つ
    return [...totals.values()].sort((a, b) => b.total - a.total).slice(0, 3);
}

function setRankingTitle(ym) {
    const title = document.getElementById("rankingTitle");
    if (!title) return;

    const now = new Date();
    const nowYm = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}`;

    // 今月なら「今月の～」
    if (ym === nowYm) {
        title.textContent = "今月の人気アトラクションランキング";
        return;
    }

    // ym = "YYYY-MM" の月だけ表示
    const parts = ym.split("-");
    const month = parts.length >= 2 ? Number(parts[1]) : NaN;

    if (!Number.isNaN(month)) {
        title.textContent = `${month}月の人気アトラクションランキング`;
    } else {
        title.textContent = "人気アトラクションランキング";
    }
}

function renderRanking(ym) {
    if (!cachedData) return;

    // タイトル更新
    setRankingTitle(ym);

    const top3 = top3ByMonth(cachedData, ym);

    // ---- ランキング表（#top3Table）に表示 ----
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

        // グラフも消す
        if (top3Chart) {
            top3Chart.destroy();
            top3Chart = null;
        }
        return;
    }

    top3.forEach((x, i) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${i + 1}</td>
            <td>${x.attraction_name}</td>
            <td>${x.total}</td>
        `;
        tbody.appendChild(tr);
    });

    // ---- 棒グラフ（Chart.js）に表示 ----
    const canvas = document.getElementById("top3Chart");
    if (!canvas) {
        console.error("canvas #top3Chart が見つかりません");
        return;
    }

    const labels = top3.map((x) => x.attraction_name);
    const values = top3.map((x) => Number(x.total) || 0);

    // すでに描画済みなら破棄（ホットリロード対策）
    if (top3Chart) top3Chart.destroy();

    top3Chart = new Chart(canvas, {
        type: "bar",
        data: {
            labels,
            datasets: [
                {
                    label: `${ym} 上位3（回数）`,
                    data: values,
                },
            ],
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { precision: 0 }, // 整数表示
                },
            },
        },
    });
}

async function load() {
    const res = await fetch("/historys/api/attraction_monthly_totals");

    if (!res.ok) {
        const text = await res.text();
        console.error("API error:", res.status, text);
        return;
    }

    cachedData = await res.json();

    // 初期値：今月を monthPicker に入れる
    const now = new Date();
    const defaultYm = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}`;

    const monthPicker = document.getElementById("monthPicker");
    if (monthPicker) monthPicker.value = defaultYm;

    // 初回描画（タイトルは setRankingTitle 内で「今月の～」になる）
    renderRanking(defaultYm);

    // ボタンで再表示
    const btn = document.getElementById("applyMonth");
    if (btn && monthPicker) {
        btn.addEventListener("click", () => {
            const ym = monthPicker.value; // "YYYY-MM"
            if (!ym) return;
            renderRanking(ym);
        });

        // Enterキーでも更新（任意）
        monthPicker.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                const ym = monthPicker.value;
                if (!ym) return;
                renderRanking(ym);
            }
        });
    }
}

load().catch(console.error);
