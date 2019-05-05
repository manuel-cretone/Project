import { Statistics } from '../../interface/Statistics.interface';
import { Serverdata } from './../../interface/Serverdata.interface';
import { Component, OnInit, Input } from '@angular/core';
import { ServiceService } from '../../service/service.service';
@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.scss']
})
export class ChartComponent implements OnInit {
  // tslint:disable-next-line:no-input-rename
  @Input('signals') signals: Serverdata;

  constructor(private service: ServiceService) {}

  barChartLabels = new Array<any>();
  barChartType = '';
  barChartOptions = {
    scaleShowVerticalLines: false,
    responsive: true,
    fill: false
  };
  public chartColors: Array<any> = [
    {
      backgroundColor: '#87BFFF'
    }
  ];

  public barChartData: any[] = [{ data: [], label: '' }];

  async ngOnInit() {
    console.log('siamo in COMPONENT');
    console.log(this.signals);
    this.fillLineChart(this.signals);
  }

  fillLineChart(signal: Serverdata) {
    this.barChartType = 'line';
    this.barChartData = [{ data: signal.valori, label: '' }];
    this.barChartLabels = signal.timeScale;
  }

  // Statistiche sul grafico bar chart
  fillBarChart(statistics: Statistics) {
    this.barChartType = 'bar';
  }
}
