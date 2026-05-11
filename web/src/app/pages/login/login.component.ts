import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NgIf } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, NgIf],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {
  email = 'admin@techintel.com';
  password = 'Admin@123';
  loading = false;
  error = '';

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  onLogin(): void {
    this.loading = true;
    this.error = '';

    setTimeout(() => {
      const success = this.authService.login(this.email.trim(), this.password.trim());

      if (success) {
        this.router.navigate(['/dashboard']);
      } else {
        this.error = 'Invalid email or password';
      }

      this.loading = false;
    }, 200);
  }
}