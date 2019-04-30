import { TestBed } from '@angular/core/testing';

import { Service.ServiceService } from './service.service';

describe('Service.ServiceService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: Service.ServiceService = TestBed.get(Service.ServiceService);
    expect(service).toBeTruthy();
  });
});
