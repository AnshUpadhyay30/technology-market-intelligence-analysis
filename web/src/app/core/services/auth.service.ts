import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly authKey = 'techintel_logged_in_user';

  login(email: string, password: string): boolean {
    const validEmail = 'admin@techintel.com';
    const validPassword = 'Admin@123';

    if (email === validEmail && password === validPassword) {
      localStorage.setItem(
        this.authKey,
        JSON.stringify({
          email: validEmail,
          name: 'Admin User',
          role: 'ADMIN'
        })
      );
      return true;
    }

    return false;
  }

  isLoggedIn(): boolean {
    return !!localStorage.getItem(this.authKey);
  }

  getUser(): { email: string; name: string; role: string } | null {
    const raw = localStorage.getItem(this.authKey);
    return raw ? JSON.parse(raw) : null;
  }

  logout(): void {
    localStorage.removeItem(this.authKey);
  }
}