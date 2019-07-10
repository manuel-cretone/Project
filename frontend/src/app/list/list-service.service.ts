import { ServiceService } from './../service/service.service';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ListServiceService {
  constructor(private service: ServiceService) {}

  async drawSeizure(start, len) {
    await this.service
      .getAllSignals(start, len)
      .then(
        (data: {
          inizio: number;
          dimensione: number;
          window: [][];
          timeScale: [];
        }) => {
          return data;
        }
      );
  }

  numberOfList(list: string[], value: string) {
    for (let i = 0; i < list.length; i++) {
      if (list[i] === value) {
        return i;
      }
    }
  }
}
