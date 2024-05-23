import { useState } from "react";

function App() {
  const [pred, setPred] = useState('');
  const [err, setErr] = useState('');
  const [pathInput, setPathInput] = useState('');

  const onInputChange = (event) => {
    setPathInput(event.target.value);
  }

  const fetchData = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8001/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({"path":pathInput})
      });
      const data = await response.json();
      if (response.ok) {
        setPred(data.res);
        setErr();
      } else {
        setErr(data.msg);
      }
    } catch (error) {
      console.error('Error fetching name:', error);
    }
  };


  return (
    <div>
      <input type="text" value={pathInput} onChange={onInputChange} size="50"></input><br></br>
      <button onClick={fetchData}>Predict</button>
      {pred && <p>Response: {pred}</p>}
      {err && <p>Error: {err}</p>}
    </div>
  );
}

export default App;
