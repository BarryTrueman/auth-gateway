// types.ts
import { IError } from './error';

export interface IGatewayConfig {
  authGateway: {
    port: number;
    host: string;
    clientRootUrl: string;
  };
}

export interface IAuthRequest {
  username: string;
  password: string;
}

export interface IAuthResponse {
  token: string;
  expiresAt: number;
}

export interface IErrorResponse {
  error: IError;
}