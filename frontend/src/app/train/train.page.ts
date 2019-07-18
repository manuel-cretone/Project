import { HttpErrorResponse } from '@angular/common/http';
import { ServiceService } from './../service/service.service';
import { Component, OnInit, Input, OnChanges } from '@angular/core';
import { UploadData } from '../interface/UploadData.interface';
import { LoadingController } from '@ionic/angular';
import { THIS_EXPR } from '@angular/compiler/src/output/output_ast';

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
  paramsConvolutional;
  checked: boolean;
  errorUploadFile;
  errorDataset;
  errorSettingNet;
  errorCreateNet;
  errorTrain;

  @Input() startSeizure: number;
  @Input() seizureEnd: number;
  @Input() windowSize: number;
  @Input() stride: number;
  @Input() epochs: number;
  @Input() selectMethod: string;
  @Input() networkName: string;

  // params for creaing convolutional network

  @Input() output: number;
  @Input() kernel: number;
  @Input() strideConv: number;
  @Input() padding: number;
  @Input() poolkernel: number;
  @Input() poolstride: number;
  @Input() linear: number;
  @Input() name: string;

  file: File = null;
  upload: UploadData;
  checkFile = false;
  trainParameters;
  delete: boolean;
  checkDataset: boolean;

  checkNetConvolutional: boolean;
  checkLinearNet: boolean;

  checkTrain: boolean;
  messageCreationDataset: boolean;
  messageCreationNet: boolean;

  constructor(
    private service: ServiceService,
    private loadingController: LoadingController
  ) {}

  ngOnInit() {}

  ngOnChanges() {}
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

      await this.service
        .upTraining(uploadData, this.startSeizure, this.seizureEnd)
        .then(
          data => {
            this.listOfFile = data.uploaded;
          },
          (error: HttpErrorResponse) =>
            (this.errorUploadFile = error.statusText)
        );

      this.startSeizure = null;
      this.seizureEnd = null;
      this.checkFile = true;
    } else {
      this.checkFile = false;
    }
  }

  async makeConvert() {
    const loader: any = await this.loadingController.create({
      message: 'Please Wait, dataset creating...',
      cssClass: 'custom-loading',
      mode: 'ios',
      spinner: 'bubbles'
    });
    loader.present();
    await this.service.doConvert(this.windowSize, this.stride).then(
      data => {
        console.log(data);
        this.checkDataset = false;
      },
      (errors: HttpErrorResponse) => {
        this.errorDataset = errors.statusText;
        this.checkDataset = true;
        this.messageCreationDataset = false;
      }
    );

    loader.dismiss();
    if (this.checkDataset === false) {
      this.messageCreationDataset = true;
    }
  }

  async makeTrain() {
    const loader: any = await this.loadingController.create({
      message: 'Please Wait, training in progress...',
      cssClass: 'custom-loading',
      mode: 'ios',
      spinner: 'bubbles'
    });
    loader.present();
    await this.service
      .getTrain(this.epochs, this.selectMethod, this.networkName)
      .then(
        data => {
          this.checkTrain = false;
          this.trainParameters = data;
        },
        (error: HttpErrorResponse) => {
          this.errorTrain = error.statusText;
          this.checkTrain = true;
        }
      );
    loader.dismiss();
  }

  makeCleanFile() {
    this.service.makeCleanFiles();
    console.log(this.service.makeCleanFiles());
    this.listOfFile = null;
  }

  async makeConvolutionalNet() {
    if (
      this.output !== undefined &&
      this.kernel !== undefined &&
      this.strideConv !== undefined &&
      this.padding !== undefined &&
      this.poolkernel !== undefined &&
      this.poolstride !== undefined
    ) {
      this.delete = true;
      this.Convolutional();
      this.output = null;
      this.kernel = null;
      this.strideConv = null;
      this.padding = null;
      this.poolkernel = null;
      this.poolstride = null;
    }
  }

  async Convolutional() {
    await this.service
      .makeConvolutional(
        this.output,
        this.kernel,
        this.strideConv,
        this.padding,
        this.poolkernel,
        this.poolstride
      )
      .then(
        data => {
          console.log(data);
          this.paramsConv = data;
          this.checkNetConvolutional = false;
          console.log(this.paramsConv);
        },
        (error: HttpErrorResponse) => {
          this.errorSettingNet = error.statusText;
          this.checkNetConvolutional = true;
        }
      );
    this.paramsConvolutional = Object.keys(this.paramsConv);
  }

  async createNetwork() {
    await this.service.initializeNetwork(this.linear).then(
      data => {
        this.checkLinearNet = false;
        this.messageCreationNet = true;
      },
      (error: HttpErrorResponse) => {
        this.errorCreateNet = error.statusText;
        this.checkLinearNet = true;
        this.messageCreationNet = false;
      }
    );
  }
  cleanLayers() {
    this.delete = false;
    this.service.makeCleanLayers();
  }
}
