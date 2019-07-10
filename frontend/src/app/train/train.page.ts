import { HttpErrorResponse } from '@angular/common/http';
import { ServiceService } from './../service/service.service';
import { Component, OnInit, Input, OnChanges } from '@angular/core';
import { UploadData } from '../interface/UploadData.interface';
import { LoadingController } from '@ionic/angular';

@Component({
  selector: 'app-train',
  templateUrl: './train.page.html',
  styleUrls: ['./train.page.scss']
})
export class TrainPage implements OnInit, OnChanges {
  listOfFile;
  paramsConv: {
    message: {
      input: any;
      output: any;
      kernel: any;
      stride: any;
      padding: any;
      pool_kernel: any;
      pool_stride: any;
      out_dim: any;
    };
  };
  checked: boolean;
  error: any;
  constructor(
    private service: ServiceService,
    private loadingController: LoadingController
  ) {}

  @Input() startSeizure: number;
  @Input() seizureEnd: number;
  @Input() windowSize: number;
  @Input() stride: number;
  @Input() epochs: number;
  @Input() selectMethod: string;
  @Input() networkName: string;

  // params for creaing convolutional network
  @Input() input: number;
  @Input() output: number;
  @Input() kernel: number;
  @Input() strideConv: number;
  @Input() padding: number;
  @Input() poolkernel: number;
  @Input() poolstride: number;
  @Input() linear: number;

  file: File = null;
  upload: UploadData;
  checkFile = false;

  ngOnInit() {}

  ngOnChanges() {
    // if (
    //   this.input !== undefined &&
    //   this.output !== undefined &&
    //   this.kernel !== undefined &&
    //   this.strideConv !== undefined &&
    //   this.padding !== undefined &&
    //   this.poolkernel !== undefined &&
    //   this.poolstride !== undefined
    // ) {
    //   this.checked = true;
    // }
  }
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
  async onUploadTrain() {
    const uploadData = new FormData();
    if (this.file != null) {
      uploadData.append('myfile', this.file, this.file.name);
      console.log(uploadData);
      const loader: any = await this.loadingController.create({
        message: 'Please Wait',
        cssClass: 'custom-loading',
        mode: 'ios',
        spinner: 'bubbles'
      });
      loader.present();
      await this.service
        .upTraining(uploadData, this.startSeizure, this.seizureEnd)
        .then(data => {
          this.listOfFile = data.uploaded;
        });
      loader.dismiss();
      console.log(this.listOfFile);

      this.checkFile = true;
    } else {
      this.checkFile = false;
    }
  }

  makeConvert() {
    this.service.doConvert(this.windowSize, this.stride).then(
      // data => {},
      (errors: HttpErrorResponse) => (this.error = errors.statusText)
    );
  }

  async makeTrain() {
    console.log(this.selectMethod);
    const a = await this.service.getTrain(this.epochs, this.selectMethod);
    console.log(a);
  }

  makeCleanFile() {
    this.service.makeCleanFiles();
    console.log(this.service.makeCleanFiles());
    this.listOfFile = null;
  }

  async makeConvolutionalNet() {
    if (
      this.input !== undefined &&
      this.output !== undefined &&
      this.kernel !== undefined &&
      this.strideConv !== undefined &&
      this.padding !== undefined &&
      this.poolkernel !== undefined &&
      this.poolstride !== undefined
    ) {
      this.checked = true;
      this.Convolutional();
      this.input = null;
      this.output = null;
      this.kernel = null;
      this.strideConv = null;
      this.padding = null;
      this.poolkernel = null;
      this.poolstride = null;
    }
  }

  async Convolutional() {
    return await this.service
      .makeConvolutional(
        this.input,
        this.output,
        this.kernel,
        this.strideConv,
        this.padding,
        this.poolkernel,
        this.poolstride
      )
      .then(data => {
        console.log(data);
        this.paramsConv = data;
        console.log(this.paramsConv);
      });
  }

  async createNetwork() {
    await this.service.initializeNetwork(this.linear);
  }
  cleanLayers() {
    console.log('yftguyhuj');
    this.service.makeCleanLayers();
  }
}
