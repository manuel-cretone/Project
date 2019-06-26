import { ServiceService } from './../service/service.service';
import { Component, OnInit } from '@angular/core';
import { UploadData } from '../interface/UploadData.interface';

@Component({
  selector: 'app-train',
  templateUrl: './train.page.html',
  styleUrls: ['./train.page.scss']
})
export class TrainPage implements OnInit {
  constructor(private service: ServiceService) {}

  file: File = null;
  upload: UploadData;
  checkFile = false;

  ngOnInit() {}

  /**
   *
   * @param event download file  event
   */
  onFileSelected(event) {
    this.file = event.target.files[0];
  }
  /**
   *
   */
  async onUpload() {
    const uploadData = new FormData();
    if (this.file != null) {
      uploadData.append('myfile', this.file, this.file.name);
      await this.service.UploadFile(uploadData);
      this.checkFile = true;
    } else {
      this.checkFile = false;
    }
  }
}
