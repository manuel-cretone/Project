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
  @Input()
  selectChannel = null;

  constructor(private service: ServiceService) {}
  signals: Serverdata;
  file: File = null;
  upload: UploadData;
  checkFile = false;
  Channels;

  ngOnInit() {}

  async signal() {
    await this.service.getSignal('4', '10', '2').then((data: Serverdata) => {
      this.signals = data;
    });
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
    console.log(this.selectChannel);
    console.log(this.Channels);
  }
}
