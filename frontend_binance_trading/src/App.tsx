import React, { useEffect, useState } from "react";
import "./App.css";
import { Chart } from "./components/Chart";

function App() {
  const [chartData, setChartData] = useState({});
  useEffect(() => {
    const data = { data: [{ name: "asdf", priceUsd: 2 }] };

    // setChartData({
    //   labels: data.data.map((crypto) => crypto.name),
    //   datasets: [
    //     {
    //       label: "Price in USD",
    //       data: data.data.map((crypto) => crypto.priceUsd),
    //       backgroundColor: [
    //         "#ffbb11",
    //         "#C0C0C0",
    //         "#50AF95",
    //         "#f3ba2f",
    //         "#2a71d0",
    //       ],
    //     },
    //   ],
    // });
  });

  return (
    <div className="App">
      <h2>My mongo app</h2>
      <Chart chartData={chartData} />
    </div>
  );
}

export default App;
