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
    // <div class="container flex flex-col items-center justify-center">
    //   <input type="text" value={pathInput} onChange={onInputChange} class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="File path"></input>
    //   <button onClick={fetchData} class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 border border-green-700 rounded">Predict</button>
    //   {pred && <p>Response: {pred}</p>}
    //   {err && <p>Error: {err}</p>}
    // </div>
    <div class="flex items-center justify-center h-screen">
      <div class="w-full max-w-md">
      <form class="bg-gray-100 shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <div class="mb-4">
          <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" type="text" placeholder="Filepath" value={pathInput} onChange={onInputChange}></input>
        </div>
        <div class="flex items-center justify-center">
          <button class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="button" onClick={fetchData}>
          Predict
          </button>
        </div>
      </form>
      {pred && <p>Response: {pred}</p>}
      {err && <p>Error: {err}</p>}
      </div>
    </div>
    
  );
}

export default App;
