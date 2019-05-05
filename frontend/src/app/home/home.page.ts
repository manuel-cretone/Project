import { ChartComponent } from './../component/chart/chart.component';
import { HomeService } from './home.service';
import { Serverdata } from './../interface/Serverdata.interface';
import { UploadData } from '../interface/UploadData.interface';
import { Component, OnInit, Input, ViewChild } from '@angular/core';
import { ServiceService } from '../service/service.service';
import { Chart } from 'chart.js';
import { Statistics } from '../interface/Statistics.interface';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss']
})
export class HomePage implements OnInit {
  constructor(
    private service: ServiceService,
    private homeService: HomeService
  ) {}
  @Input() selectChannel: string;
  @Input() selectStart: number;
  @Input() selectNumberSignal: number;
  signals: Serverdata;
  file: File = null;
  upload: UploadData;
  checkFile = false;
  checkButton = false;
  Channels;
  Statics: Statistics;
  ////////////////////////////////////////////////////////////////
  public barChartOptions: any = {
    scaleShowVerticalLines: false,
    responsive: true,
    fill: false
  };
  public barChartLabels: string[] = [];
  public barChartType = 'line';
  public barChart = 'bar';
  public barChartLegend = true;

  public barChartData: any[] = [{ data: [], label: 'Series A' }];

  ngOnInit() {}

  async signal(channel, numberSignals, start) {
    await this.service
      .getSignal(channel, numberSignals, start)
      .then((data: Serverdata) => {
        this.signals = data;
      });
    console.log(this.signals);
  }

  onFileSelected(event) {
    this.file = event.target.files[0];
  }

  async onUpload() {
    const uploadData = new FormData();
    if (this.file != null) {
      uploadData.append('myfile', this.file, this.file.name);
      await this.service.UploadFile(uploadData).then((data: UploadData) => {
        this.upload = data;
        this.Channels = data.channelLabels;
      });
      this.checkFile = true;
    } else {
      this.checkFile = false;
    }
  }

  async draw() {
    this.checkButton = true;
    if (this.checkButton) {
      const channel = this.homeService.numberOfList(
        this.upload.channelLabels,
        this.selectChannel
      );
      if (this.selectStart < 921600 && this.selectNumberSignal < 1001) {
        await this.signal(channel, this.selectNumberSignal, this.selectStart);
        // this.chart.fillLineChart(this.signals, this.selectChannel);
        // await this.getStatics(channel, this.selectNumberSignal, this.selectStart);
        this.barChartData = [
          { data: this.signals.valori, label: this.selectChannel, fill: false }
        ];
        this.barChartLabels = this.signals.timeScale;
      }
    }
  }

  // async getStatics(channel, numberSignals, start) {
  //   await this.service
  //     .gestStatistics(channel, start, numberSignals)
  //     .then((data: Statics) => {
  //       this.Statics = data;
  //     });
  //   console.log(this.Statics);
  // }
}
