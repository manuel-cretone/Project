import { Component, OnInit, Input } from '@angular/core';
import { ServiceService } from '../service/service.service';
import { UploadData } from '../interface/UploadData.interface';
import * as Highcharts from 'highcharts/highstock';
import { LoadingController } from '@ionic/angular';
import { ListServiceService } from './list-service.service';
@Component({
  selector: 'app-list',
  templateUrl: 'list.page.html',
  styleUrls: ['list.page.scss']
})
export class ListPage implements OnInit {
  @Input() selectNetwork: string;
  Networks: [];
  upload: UploadData;
  checkFile = false;
  checkSubmit = false;
  checkPrediction = false;
  clicked: boolean;
  file: File = null;
  allSignalsChannels;
  predict: { time: []; values: [] };
  constructor(
    private service: ServiceService,
    private loadingController: LoadingController,
    private listService: ListServiceService
  ) {}
  ngOnInit() {
    this.getModels();
  }

  onFileSelected(event) {
    this.file = event.target.files[0];
    this.checkFile = true;
  }

  async onUpload() {
    const uploadData = new FormData();
    if (this.file != null) {
      uploadData.append('myfile', this.file, this.file.name);
      await this.service.UploadFile(uploadData);
      this.checkSubmit = true;
    } else {
      this.checkSubmit = false;
    }
  }
  /**
   *
   */
  async getPrediction() {
    const model = this.listService.numberOfList(
      this.Networks,
      this.selectNetwork
    );
    this.checkPrediction = false;
    const loader: any = await this.loadingController.create({
      message: 'Please Wait',
      cssClass: 'custom-loading',
      mode: 'ios',
      spinner: 'bubbles'
    });
    loader.present();
    if (model === undefined) {
      this.predict = await this.service.getPredict(0);
    } else {
      this.predict = await this.service.getPredict(model);
    }
    loader.dismiss();

    this.drawChart(this.clicked, this.listService, this.allSignalsChannels);
    this.checkPrediction = true;
    console.log(this.predict);
  }

  async getModels() {
    this.service.getModels().then(data => {
      this.Networks = data.name;
    });
  }

  drawChart(clicked: boolean, listService: ListServiceService, signals) {
    Highcharts.chart('chart', {
      chart: {
        type: 'column',
        zoomType: 'x',
        panning: true,
        panKey: 'shift'
      },
      // title: {
      //   text: 'Stacked bar chart'
      // },
      xAxis: {
        categories: this.predict.time,
        min: 0,

        scrollbar: {
          enabled: true
        }
      },
      yAxis: {
        min: 0,
        title: {
          text: 'Seizure Detected'
        }
      },
      legend: {
        reversed: true
      },
      plotOptions: {
        series: {
          stacking: 'normal',

          cursor: 'pointer',
          point: {
            events: {
              click() {
                clicked = true;
                signals = listService.drawSeizure(this.category, 30);
                console.log(clicked);
                // alert('Category: ' + this.category + ', value: ' + this.y);
              }
            }
          }
        }
      },
      series: [
        {
          data: this.predict.values
        }
      ]
    });
  }
}
