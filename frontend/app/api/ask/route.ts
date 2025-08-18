// Optional proxy route for Next.js API if deploying frontend+backend together
// This file can be left empty or used to forward requests to the backend
export async function POST(req: Request) {
  // Example: forward to backend
  // const body = await req.json();
  // const res = await fetch("http://backend:5000/ask", { method: "POST", body: JSON.stringify(body), headers: { "Content-Type": "application/json" } });
  // const data = await res.json();
  // return new Response(JSON.stringify(data), { status: 200 });
  return new Response(JSON.stringify({ ok: true, note: "Proxy not implemented. Use direct backend URL." }), { status: 200 });
}
