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

import { ChartOptions } from "chart.js";

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
  const filteredData = data.filter(
    (point) => point.value !== null && point.value !== undefined
  );

  const chartData = {
    labels: filteredData.map((point) => {
      return Math.floor(point.test_time);
    }),
    datasets: [
      {
        label: title,
        data: filteredData.map((point) => point.value.toFixed(3)),
        borderColor: color,
        backgroundColor: transparentColor,
        borderWidth: 1,
      },
    ],
  };

  const chartOptions: ChartOptions<"line"> = {
    scales: {
      x: {
        title: { display: true, text: "Time (s)" },
      },
      y: {
        title: { display: true, text: title },
      },
    },
    plugins: {
      tooltip: {
        callbacks: {
          label: (context) => {
            const value = context.raw;
            return `Value: ${Number(value).toFixed(3)}`;
          },
        },
      },
    },
    layout: {
      padding: {
        left: 0,
        right: 0,
        top: 10,
        bottom: 10,
      },
    },
  };

  return <Line data={chartData} options={chartOptions} />;
};

export default DynamicLineChart;
