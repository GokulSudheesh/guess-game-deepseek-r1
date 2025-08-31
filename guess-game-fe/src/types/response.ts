import { GenericResponse } from "./generic-response";

interface IResponse {
  session_id: string;
  question: string;
  guess: string | null;
  confidence: number;
  question_number: number;
}

export type APIResponse = GenericResponse<IResponse>;
