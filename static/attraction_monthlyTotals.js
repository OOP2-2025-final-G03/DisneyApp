// Chart.js のインスタンスを保持（再描画時に destroy するため）
let top3Chart = null;

// APIの全データ（全月分）を保持
let cachedData = null;

function top3WithTiesByMonth(data, ym /* "YYYY-MM" */) {
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

    // 3) total降順にソート
    const arr = [...totals.values()].sort((a, b) => b.total - a.total);

    // 3件以下ならそのまま
    if (arr.length <= 3) return arr;

    // 3位の回数（同点は全部表示）
    const thirdTotal = arr[2].total;
    return arr.filter((x) => x.total >= thirdTotal);
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

    // 上位3（同点は全部表示）
    const top = top3WithTiesByMonth(cachedData, ym);

    // ---- ランキング表（#top3Table）に表示 ----
    const tbody = document.querySelector("#top3Table tbody");
    if (!tbody) {
        console.error("table #top3Table が見つかりません");
        return;
    }

    tbody.innerHTML = "";

    if (top.length === 0) {
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

    top.forEach((x, i) => {
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

    const labels = top.map((x) => x.attraction_name);
    const values = top.map((x) => Number(x.total) || 0);

    // すでに描画済みなら破棄（ホットリロード対策）
    if (top3Chart) top3Chart.destroy();

    top3Chart = new Chart(canvas, {
        type: "bar",
        data: {
            labels,
            datasets: [
                {
                    label: `${ym} 上位（回数）`,
                    data: values,
                    // 棒の太さを固定（1本でも太くなりすぎない）
                    barThickness: 80,
                    maxBarThickness: 100,
                },
            ],
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    // 縦軸の「回数（数字）」を表示しない
                    ticks: {
                        display: false,
                    },
                    // 目盛りのチョンチョンも消したいなら（任意）
                    grid: {
                        drawTicks: false,
                    },
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
