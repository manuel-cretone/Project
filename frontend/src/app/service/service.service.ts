import { Serverdata } from '../interface/Serverdata.interface';
import { UploadData } from '../interface/UploadData.interface';
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ServiceService {
  constructor(private http: HttpClient) {}

  async getSignal(channel: string, len: string, start: string) {
    const params = new HttpParams()
      .set('channel', channel)
      .set('len', len)
      .set('start', start);
    return (await this.http
      .get('http://127.0.0.1:8000/newupload/manageparam/', {
        params
      })
      .toPromise()) as Array<Serverdata>;
    // .subscribe((data: Serverdata[]) => {
    //   console.log(data);
    // });
  }
  async getFile(file: FormData) {
    return (await this.http
      .post('http://127.0.0.1:8000/newupload/', file)
      .toPromise()) as Array<UploadData>;
  }
}
