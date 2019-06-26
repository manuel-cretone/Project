import { Component, OnInit } from '@angular/core';
import { ServiceService } from '../service/service.service';
import { UploadData } from '../interface/UploadData.interface';
@Component({
  selector: 'app-list',
  templateUrl: 'list.page.html',
  styleUrls: ['list.page.scss']
})
export class ListPage implements OnInit {
  upload: UploadData;
  checkFile = false;
  file: File = null;
  constructor(private service: ServiceService) {}
  ngOnInit() {}

  onFileSelected(event) {
    this.file = event.target.files[0];
    this.checkFile = true;
  }

  async onUpload() {
    const uploadData = new FormData();
    if (this.file != null) {
      uploadData.append('myfile', this.file, this.file.name);
      await this.service.UploadFile(uploadData).then((data: UploadData) => {
        this.upload = data;
      });
      this.checkFile = true;
    } else {
      this.checkFile = false;
    }
  }
}
