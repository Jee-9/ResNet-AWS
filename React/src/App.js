import './App.css';
import { useEffect, useState } from 'react';
import { lambdaApi } from './api';
import Button from '@mui/material/Button';

import ReactPlayer from 'react-player';

const App = () => {
  console.log('hihie');
  const [urlArr, setUrlArr] = useState([]);

  useEffect(() => {
    lambdaApi.getData('user-1').then(resp => {
      setUrlArr(Object.entries(resp.data));
  })}, []);

  console.log('urlArr', urlArr);

  return (
    <>
    <div>
      {urlArr.map(urlKeyValue => (
        <a key={urlKeyValue[0]} href={urlKeyValue[1]}>
          <ReactPlayer url = {urlKeyValue[1]}/>
        </a>
      ))}
    </div>
    </>
  );
}

export default App;
