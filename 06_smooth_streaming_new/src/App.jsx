import { useState } from "react";
import "./App.css";

function App() {
  const [sound, setSound] = useState("");
  const [where, setWhere] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();

    setSuggestions([]);
    setLoading(true);

    const ws = new WebSocket(
      `ws://localhost:8000/search?sound=${sound}&location=${where}`
    );
    ws.onmessage = (event) => {
      console.log(event.data);
      setSuggestions((prevSuggestions) => {
        const newSuggestion = JSON.parse(event.data);

        // Try to find existing Suggestion with same label
        const existingSuggestionIndex = prevSuggestions.findIndex(
          (s) => s.label === newSuggestion.label
        );

        // Copy the previous suggestions to return a new list
        const newSuggestions = prevSuggestions.slice();

        if (existingSuggestionIndex === -1) {
          // Not found, add new suggestion to list
          // Move description_delta into description
          newSuggestions.push({
            ...newSuggestion,
            description: newSuggestion.description_delta,
          });
        } else {
          // Found existing suggestion, so update it
          // Replace suggestion by taking the old one and
          // adding the description_delta to the description
          newSuggestions[existingSuggestionIndex] = {
            ...newSuggestions[existingSuggestionIndex],
            description:
              newSuggestions[existingSuggestionIndex].description +
              newSuggestion.description_delta,
          };
        }

        return newSuggestions;
      });
    };

    ws.onclose = (event) => {
      setLoading(false);
    };
  };
  return (
    <>
      <h1>Car Sound Troubleshooter</h1>
      <form onSubmit={handleSubmit} className="form">
        <label htmlFor="sound" className="label">
          Sound
        </label>
        <input
          id="sound"
          type="text"
          value={sound}
          onChange={(e) => setSound(e.target.value)}
          className="input"
        />

        <label htmlFor="where" className="label">
          Location
        </label>
        <input
          id="where"
          type="text"
          value={where}
          onChange={(e) => setWhere(e.target.value)}
          className="input"
        />

        <input type="submit" value="Submit" className="submit" />
      </form>

      {loading ? <p>Loading...</p> : <p>&nbsp;</p>}

      {suggestions.map((suggestion, index) => (
        <div key={index} className="suggestion">
          <h1 className="suggestion-label">{suggestion.label}</h1>
          <p className="suggestion-description">{suggestion.description}</p>
        </div>
      ))}
    </>
  );
}

export default App;
