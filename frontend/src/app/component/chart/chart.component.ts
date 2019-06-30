import { StockChart } from 'angular-highcharts';
import { Serverdata } from './../../interface/Serverdata.interface';
import { Component, OnInit, Input, OnChanges } from '@angular/core';
import { ServiceService } from '../../service/service.service';
import * as Highcharts from 'highcharts/highstock';
@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.scss']
})
export class ChartComponent implements OnChanges {
  categories: any;
  fillSignal: any[];
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
  chartType;
  barChartData = [];
  highcharts = Highcharts;
  barChartOptions;
  yAxses;

  // barChartOptions = [];
  loadData() {
    this.barChartOptions = {
      chart: this.chartType,
      scrollbar: {
        enabled: true
      },
      title: {
        text: 'Monthly Average Temperature'
      },
      subtitle: {
        text: 'Source: WorldClimate.com'
      },
      xAxis: {
        categories: this.categories,
        min: 0,
        max: 1000,

        crosshair: true,
        visible: false
      },
      yAxis: this.yAxses,
      tooltip: {
        valueSuffix: ''
      },
      series: this.barChartData
    };
    console.log(this.yAxses);
  }

  ////////////////////////////////////////////////////////////////////
  async ngOnChanges() {
    console.log(' ALL signals CHENNEL');
    console.log(this.allSignalsChannels);
    if (this.allSignalsChannels) {
      this.fillAllChart(this.allSignalsChannels);
    }
    if (this.signals) {
      this.allSignalsChannels = null;
      this.fillLineChart(this.signals);
    }
    if (this.distribution) {
      this.fillBarChart(this.distribution);
    }
    this.allSignalsChannels = null;
    this.signals = null;
    this.distribution = null;
  }

  async fillLineChart(signal: Serverdata) {
    const dat = [];
    dat.push({
      data: signal.valori
    });
    this.barChartData = [];
    console.log('barchar DATA in FILL LINE CHART');
    console.log(this.barChartData);
    this.yAxses = [];
    this.barChartData = dat;
    console.log(this.barChartData);
    this.yAxses = {
      title: {
        text: ''
      }
    };
    this.categories = signal.timeScale;
    this.chartType = {
      width: 1000,
      type: 'line',
      zoomType: 'x  ',
      panning: true,
      panKey: 'shift'
    };
    this.loadData();
  }

  // Statistiche sul grafico bar chart
  fillBarChart(distr: { hist: []; bins: [] }) {
    const dat = [];
    this.chartType = 'column';
    // this.barChartData.push({ data: distr.hist });
    dat.push({
      data: distr.hist
    });

    this.barChartData = dat;
    this.yAxses = {
      title: {
        text: ''
      }
    };
    this.chartType = {
      type: 'bar',
      zoomType: 'x  ',
      panning: true,
      panKey: 'shift'
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
    this.signals = null;
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
        yAxis: i,
        showInLegend: false
      });
      yAxis.push({
        title: {
          text: ''
        },
        height: axisHeight,
        top: axisTop,
        offset: 0
      });
      axisTop += axisHeight + 50;
    }
    this.barChartData = [];
    this.barChartData = dat;
    this.yAxses = yAxis;
    console.log(this.yAxses);
    this.chartType = {
      height: 3500,
      width: 1000,
      type: 'line',
      zoomType: 'x  ',
      panning: true,
      panKey: 'shift'
    };

    this.loadData();
  }
}
