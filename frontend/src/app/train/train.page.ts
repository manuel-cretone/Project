import { ServiceService } from './../service/service.service';
import { Component, OnInit, Input } from '@angular/core';
import { UploadData } from '../interface/UploadData.interface';

@Component({
  selector: 'app-train',
  templateUrl: './train.page.html',
  styleUrls: ['./train.page.scss']
})
export class TrainPage implements OnInit {
  constructor(private service: ServiceService) {}

  @Input() startSeizure: number;
  @Input() seizureEnd: number;
  @Input() windowSize: number;
  @Input() stride: number;
  @Input() epochs: number;
  @Input() selectMethod: string;
  @Input() networkName: string;
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
  onUploadTrain() {
    const uploadData = new FormData();
    if (this.file != null) {
      uploadData.append('myfile', this.file, this.file.name);
      console.log(uploadData);
      this.service.upTraining(uploadData, this.startSeizure, this.seizureEnd);

      console.log(this.startSeizure);
      console.log(this.seizureEnd);
      this.checkFile = true;
    } else {
      this.checkFile = false;
    }
  }

  makeConvert() {
    this.service.doConvert(this.windowSize, this.stride);
  }

  async makeTrain() {
    const a = await this.service.getTrain(this.epochs, 0);
    console.log(a);
  }
}
