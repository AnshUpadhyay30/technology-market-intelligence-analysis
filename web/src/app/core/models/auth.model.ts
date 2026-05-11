export interface LoginRequest {
    email: string;
    password: string;
  }
  
  export interface LoginResponse {
    status: string;
    message: string;
    access_token: string;
    user: {
      email: string;
      name: string;
      role: string;
    };
  }