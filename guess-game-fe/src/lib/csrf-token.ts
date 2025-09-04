import { CSRF_SECRET } from "@/config";
import { createToken, verifyToken, atou, utoa } from "@edge-csrf/core";

const CONFIG = {
  SALT_LENGTH: 49, // Custom number between 1 and 255
};

export async function generateCsrfToken(): Promise<string> {
  if (!CSRF_SECRET) throw new Error("CSRF_SECRET is not defined");

  const secretUint8Array = atou(CSRF_SECRET);
  const tokenUint8Arr = await createToken(secretUint8Array, CONFIG.SALT_LENGTH);
  const tokenStr = utoa(tokenUint8Arr);
  return tokenStr;
}

export async function verifyCsrfToken(token: string): Promise<boolean> {
  if (!CSRF_SECRET) throw new Error("CSRF_SECRET is not defined");

  const secretUint8Array = atou(CSRF_SECRET);
  const tokenUint8Arr = atou(token);
  const isValid = await verifyToken(tokenUint8Arr, secretUint8Array);
  return isValid;
}
