// dashboard.js - 月別新規ユーザー数の棒グラフを描画

document.addEventListener('DOMContentLoaded', function() {
    const chartCanvas = document.getElementById('newUsersChart');
    
    if (!chartCanvas) {
        console.warn('グラフコンテナが見つかりません');
        return;
    }

    // data属性からデータを取得
    const months = JSON.parse(chartCanvas.getAttribute('data-labels') || '[]');
    const counts = JSON.parse(chartCanvas.getAttribute('data-counts') || '[]');

    // Chart.jsで棒グラフを作成
    new Chart(chartCanvas, {
        type: 'bar',
        data: {
            labels: months,
            datasets: [{
                label: '新規ユーザー数',
                data: counts,
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            }
        }
    });
});
