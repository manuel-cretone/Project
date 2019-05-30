import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class HomeService {
  constructor() {}

  numberOfList(list: string[], value: string) {
    for (let i = 0; i < list.length; i++) {
      if (list[i] === value) {
        return i.toString();
      }
    }
  }
}
