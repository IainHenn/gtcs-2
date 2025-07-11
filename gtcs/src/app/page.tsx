"use client";
import { useState } from "react";

export default function Home() {
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [campID, setCampID] = useState("");
  const [numSites, setNumSites] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [observeDate, setObserveDate] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState<string | null>(null);

  const submitInfo = () => {
    setLoading(true);
    setSuccess(null);
    fetch("http://127.0.0.1:8000/submit/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name,
        password,
        campID,
        numSites,
        startDate,
        endDate,
        observeDate,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        setSuccess("Submitted successfully!");
        setLoading(false);
      })
      .catch((err) => {
        setSuccess("Submission failed.");
        setLoading(false);
      });
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-black-100 to-black-200">
      <div className="bg-white shadow-xl p-8 border border-gray-200 rounded-2xl w-full max-w-md">
        <h1 className="text-2xl font-bold text-center mb-6 text-black">Get The Campsite(s)</h1>
        <div className="flex justify-center mb-6">
          <img src="/tent.png" alt="Tent" className="h-16 w-16" />
        </div>
        <form
          className="space-y-4"
          onSubmit={(e) => {
            e.preventDefault();
            submitInfo();
          }}
        >
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Username</label>
            <input
              className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-400 text-black"
              placeholder="Enter Username"
              value={name}
              onChange={(e) => setName(e.target.value)}
              autoComplete="username"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input
              className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-400 text-black"
              placeholder="Enter Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Campground ID</label>
            <input
              className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-400 text-black"
              placeholder="Enter Campground ID"
              type="text"
              value={campID}
              onChange={(e) => setCampID(e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1"># Of Sites (2 or less)</label>
            <input
              className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-400 text-black"
              placeholder="Enter # Of Sites"
              type="text"
              value={numSites}
              onChange={(e) => {
                const val = e.target.value.replace(/[^0-9]/g, "");
                if (val === "" || parseInt(val) <= 2) {
                  setNumSites(val);
                }
              }}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
            <input
              className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-400 text-black"
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">End Date</label>
            <input
              className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-400 text-black"
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Date To Reserve Site(s)</label>
            <input
              className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-400 text-black"
              type="datetime-local"
              value={observeDate}
              onChange={(e) => setObserveDate(e.target.value)}
            />
          </div>
          <button
            type="submit"
            className={`w-full p-2 font-semibold rounded transition-colors ${
              loading
                ? "bg-indigo-300 text-white cursor-not-allowed"
                : "bg-indigo-600 hover:bg-indigo-700 text-white"
            }`}
            disabled={loading}
          >
            {loading ? "Submitting..." : "Submit"}
          </button>
          {success && (
            <div
              className={`text-center mt-2 text-sm ${
                success === "Submitted successfully!"
                  ? "text-green-600"
                  : "text-red-600"
              }`}
            >
              {success}
            </div>
          )}
        </form>
      </div>
    </div>
  );
}
