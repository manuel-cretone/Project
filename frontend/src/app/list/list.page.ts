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
  predict: { time: []; values: []; seizureWindows: any; totalWindows: any };

  a: { window: []; timeScale: [] };
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
      await this.service.getPredict(0).then(data => {
        this.predict = data;
      });
    } else {
      await this.service.getPredict(model).then(data => {
        this.predict = data;
      });
    }

    loader.dismiss();

    this.drawChart(
      this.a,
      this.listService,
      this.allSignalsChannels,
      this.service
    );

    this.checkPrediction = true;
    console.log(this.predict);
  }

  async getModels() {
    this.service.getModels().then(data => {
      this.Networks = data.name;
    });
  }

  drawChart(clicked: any, listService: ListServiceService, signals, service) {
    Highcharts.chart('chart', {
      chart: {
        type: 'column',
        zoomType: 'x',
        panning: true,
        panKey: 'shift'
      },

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
              async click() {
                console.log(this.category);
                clicked = await service.getAllSignals(this.category, 30);
                console.log(clicked);
                const series = [];
                const data = [];
                const seriesCount = 23,
                  pointsCount = 100;
                let axisTop = 50;

                const axisHeight = 1100 / seriesCount;
                const yAxis = [];

                for (let i = 0; i < seriesCount; i++) {
                  data.push({
                    data: clicked.window[i],
                    yAxis: i,
                    showInLegend: false
                  });

                  yAxis.push({
                    title: {
                      text: ''
                    },
                    height: axisHeight,
                    top: axisTop,
                    offset: 0
                  });

                  axisTop += axisHeight + 12.5;
                }

                Highcharts.chart('signalsChart', {
                  chart: {
                    height: 1500
                  },
                  series: data,
                  yAxis
                });

                // signals = listService.drawSeizure(this.category, 30);
                // console.log(clicked);
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

<<<<<<< HEAD
  DrawSignals(start: any, len: any) {}
=======
  drawSignals(start, len) {
    this.service.drawSignalSeizure(start, len);
    Highcharts.chart('chart', {
      chart: {
        type: 'column',
        zoomType: 'x',
        panning: true,
        panKey: 'shift'
      },
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

      series: [
        {
          
          data: this.predict.values
        }
      ]
    });
  }
>>>>>>> silvestri
}
