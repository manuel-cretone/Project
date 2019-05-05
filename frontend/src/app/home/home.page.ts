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
  Statistics: Statistics;
  distribution = { hist: [], bins: [] };
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
  public barData: any[] = [{ data: [], label: 'Series A' }];
  public barlabel: string[] = [];
  ///////////////////////////////////////////////////////////////
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

      await this.signal(channel, this.selectNumberSignal, this.selectStart);
      // this.chart.fillLineChart(this.signals, this.selectChannel);
      await this.getStatistics(
        channel,
        this.selectNumberSignal,
        this.selectStart
      );
      await this.getOccurrency(
        channel,
        this.selectNumberSignal,
        this.selectStart
      );
      this.barChartData = [
        { data: this.signals.valori, label: this.selectChannel, fill: false }
      ];
      this.barChartLabels = this.signals.timeScale;
    }
  }

  async getStatistics(channel, numberSignals, start) {
    await this.service
      .gestStatistics(channel, start, numberSignals)
      .then((data: Statistics) => {
        this.Statistics = data;
      });
    console.log(this.Statistics);
  }

  async getOccurrency(channel, numberSignals, start) {
    this.distribution = await this.service.getOccurrency(
      channel,
      start,
      numberSignals
    );
    console.log(this.distribution);
    this.barData = [
      {
        data: this.distribution.hist,
        label: this.selectChannel,
        fill: false
      }
    ];
    this.barlabel = this.distribution.bins;
  }
}
