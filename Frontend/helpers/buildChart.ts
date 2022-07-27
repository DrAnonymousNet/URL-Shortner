// import Chart from "chart.js";
// import {Chart} from "chart.js"
import { ScaleType } from "chart.js";
import { ChartType, Scale, ScaleChartOptions, ScaleOptions } from "chart.js";
import Chart from "chart.js/auto";
import { endianness } from "os";
interface extendWindow extends Window {
  charts: Chart<"pie" | "line", number[], string>[];
  chart: Chart<"pie", number[], string>;
}

declare let window: extendWindow;
let windowInitialized = false;

// console.log(window.charts)
// let charts:  Chart<"pie", number[], string>[] = []
// let chart: any

// import { ChartType } from 'chart.js';

// const lineChartType: ChartType = "line";
// const pieChartType: ChartType = "pie";


const buildLegend = (legend: boolean) => {
  const legendConfig = {
    position: "right",
    labels: {
      fontFamily: "Lato",
      fontColor: "#f6f8fa",
    },
  };
  return legend ? legendConfig : null;
};

const buildScales = (axes: boolean) => {
  const scales = {
    x:   {
        ticks: {
          fontFamily: "Lato",
          fontColor: "#091E42",
          fontSize: 10,
          color: '#B3B9C4',
          tickLength: 30,
          // padding: 0

        },
        title: {
          text: "days in current month",
          display: true,
          align: 'end',
          color: "#2B7FFF"
        },
        grid: {
          // display: false
          color: '#E6F0FF'
        }
       
      },
      
    y: {
      ticks: {
        fontFamily: "Lato",
          fontColor: "#091E42",
          fontSize: 10,
          color: '#B3B9C4',
          stepSize: 1,
          // padding: 0

        },
        title: {
        text: "views",
          display: true,
          align:  'end',
          color: "#2B7FFF"

        }
        
      },
    
  };

  return axes ? scales : null
};

const buildChart = (config: IChartConfig, id: number) => {
  
  
  if (!windowInitialized) {
    // if(JSON.stringify(window.charts) != '[]') {
    //   window.charts.forEach(chart => chart.destroy)
    // }
    window.charts = [];
    windowInitialized = true;
  }
  // console.log(window.charts)
    
  if (window.charts[id]) window.charts[id].destroy();

  const {
    canvasElement,
    chartType,
    labels,
    data,
    backgroundColor,
    axes,
    legend,
  } = config;
  // ifwindow){
    let legend_labels: any
    // console.log(labels)
    // console.log(data)
    // if(chartType == ("pie" as ChartType)){
      //   legend_labels =  {
        //     boxWidth: 10,
        //     boxHeight: 9,
        //     padding: 12,
        //   }
        // }else legend_labels = ''
        
        window.charts[id] = new Chart(canvasElement, {
          // window.charts[id] = new Chart(canvasElement, {
            
            type: chartType,
            data: {
              labels,
              datasets: [
                { 
                  data,
                  backgroundColor,
                  borderWidth: 1,
                },
              ],
            },

    options: {
      elements:{
        point: {
          pointStyle: "circle",
          backgroundColor: "green",
          radius: 3,
          borderWidth: 15,
          borderColor: "#E6F0FF"
        },
        line: {
          borderColor: '#0065FF',
          borderWidth: 22
        }
      },
      scales: buildScales(axes),
      legend: buildLegend(legend),
      maintainAspectRatio:  chartType == "line" ? false : true ,
      responsive:true ,
      plugins: {
        
        
        legend: {
        
          position: "bottom",
          labels:  axes ? ' ' : {
            boxWidth: 10,
            boxHeight: 9,
            padding: 12,
          }
          
        },
        tooltip: {
          // fon
          // titleFont: "Lato",
          // bodyFont: "Lato",
          cornerRadius: 3,
        },
      },
    },
  });
  // return window.charts[id];
  
  // }
};

export default buildChart;
