import { Serverdata } from './../interface/Serverdata.interface';
import { UploadData } from '../interface/UploadData.interface';
import { Component, OnInit, Input } from '@angular/core';
import { ServiceService } from '../service/service.service';

import { Statistics } from '../interface/Statistics.interface';
import { Page1Service } from './page1.service';
import { LoadingController } from '@ionic/angular';

@Component({
  selector: 'app-page1',
  templateUrl: './page1.page.html',
  styleUrls: ['./page1.page.scss']
})
export class Page1Page implements OnInit {
  constructor(
    private service: ServiceService,
    private page1service: Page1Service,
    private loadingController: LoadingController
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
  Channels: string[];
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

  async allSignals(start, numberSignals) {
    await this.service
      .getAllSignals(start, numberSignals)
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
      const channel = this.page1service.numberOfList(
        this.upload.channelLabels,
        this.selectChannel
      );

      if (channel === undefined) {
        await this.allSignals(this.selectStart, this.selectNumberSignal);
        this.distribution = null;
        this.signals = null;
        this.Statistics = null;
      } else {
        const loader: any = await this.loadingController.create({
          message: 'Please Wait',
          cssClass: 'custom-loading',
          mode: 'ios',
          spinner: 'bubbles'
        });
        loader.present();
        await this.signal(channel, this.selectStart, this.selectNumberSignal);
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
        loader.dismiss();

        this.allSignalsChannels = null;
      }
      // this.chart.fillLineChart(this.signals, this.selectChannel);
    }

    // this.upload = null;
    // this.selectChannel = null;
    // this.selectStart = null;
    // this.selectNumberSignal = null;
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
