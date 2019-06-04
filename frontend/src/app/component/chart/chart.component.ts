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
  // tslint:disable-next-line:no-input-rename
  @Input('allSignalsChannels') allSignalsChannels: {
    inizio: number;
    dimensione: number;
    window: [][];
    timeScale: [];
  };
  public highChartsOptions: Highcharts.Options;
  barChartLabels = new Array<any>();
  chartType: string;
  barChartData = [];
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
      scrollbar: {
        enabled: true
      },
      subtitle: {
        text: 'Source: WorldClimate.com'
      },
      xAxis: {
        categories: [],
        crosshair: true,
        scrollbar: {
          enabled: true,
          showFull: false
        }
      },
      yAxis: this.yAxses,
      tooltip: {
        valueSuffix: ''
      },
      series: this.barChartData
    };
  }

  ////////////////////////////////////////////////////////////////////
  async ngOnChanges() {
    // console.log('siamo in SIGNALS');
    // console.log(this.signals);
    // this.chartHigh();
    // this.fillLineChart(this.signals);
    console.log('siamo in ALL signals');
    console.log(this.allSignalsChannels);
    if (this.allSignalsChannels) {
      this.fillAllChart(this.allSignalsChannels);
    }

    if (this.distribution) {
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
    const dat = [];
    this.chartType = 'column';
    this.barChartData.push({ data: distr.hist });
    dat.push({
      data: distr.hist
    });

    this.barChartData = dat;
    this.yAxses = {
      title: {
        text: ''
      }
    };
    this.loadData();
    // this.barChartOptions.scales.xAxes = [];
  }

  // load all signal channel
  fillAllChart(signals: {
    inizio: number;
    dimensione: number;
    window: [][];
    timeScale: [];
  }) {
    const data = [];
    const dat = [];
    const seriesCount = 20;
    let axisTop = 50;
    const axisHeight = 100;
    const yAxis = [];
    console.log('siamo in fillALLCHART');
    console.log(signals.window[0]);
    for (let i = 0; i < 23; i++) {
      // console.log(signals.window[i]);
      // dat = [];
      dat.push({
        data: signals.window[i],
        yAxis: i
      });
      yAxis.push({
        title: {
          text: ''
        },
        height: axisHeight,
        top: axisTop,
        offset: 0,
        scrollbar: {
          enabled: true,
          showFull: false
        }
      });
      axisTop += axisHeight + 50;
    }
    this.barChartData = dat;
    this.yAxses = yAxis;
    this.loadData();
  }
}
