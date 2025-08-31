import { BASE_URL, API_ENDPOINT } from "@/config";

export async function POST(
  request: Request,
  { params }: { params: Promise<{ slug: string[] }> }
) {
  const { slug } = await params;
  const pathname = API_ENDPOINT + "/" + slug.join("/");
  const proxyURL = new URL(pathname, BASE_URL);
  const proxyRequest = new Request(proxyURL, request);

  try {
    return fetch(proxyRequest);
  } catch (reason) {
    const message =
      reason instanceof Error ? reason.message : "Unexpected exception";

    return new Response(message, { status: 500 });
  }
}
