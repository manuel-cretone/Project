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
  barChartType: string;
  barChartData = [];

  // barChartOptions = [];
  barChartOptions = {
    chart: {
      type: this.barChartType
    },
    title: {
      text: 'Monthly Average Temperature'
    },
    subtitle: {
      text: 'Source: WorldClimate.com'
    },
    xAxis: {
      categories: []
    },
    yAxis: {
      title: {
        text: 'Temperature °C'
      }
    },
    tooltip: {
      valueSuffix: ' °C'
    },
    series: {}[]
  };
  highcharts = new Highcharts.Chart(this.barChartOptions);
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
    this.fillLineChart(this.signals);
    if (this.distribution) {
      console.log('siamo in DISTRIBUTION');
      console.log(this.distribution);
      this.fillBarChart(this.distribution);
    }
  }
  async fillLineChart(signal: Serverdata) {
    this.barChartType = 'line';
    this.barChartData = signal.valori;
    console.log('FILL LINE CHART');
    console.log(this.barChartData);
    this.barChartOptions.xAxis.categories = [];
    this.barChartOptions.series[0].data.pop();
    this.barChartOptions.series[0].data.push(this.barChartData);
    this.highcharts.redraw(true);
    // this.highcharts.setOptions(this.highChartsOptions);
  }

  // Statistiche sul grafico bar chart
  fillBarChart(distr: { hist: []; bins: [] }) {
    this.barChartType = 'bar';
    // this.barChartData = distr.hist;
    // this.barChartLabels = distr.bins;
    this.barChartOptions.chart.type = this.barChartType;
    this.barChartOptions.xAxis.categories = distr.bins;
    this.barChartOptions.series[0].data = distr.hist;
    // this.barChartOptions.scales.xAxes = [];
  }
}
