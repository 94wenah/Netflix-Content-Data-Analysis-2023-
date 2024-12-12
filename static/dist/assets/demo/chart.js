document.addEventListener('DOMContentLoaded', function () {
    fetch('/chart-data')
        .then(response => response.json())
        .then(data => {
            // 確保數據縮放為 Billion 單位
            data.values = data.values.map(value => value / 1e9); // 將數據轉換為 Billion

            const ctx = document.getElementById('contentTypeChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: '', // 清空圖例標籤
                        data: data.values,
                        backgroundColor: ['#343A40','#E50914'], // 顏色配置
                      
                        borderWidth: 1
                    }]
                },
                options: {
                    plugins: {
                        legend: {
                            display: false // 隱藏圖例
                        }
                    },
                    maintainAspectRatio: false,
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            min: 0,
                            max: 120, // 最大值根據數據調整
                            ticks: {
                                stepSize: 20,
                                callback: function(value) {
                                    return value + 'B'; // 添加單位 'B'
                                }
                            },
                            title: {
                                display: true,
                                text: 'Total Hours Viewed' // Y 軸標籤
                            },                            grid: {
                                drawOnChartArea: false
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Content Type' // X 軸標籤
                            },
                            grid: {
                                drawOnChartArea: false
                            }
                        }

                    }
                }
            });
        })
        .catch(error => console.error('Error:', error));
});
