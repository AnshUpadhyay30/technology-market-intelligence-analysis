import { Routes } from '@angular/router';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { TechnologiesComponent } from './pages/technologies/technologies.component';
import { CompetitorsComponent } from './pages/competitors/competitors.component';
import { ResearchSourcesComponent } from './pages/research-sources/research-sources.component';
import { ReportsComponent } from './pages/reports/reports.component';
import { LoginComponent } from './pages/login/login.component';
import { authGuard } from './core/services/auth.guard';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },

  { path: 'dashboard', component: DashboardComponent, canActivate: [authGuard] },
  { path: 'technologies', component: TechnologiesComponent, canActivate: [authGuard] },
  { path: 'competitors', component: CompetitorsComponent, canActivate: [authGuard] },
  { path: 'research-sources', component: ResearchSourcesComponent, canActivate: [authGuard] },
  { path: 'reports', component: ReportsComponent, canActivate: [authGuard] },

  { path: '**', redirectTo: 'login' }
];