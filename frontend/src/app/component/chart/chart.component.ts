import { Statistics } from '../../interface/Statistics.interface';
import { Serverdata } from './../../interface/Serverdata.interface';
import { Component, OnInit, Input, OnChanges } from '@angular/core';
import { ServiceService } from '../../service/service.service';
@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.scss']
})
export class ChartComponent implements OnChanges {
  // tslint:disable-next-line:no-input-rename
  @Input('signals') signals: Serverdata;
  // tslint:disable-next-line:no-input-rename
  @Input('distribution') distribution: { hist: []; bins: [] };
  constructor(private service: ServiceService) {}

  barChartLabels = new Array<any>();
  barChartType = '';
  barChartOptions = {
    scaleShowVerticalLines: false,
    responsive: true,
    scales: {
      xAxes: [
        {
          ticks: {
            autoSkip: true,
            autoSkipPadding: 50
          }
        }
      ]
    },
    elements: {
      point: {
        radius: 0
      }
    }
  };

  public barChartData: any[] = [{ data: [], label: '' }];

  ngOnChanges() {
    console.log('siamo in SIGNALS');
    console.log(this.signals);
    this.fillLineChart(this.signals);
    if (this.distribution) {
      console.log('siamo in DISTRIBUTION');
      console.log(this.distribution);
      this.fillBarChart(this.distribution);
    }
  }

  async fillLineChart(signal: Serverdata) {
    this.barChartType = 'line';
    this.barChartData = [{ data: signal.valori, label: '', fill: false }];
    this.barChartLabels = signal.timeScale;
  }

  // Statistiche sul grafico bar chart
  fillBarChart(distr: { hist: []; bins: [] }) {
    this.barChartType = 'bar';
    this.barChartData = [{ data: distr.hist, label: '', fill: false }];
    this.barChartLabels = distr.bins;
    this.barChartOptions.scales.xAxes = [];
  }
}
