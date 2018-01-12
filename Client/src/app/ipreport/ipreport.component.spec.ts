import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { IpreportComponent } from './ipreport.component';

describe('IpreportComponent', () => {
  let component: IpreportComponent;
  let fixture: ComponentFixture<IpreportComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ IpreportComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(IpreportComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
