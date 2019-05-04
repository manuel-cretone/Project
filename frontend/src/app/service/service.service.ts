import { Serverdata } from '../interface/Serverdata.interface';
import { UploadData } from '../interface/UploadData.interface';
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ServiceService {
  constructor(private http: HttpClient) {}

  getSignal(channel: string, len: string, start: string) {
    const params = new HttpParams()
      .set('channel', channel)
      .set('len', len)
      .set('start', start);
    return this.http
      .get('http://127.0.0.1:8000/newupload/manageparam/', {
        params
      })
      .toPromise();
  }

  UploadFile(file: FormData) {
    return this.http.post('http://127.0.0.1:8000/newupload/', file).toPromise();
  }
}
