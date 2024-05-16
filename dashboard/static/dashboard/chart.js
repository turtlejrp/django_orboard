const labels = [
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
];

const data = {
  labels: labels,
  datasets: [
    {
      label: "Actual",
      backgroundColor: ["rgb(255, 99, 132)", "aquamarine"],
      borderColor: ["rgb(255, 99, 132)", "aquamarine"],
      borderWidth: 2,
      borderRadius: 5,
      data: "{{Actual}}",
    },
    {
      label: "Target",
      backgroundColor: "rgb(255,255,255,0.5)",
      borderColor: "rgb(255,255,255,0.5)",
      borderWidth: 2,
      borderRadius: 5,
      data: "{{Plan}}",
    },
  ],
};

const config = {
  type: "bar",
  data: data,
  plugins: [ChartDataLabels],
  options: {
    indexAxis: "y",
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
            size: 13,
            weight: "bold",
          },
          color: "white",
        },
        barThickness: 20,
      },
      y: {
        ticks: {
          font: {
            size: 13,
            weight: "bold",
          },
          color: "white",
        },
      },
    },
  },
};
const myChart = new Chart(
  document.getElementById("myChart").getContext("2d"),
  config
);
