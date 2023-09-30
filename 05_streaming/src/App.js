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
        // A new list, which is the old list plus the new suggestion
        return [...prevSuggestions, JSON.parse(event.data)];
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
