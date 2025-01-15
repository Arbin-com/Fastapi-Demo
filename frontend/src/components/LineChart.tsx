import React from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend
);

interface DynamicLineChartProps {
  title: string;
  data: { test_time: number; value: number }[];
  color: string;
}

const DynamicLineChart: React.FC<DynamicLineChartProps> = ({
  title,
  data,
  color,
}) => {
  const transparentColor = color.replace("1)", "0.2)");
  const chartData = {
    labels: data.map((point) => point.test_time),
    datasets: [
      {
        label: title,
        data: data.map((point) => point.value),
        borderColor: color,
        backgroundColor: transparentColor,
        borderWidth: 2,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    scales: {
      x: { title: { display: true, text: "Time (s)" } },
      y: { title: { display: true, text: title } },
    },
  };

  return <Line data={chartData} options={chartOptions} />;
};

export default DynamicLineChart;
