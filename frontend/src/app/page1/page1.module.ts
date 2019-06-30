import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';

import { IonicModule } from '@ionic/angular';

import { Page1Page } from './page1.page';
import { ChartsModule } from 'ng2-charts';
import { HighchartsChartModule } from 'highcharts-angular';
import { ServiceService } from '../service/service.service';
import { ChartComponent } from '../component/chart/chart.component';
import { HeaderComponent } from '../component/header/header.component';
import { FooterComponent } from '../component/footer/footer.component';

const routes: Routes = [
  {
    path: '',
    component: Page1Page
  }
];

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    ChartsModule,
    HighchartsChartModule,
    RouterModule.forChild(routes)
  ],
  declarations: [Page1Page, ChartComponent, HeaderComponent, FooterComponent],
  providers: [ServiceService]
})
export class Page1PageModule {}
