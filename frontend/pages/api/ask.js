export default async function handler(req, res) {
  if (req.method === 'POST') {
    // Forward to backend Flask API
    const response = await fetch('http://localhost:5000/api/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req.body),
    });
    const data = await response.json();
    res.status(200).json(data);
  } else {
    res.status(405).end();
  }
}
