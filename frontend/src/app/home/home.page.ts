import { HomeService } from './home.service';
import { Serverdata } from './../interface/Serverdata.interface';
import { UploadData } from '../interface/UploadData.interface';
import { Component, OnInit, Input } from '@angular/core';
import { ServiceService } from '../service/service.service';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss']
})
export class HomePage implements OnInit {
  @Input() selectChannel: string;
  @Input() selectStart: string;
  @Input() selectNumberSignal: string;

  constructor(
    private service: ServiceService,
    private homeService: HomeService
  ) {}
  signals: Serverdata;
  file: File = null;
  upload: UploadData;
  checkFile = false;
  checkButton = false;
  Channels;

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

  draw() {
    this.checkButton = true;
    const channel = this.homeService.numberOfList(
      this.upload.channelLabels,
      this.selectChannel
    );
    const start = this.selectStart;
    const numberSignals = this.selectNumberSignal;
    this.signal(channel, start, numberSignals);
    this.checkButton = false;
  }
}
