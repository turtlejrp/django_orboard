var canvas = document.getElementById("dekidakaChart");
var ctx = canvas.getContext("2d");

var horizonalLinePlugin = {
  id: "horizontalLine",
  afterDraw: function (chartInstance) {
    var yScale = chartInstance.scales["y"];
    var index;
    var line;
    var style;

    if (chartInstance.options.horizontalLine) {
      for (
        index = 0;
        index < chartInstance.options.horizontalLine.length;
        index++
      ) {
        line = chartInstance.options.horizontalLine[index];

        if (!line.style) {
          style = "rgba(169,169,169, .6)";
        } else {
          style = line.style;
        }

        if (line.y) {
          yValue = yScale.getPixelForValue(line.y);
        } else {
          yValue = 0;
        }

        ctx.lineWidth = 3;

        if (yValue) {
          ctx.beginPath();
          ctx.moveTo(70, yValue);
          ctx.lineTo(canvas.width, yValue);
          ctx.strokeStyle = style;
          ctx.stroke();
        }

        if (line.text) {
          ctx.fillStyle = style;
          ctx.fillText(line.text, 0, yValue + ctx.lineWidth);
        }
      }
      return;
    }
  },
};

var dekidaka = {
  labels: [
    "7:35-8:30",
    "8:30-9:20",
    "9:30-10:30",
    "10:30-11:30",
    "12:30-13:30",
    "13:30-14:20",
    "14:30-15:30",
    "15:30-16:25",
    "16:50-17:50",
    "17:50-18:50",
    "18:50-19:15",
  ],
  datasets: [
    {
      label: "OR Percentage",
      fill: false,
      lineTension: 0.1,
      backgroundColor: "rgba(75,192,192,0.4)",
      borderColor: "rgba(75,192,192,1)",
      data: [90, 83, 80, 81, 92, 99, 78],
    },
  ],
};
//When uncommenting below line, graph is created without horizontal lines
Chart.register(horizonalLinePlugin);
var dekidakaChart = new Chart(ctx, {
  type: "line",
  data: dekidaka,
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      datalabels: {
        color: "black",
        font: { weight: "bold", size: 15 },
        anchor: "end",
        align: "end",
        offset: -30,
      },
      legend: {
        position: "bottom",
        labels: {
          color: "white",
          boxWidth: 20,
        },
      },
    },
    scales: {
      x: {
        ticks: {
          font: {
            size: 10,
            weight: "bold",
          },
          color: "white",
        },
        barThickness: 20,
      },
      y: {
        ticks: {
          beginAtZero: true,
          font: {
            size: 13,
            weight: "bold",
          },
          color: "white",
        },
      },
    },
    horizontalLine: [
      {
        y: 92,
        style: "#00ff00",
        text: "OR Target",
      },
      {
        y: 84,
        style: "#ff0000",
        text: "Lower-limit",
      },
    ],
  },
});
