import { BASE_URL, API_ENDPOINT, CSRF_TOKEN_COOKIE } from "@/config";
import { verifyCsrfToken } from "@/lib/csrf-token";
import { cookies } from "next/headers";

async function handleRequest(request: Request) {
  const cookieStore = await cookies();
  const csrfToken = cookieStore.get(CSRF_TOKEN_COOKIE)?.value;
  const isValid = csrfToken && (await verifyCsrfToken(csrfToken));
  if (!isValid) return new Response("Invalid CSRF Token", { status: 403 });

  const pathname = request.url.split("/internal/")[1];
  const url = API_ENDPOINT + "/" + pathname;
  const proxyURL = new URL(url, BASE_URL);
  const proxyRequest = new Request(proxyURL, request);

  try {
    return fetch(proxyRequest);
  } catch (reason) {
    const message =
      reason instanceof Error ? reason.message : "Unexpected exception";

    return new Response(message, { status: 500 });
  }
}

export async function POST(request: Request) {
  return handleRequest(request);
}

export async function GET(request: Request) {
  return handleRequest(request);
}
