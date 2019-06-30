import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { RouterModule } from '@angular/router';
import { ChartComponent } from '../component/chart/chart.component';
import { ListPage } from './list.page';
import { HeaderComponent } from '../component/header/header.component';
import { FooterComponent } from '../component/footer/footer.component';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,

    IonicModule,
    RouterModule.forChild([
      {
        path: '',
        component: ListPage
      }
    ])
  ],
  declarations: [ListPage, HeaderComponent, FooterComponent]
})
export class ListPageModule {}
