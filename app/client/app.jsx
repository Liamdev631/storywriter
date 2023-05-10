import React, { useEffect, useState } from 'react';

function App() {
  const [data, setData] = useState('');

  useEffect(() => {
    // Fetch the data from the Flask server
    fetch('http://localhost:5000/api/data')
      .then(response => response.json())
      .then(data => setData(data.data));
  }, []);

  return (
    <div className="App">
      <h1>My App</h1>
      <p>{data}</p>
    </div>
  );
}

export default App;
