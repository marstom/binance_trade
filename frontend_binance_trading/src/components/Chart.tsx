import { Bar } from "react-chartjs-2";

interface Props {
  chartData: any;
}

export const Chart: React.FC<Props> = ({ chartData }) => {
  return (
    <div>
      <Bar
        data={{}}
        options={{
          plugins: {
            title: {
              display: true,
              text: "Cryptocurrency prices",
            },
            legend: {
              display: true,
              position: "bottom",
            },
          },
        }}
      />
    </div>
  );
};
