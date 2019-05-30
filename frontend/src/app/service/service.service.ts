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
}
