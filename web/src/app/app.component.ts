import { Component } from '@angular/core';
import { NgClass, NgIf } from '@angular/common';
import { Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { AuthService } from './core/services/auth.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive, NgClass, NgIf],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  sidebarOpen = false;

  constructor(
    public router: Router,
    public authService: AuthService
  ) {}

  closeSidebar(): void {
    this.sidebarOpen = false;
  }

  toggleSidebar(): void {
    this.sidebarOpen = !this.sidebarOpen;
  }

  logout(): void {
    this.authService.logout();
    this.sidebarOpen = false;
    this.router.navigate(['/login']);
  }

  get isLoginPage(): boolean {
    return this.router.url === '/login';
  }
}