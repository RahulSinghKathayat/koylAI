import React, { useState } from "react";

function App() {
  const [condition, setCondition] = useState("");
  const [allergies, setAllergies] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [apiKey, setApiKey] = useState("");

  const handleSubmit = async () => {
    if (!condition || !allergies || !apiKey) {
      alert("");
      return;
    }

    setLoading(true);
    setResponse("");

    try {
      const res = await fetch("", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${apiKey}`
        },
        body: JSON.stringify({ condition, allergies })
      });

      const data = await res.json();
      setResponse(data.recommendation || "No recommendation received.");
    } catch (err) {
      console.error(err);
      setResponse("Error fetching recommendation.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white text-black flex flex-col items-center p-6">
      <h1 className="text-3xl font-bold mb-6">Koyl AI: Nutrition Advisor</h1>

      <input
        className="border p-2 mb-3 w-full max-w-md"
        type="password"
        placeholder="Enter your GROQ API Key"
        value={apiKey}
        onChange={(e) => setApiKey(e.target.value)}
      />

      <input
        className="border p-2 mb-3 w-full max-w-md"
        placeholder="Enter patient condition(s)"
        value={condition}
        onChange={(e) => setCondition(e.target.value)}
      />

      <input
        className="border p-2 mb-3 w-full max-w-md"
        placeholder="Enter allergy profile"
        value={allergies}
        onChange={(e) => setAllergies(e.target.value)}
      />

      <button
        className="bg-blue-600 text-white px-6 py-2 rounded"
        onClick={handleSubmit}
        disabled={loading}
      >
        {loading ? "Loading..." : "Get Dietary Recommendations"}
      </button>

      <div className="mt-6 w-full max-w-2xl bg-gray-100 p-4 rounded">
        <h2 className="font-semibold mb-2">Dietary Recommendation:</h2>
        <pre>{response}</pre>
      </div>
    </div>
  );
}

export default App;
