// 完全版: DOMContentLoaded で /api/stats を取得し、表示と Chart.js のグラフを作成する

document.addEventListener('DOMContentLoaded', () => {
  const ids = {
    users: 'user-count',
    attractions: 'attraction-count',
    areas: 'area-count'
  };
  const canvas = document.getElementById('statsChart');
  if (canvas) {
    canvas.style.maxWidth = '1000px';   // 最大幅
    canvas.style.width = 'auto';        // レスポンシブに幅を伸縮
    canvas.style.maxHeight = '400px';  // 最大高さ
    canvas.style.height = 'auto';
  }
  const ctx = canvas ? canvas.getContext('2d') : null;

  async function fetchStats() {
    const res = await fetch('/api/stats', {cache: 'no-store'});
    if (!res.ok) throw new Error(`network error: ${res.status}`);
    return await res.json();
  }

  function createChart(data) {
    if (!ctx || typeof Chart === 'undefined') return;
    const labels = ['ユーザー', 'アトラクション', 'エリア'];
    const values = [data.users || 0, data.attractions || 0, data.areas || 0];
    const colors = [
      'rgba(54, 162, 235, 0.8)',   // 青
      'rgba(255, 159, 64, 0.8)',   // オレンジ
      'rgba(75, 192, 192, 0.8)'    // 緑
    ];
    if (window.__statsChartInstance) {
      try { window.__statsChartInstance.destroy(); } catch (e) {}
    }

    window.__statsChartInstance = new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          label: '総数',
          data: values,
          backgroundColor: colors,
          borderColor: colors.map(c => c.replace(/0\.8/, '1')),
          borderWidth: 1
        }]
      },
      options: {
        // ここを追加するとバーが横向き（水平）になります
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: true,
        aspectRatio: 2,
        scales: { x: { beginAtZero: true, ticks: { precision: 0 } } },
        plugins: { legend: { display: false } }
      }
    });
  }

  fetchStats()
    .then(data => {
      try {
        document.getElementById(ids.users).innerText = String(data.users ?? 0);
        document.getElementById(ids.attractions).innerText = String(data.attractions ?? 0);
        document.getElementById(ids.areas).innerText = String(data.areas ?? 0);
      } catch (e) {}
      createChart(data);
    })
    .catch(err => {
      console.error('stats fetch error:', err);
      try {
        document.getElementById(ids.users).innerText = '0';
        document.getElementById(ids.attractions).innerText = '0';
        document.getElementById(ids.areas).innerText = '0';
      } catch (e) {}
    });
});