import { UploadData } from '../interface/UploadData.interface';
import { Component, OnInit } from '@angular/core';
import { ServiceService } from '../service/service.service';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss']
})
export class HomePage implements OnInit {
  constructor(private service: ServiceService) {}
  signals: Array<any>;
  file: File = null;
  upload: Array<UploadData>;

  async ngOnInit() {
    // this.signals = await this.service.getSignal('4', '10', '2');
  }

  async signal() {
    // const f = new FileReader();
    // // this.service.getFile(this.file);
    // console.log(this.file);
    // console.log(f.readAsDataURL(this.file));
  }
  onFileSelected(event) {
    this.file = event.target.files[0];
  }
  async onUpload() {
    // upload code goes here
    const uploadData = new FormData();
    uploadData.append('myfile', this.file, this.file.name);

    this.upload = await this.service.getFile(uploadData);
    console.log(this.upload);
  }
}
