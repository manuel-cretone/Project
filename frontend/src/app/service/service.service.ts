import { Serverdata } from './../interface/Serverdata.interface';

import { UploadData } from '../interface/UploadData.interface';
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ServiceService {
  constructor(private http: HttpClient) {}

  getSignal(channel: string, start: string, len: string) {
    const params = new HttpParams()
      .set('channel', channel)
      .set('start', start)
      .set('len', len);

    return this.http
      .get('http://127.0.0.1:8000/newupload/values/', {
        params
      })
      .toPromise();
  }

  UploadFile(file: FormData) {
    return this.http.post('http://127.0.0.1:8000/newupload/', file).toPromise();
  }

  gestStatistics(channel: string, start: string, len: string) {
    const params = new HttpParams()
      .set('channel', channel)
      .set('start', start)
      .set('len', len);

    return this.http
      .get('http://127.0.0.1:8000/newupload/statistics/', {
        params
      })
      .toPromise();
  }

  async getOccurrency(channel: string, start: string, len: string) {
    const params = new HttpParams()
      .set('channel', channel)
      .set('start', start)
      .set('len', len);

    return (await this.http
      .get('http://127.0.0.1:8000/newupload/distribution/', {
        params
      })
      .toPromise()) as { hist: any; bins: any };
  }
  addingNumberOfLineChart(channel: number[][]) {
    for (let i = 0; i < channel[1].length; i++) {
      channel[1][i] += 100;
    }

    return channel;
  }
  getAllSignals(start: string, len: string) {
    const params = new HttpParams().set('start', start).set('len', len);

    return this.http
      .get('http://127.0.0.1:8000/newupload/complete/', {
        params
      })
      .toPromise();
  }

  async getPredict(id?) {
    const params = new HttpParams().set('model_id', id);

    return (await this.http
      .get('http://127.0.0.1:8000/newupload/predict', { params })
      .toPromise()) as {
      time: any;
      values: any;
      seizureWindows: any;
      totalWindows: any;
    };
  }

  async getModels() {
    return (await this.http
      .get('http://127.0.0.1:8000/newupload/usermodels')
      .toPromise()) as { id: any; name: any };
  }
  /**
   *
   * @param file
   * @param seizureStart
   * @param seizureEnd
   */
  async upTraining(file: FormData, start, end) {
    console.log(file);
    console.log(start);
    console.log(end);

    const httpOptions = new HttpParams()
      .set('seizureStart', start)
      .set('seizureEnd', end);

    return (await this.http
      .post('http://127.0.0.1:8000/newupload/uptraining/', file, {
        params: httpOptions
      })
      .toPromise()) as { uploaded: any };
  }

  /**
   *
   * @param windowSize d
   * @param stride d
   */

  async doConvert(windowSize, stride) {
    const params = new HttpParams()
      .set('windowSize', windowSize)
      .set('stride', stride);
    return await this.http
      .get('http://127.0.0.1:8000/newupload/convert', { params })
      .toPromise();
  }

  /**
   *
   * @param epochs s
   * @param trainMethod s
   */
  getTrain(epochs, trainMethod, name) {
    const params = new HttpParams()
      .set('name', name)
      .set('epochs', epochs)
      .set('train_method', trainMethod);
    return this.http
      .get('http://127.0.0.1:8000/newupload/train', { params })
      .toPromise();
  }

  async makeCleanFiles() {
    await this.http
      .get('http://127.0.0.1:8000/newupload/cleanfiles')
      .toPromise();
  }

  async makeCleanModels() {
    await this.http
      .get('http://127.0.0.1:8000/newupload/cleanmodels/')
      .toPromise();
  }

  async makeConvolutional(
    output,
    kernel,
    stride,
    padding,
    poolkernel,
    poolstride
  ) {
    const params = new HttpParams()
      .set('output', output)
      .set('kernel', kernel)
      .set('stride', stride)
      .set('padding', padding)
      .set('pool_kernel', poolkernel)
      .set('pool_stride', poolstride);
    return (await this.http
      .get('http://127.0.0.1:8000/newupload/addconv/', { params })
      .toPromise()) as {
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
  }

  async initializeNetwork(linear) {
    const params = new HttpParams().set('linear', linear);
    return (await this.http
      .get('http://127.0.0.1:8000/newupload/initializenet', { params })
      .toPromise()) as { modules: any };
  }

  // cancella tutti i layer convoluzionali inseriti fino a quel momento
  async makeCleanLayers() {
    await this.http
      .get('http://127.0.0.1:8000/newupload/cleanlayers/')
      .toPromise();
  }
}
