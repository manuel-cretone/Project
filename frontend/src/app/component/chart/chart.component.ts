import { Serverdata } from './../../interface/Serverdata.interface';
import { Component, OnInit, Input, OnChanges } from '@angular/core';
import { ServiceService } from '../../service/service.service';
import * as Highcharts from 'highcharts';
import { Chart, StockChart } from 'angular-highcharts';
@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.scss']
})
export class ChartComponent implements OnChanges {
  constructor(private service: ServiceService) {}
  // tslint:disable-next-line:no-input-rename
  @Input('signals') signals: Serverdata;
  // tslint:disable-next-line:no-input-rename
  @Input('distribution') distribution: { hist: []; bins: [] };
  public highChartsOptions: Highcharts.Options;
  barChartLabels = new Array<any>();
  chartType: string;
  barChartData = [1, 2];
  highcharts = Highcharts;
  barChartOptions;
  yAxses;

  // barChartOptions = [];
  loadData() {
    this.barChartOptions = {
      chart: {
        type: this.chartType
      },
      title: {
        text: 'Monthly Average Temperature'
      },
      subtitle: {
        text: 'Source: WorldClimate.com'
      },
      xAxis: {
        categories: [],
        crosshair: true
      },
      yAxis: this.yAxses,
      tooltip: {
        valueSuffix: ''
      },
      series: [{ data: this.barChartData }]
    };
  }
  //   scaleShowVerticalLines: false,
  //   responsive: true,
  //   scales: {
  //     xAxes: [
  //       {
  //         ticks: {
  //           autoSkip: true,
  //           autoSkipPadding: 50
  //         }
  //       }
  //     ]
  //   },
  //   elements: {
  //     point: {
  //       radius: 0
  //     }
  //   }
  // };

  /////////////////////////////////////////////////////////////////////
  // Highcharts = Highcharts;
  // series = [];
  // dataHigh;
  // seriesCount = 20;
  // pointsCount = 100;
  // axisTop = 50;
  // range;
  // axisHeight = 1100 / this.seriesCount;
  // yAxis = [];

  // chartHigh() {
  //   for (let i = 0; i < this.seriesCount; i++) {
  //     this.range = Math.round(Math.random() * 100);
  //     this.dataHigh = [];
  //     for (let x = 0; x < this.pointsCount; x++) {
  //       this.dataHigh.push(Math.floor(Math.random() * this.range));
  //     }
  //     this.series.push({
  //       data: this.dataHigh,
  //       yAxis: i
  //     });
  //     this.yAxis.push({
  //       title: {
  //         text: ''
  //       },
  //       height: this.axisHeight,
  //       top: this.axisTop,
  //       offset: 0
  //     });
  //     this.axisTop += this.axisHeight + 12.5;
  //   }
  //   Highcharts.chart('container', {
  //     chart: {
  //       height: 1500
  //     },
  //     series: this.series,
  //     yAxis: this.yAxis
  //   });
  // }

  ////////////////////////////////////////////////////////////////////
  ngOnChanges() {
    console.log('siamo in SIGNALS');
    console.log(this.signals);
    // this.chartHigh();
    // this.fillLineChart(this.signals);
    this.fillAllChart();
    if (this.distribution) {
      console.log('siamo in DISTRIBUTION');
      console.log(this.distribution);
      this.fillBarChart(this.distribution);
    }
  }
  async fillLineChart(signal: Serverdata) {
    this.chartType = 'line';
    this.barChartData = signal.valori;
    this.barChartOptions.xAxis.categories = signal.timeScale;
    this.loadData();
  }

  // Statistiche sul grafico bar chart
  fillBarChart(distr: { hist: []; bins: [] }) {
    this.chartType = 'column';
    this.barChartOptions.chart.type = this.chartType;
    this.barChartOptions.xAxis.categories = distr.bins;
    this.barChartData = distr.hist;
    this.yAxses = {
      title: {
        text: ''
      }
    };
    this.loadData();
    // this.barChartOptions.scales.xAxes = [];
  }
  fillAllChart() {
    console.log('ALL CHART');
    const data = [];
    let dat = [];
    const seriesCount = 20;
    const pointsCount = 100;
    let axisTop = 50;
    let range;
    const axisHeight = 1100 / seriesCount;
    const yAxis = [];

    for (let i = 0; i < seriesCount; i++) {
      range = Math.round(Math.random() * 100);
      dat = [];
      for (let j = 0; j < pointsCount; j++) {
        data.push(Math.floor(Math.random() * range));
      }
      dat.push({
        data: dat,
        yAxis: i
      });
      yAxis.push({
        title: {
          text: ''
        },
        height: axisHeight,
        top: axisTop,
        offset: 0
      });

      axisTop += axisHeight + 12.5;
    }

    this.barChartData = dat;
    console.log(dat);
    this.yAxses = yAxis;
    this.loadData();
  }
}
