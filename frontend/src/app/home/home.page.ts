import { HomeService } from './home.service';
import { Serverdata } from './../interface/Serverdata.interface';
import { UploadData } from '../interface/UploadData.interface';
import { Component, OnInit, Input } from '@angular/core';
import { ServiceService } from '../service/service.service';

import { Statistics } from '../interface/Statistics.interface';
import { __await } from 'tslib';

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
  allSignalsChannels: {
    inizio: number;
    dimensione: number;
    window: [][];
    timeScale: [];
  };
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

  async allSignals(channel, start, numberSignals) {
    await this.service
      .getAllSignals(channel, start, numberSignals)
      .then(
        (data: {
          inizio: number;
          dimensione: number;
          window: [][];
          timeScale: [];
        }) => {
          this.allSignalsChannels = data;
        }
      );

    // console.log(this.signals.chn0);
    // console.log(this.signals.chn1);
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
    await this.onUpload();
    if (this.checkButton) {
      const channel = this.homeService.numberOfList(
        this.upload.channelLabels,
        this.selectChannel
      );
      console.log('SELECT CHANNEL');
      console.log(this.selectChannel);
      await this.allSignals(channel, this.selectStart, this.selectNumberSignal);
      console.log('ALL SIGNALS');
      console.log(this.allSignalsChannels.window);
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
