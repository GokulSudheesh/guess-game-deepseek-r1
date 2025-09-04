export interface GenericResponse<T> {
  success: boolean;
  data: T | null;
}

export interface ErrorResponse {
  detail: any;
}
