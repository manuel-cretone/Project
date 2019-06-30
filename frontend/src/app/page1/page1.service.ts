import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class Page1Service {
  constructor() {}
  numberOfList(list: string[], value: string) {
    for (let i = 0; i < list.length; i++) {
      if (list[i] === value) {
        return i.toString();
      }
    }
  }
}
