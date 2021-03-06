import { ChartsModule } from 'ng2-charts';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { RouterModule } from '@angular/router';
import { ServiceService } from '../service/service.service';
import { HomePage } from './home.page';
import { ChartComponent } from '../component/chart/chart.component';

import { HighchartsChartModule } from 'highcharts-angular';
import { HeaderComponent } from '../component/header/header.component';
import { FooterComponent } from '../component/footer/footer.component';
@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    ChartsModule,
    HighchartsChartModule,

    RouterModule.forChild([
      {
        path: '',
        component: HomePage
      }
    ])
  ],
  declarations: [HomePage, ChartComponent, HeaderComponent, FooterComponent],
  providers: [ServiceService]
})
export class HomePageModule {}
