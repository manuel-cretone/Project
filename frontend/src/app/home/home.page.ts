import { HomeService } from './home.service';
import { Serverdata } from './../interface/Serverdata.interface';
import { UploadData } from '../interface/UploadData.interface';
import { Component, OnInit, Input } from '@angular/core';
import { ServiceService } from '../service/service.service';

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
  distribution: { hist: []; bins: [] };

  ngOnInit() {}

  async signal(channel, start, numberSignals) {
    await this.service
      .getSignal(channel, start, numberSignals)
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
    console.log(this.selectChannel);
    console.log(this.Channels);
    this.onUpload();
    console.log('DATTTTTAAA');
    console.log(this.upload);
    if (this.checkButton) {
      const channel = this.homeService.numberOfList(
        this.upload.channelLabels,
        this.selectChannel
      );

      await this.signal(channel, this.selectStart, this.selectNumberSignal);
      // this.chart.fillLineChart(this.signals, this.selectChannel);
      await this.getStatistics(
        channel,
        this.selectStart,
        this.selectNumberSignal
      );
      await this.getOccurrency(
        channel,
        this.selectStart,
        this.selectNumberSignal
      );
    }
    this.upload = null;
    this.selectChannel = null;
    this.selectStart = null;
    this.selectNumberSignal = null;
  }

  async getStatistics(channel, start, numberSignals) {
    await this.service
      .gestStatistics(channel, start, numberSignals)
      .then((data: Statistics) => {
        this.Statistics = data;
      });
    console.log(this.Statistics);
  }

  async getOccurrency(channel, start, numberSignals) {
    this.distribution = await this.service.getOccurrency(
      channel,
      start,
      numberSignals
    );
    console.log(this.distribution);
  }
}
