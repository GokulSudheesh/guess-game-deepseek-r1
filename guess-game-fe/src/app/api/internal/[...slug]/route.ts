import { BASE_URL, API_ENDPOINT } from "@/config";

async function handleRequest(request: Request) {
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
