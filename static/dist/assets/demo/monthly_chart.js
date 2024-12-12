const ctx = document.getElementById("monthlyChart").getContext("2d");

new Chart(ctx, {
    type: "bar",
    data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [
  
            {
                label: "Viewership Hours (in billions)",
                data: [7.2716, 7.1037, 7.4371, 6.8657, 7.0946, 8.522, 6.5248, 6.8178, 7.2622, 8.1232, 7.7495, 10.0558],
                type: "line",
                backgroundColor: "rgba(229, 9, 20, 0.2)",
                borderColor: "#E50914",
                borderWidth: 2,
                pointBackgroundColor: "#E50914",
                pointBorderColor: "#E50914",
                tension: 0.4, // 曲線平滑度
                yAxisID: "y2"
            },          {
                label: "Number of Releases",
                data: [608, 560, 690, 647, 624, 670, 631, 674, 739, 802, 734, 787],
                backgroundColor: "#6C757D",
                borderColor: "#6C757D",
                borderWidth: 1,
                yAxisID: "y1"
            }
        ]
    },
    options: {
        responsive: true,
        scales: {
            y1: {
                type: "linear",
                position: "left",
                title: {
                    display: true,
                    text: "Number of Releases",
                    color: "#737373"
                },
                ticks: {
                    beginAtZero: true,
                    color: "#737373"
                },
                grid: {
                    drawOnChartArea: false // 禁用背景網格線
                }
            },
            y2: {
                type: "linear",
                position: "right",
                title: {
                    display: true,
                    text: "Viewership Hours (in billions)",
                    color: "#737373"
                },
                ticks: {
                    min: 5,  // 最小值
                    max: 10, // 最大值
                    stepSize: 1 ,// 刻度間距
                    callback: function(value) {
                        return value.toFixed(1) + "B"; // 格式化為 "B"
                    },
                    color: "#737373"
                },
                grid: {
                    drawOnChartArea: false // 禁用背景網格線
                }
            },
            x: {
                title: {
                    display: true,
                    text: "Months",
                    color: "#666"
                },
                ticks: {
                    color: "#666"
                },
                grid: {
                    color: "rgba(0, 0, 0, 0.1)"
                }
            }
        },
        plugins: {
            legend: {
                display: true,
                position: "top",
                labels: {
                    color: "#333"
                }
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const datasetLabel = context.dataset.label || '';
                        const value = context.raw;
                        if (context.dataset.yAxisID === 'y2') {
                            return `${datasetLabel}: ${value.toFixed(2)}B`;
                        } else {
                            return `${datasetLabel}: ${value}`;
                        }
                    }
                }
            }
        }
    }
});
