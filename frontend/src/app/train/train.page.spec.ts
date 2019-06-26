import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TrainPage } from './train.page';

describe('TrainPage', () => {
  let component: TrainPage;
  let fixture: ComponentFixture<TrainPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TrainPage ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TrainPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
