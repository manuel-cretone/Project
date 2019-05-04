import { Statistics } from '../../interface/Statistics.interface';
import { Serverdata } from './../../interface/Serverdata.interface';
import { Component, OnInit } from '@angular/core';
import { ServiceService } from '../../service/service.service';
@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.scss']
})
export class ChartComponent implements OnInit {
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

  async ngOnInit() {}

  // async ngOnChanges() {}
  fillLineChart(serverData: Serverdata, selectChannel: string) {
    this.barChartType = 'line';
    this.barChartData = [{ data: serverData.valori, label: selectChannel }];
    this.barChartLabels = serverData.timeScale;
  }

  // Statistiche sul grafico bar chart
  fillBarChart(statistics: Statistics) {
    this.barChartType = 'bar';
  }
}
