import { useState } from "react";

function App() {
  const [pred, setPred] = useState('');
  const [err, setErr] = useState('');
  const [pathInput, setPathInput] = useState('');
  const [startInput, setStartInput] = useState('');
  const [imgSrc, setImg] = useState('');

  const onInputChange = (event) => {
    setPathInput(event.target.value);
  }

  const onStartChange = (event) => {
    setStartInput(event.target.value);
  }

  const fetchData = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8001/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({"path":pathInput, "start":startInput})
      });
      const data = await response.json();
      if (response.ok) {
        setPred(data.res);
        setImg(`data:image/png;base64,${data.image}`);
        setErr();
      } else {
        setPred();
        setImg();
        setErr(data.msg);
      }
    } catch (error) {
      console.error('Error fetching name:', error);
    }
  };


  return (
    <div class="flex items-center justify-center h-screen">
      <div class="w-full max-w-md">
      <form class="bg-gray-100 shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <div class="mb-4">
          <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" type="text" placeholder="Filepath" value={pathInput} onChange={onInputChange}></input>
        </div>
        <div class="mb-4">
          <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" type="number" placeholder="Start time" value={startInput} onChange={onStartChange} min="0" step="1"></input>
        </div>
        <div class="flex items-center justify-center">
          <button class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="button" onClick={fetchData}>
          Predict
          </button>
        </div>
      </form>
      {imgSrc && <img src={imgSrc} alt="Spectrogram" className="mb-4" />}
      {pred && <p>Predicted species: {pred}</p>}
      {err && <p>Error: {err}</p>}
      </div>
    </div>
    
  );
}

export default App;
