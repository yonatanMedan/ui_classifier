import { TestBed } from '@angular/core/testing';

import { SanicService } from './sanic.service';

describe('SanicService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: SanicService = TestBed.get(SanicService);
    expect(service).toBeTruthy();
  });
});
