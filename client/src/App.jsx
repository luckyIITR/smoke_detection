import './App.css'
import { useRef } from 'react'
import { Provider } from 'react-redux';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from './components/Home';
import store from './store';
import AboutMe from './components/AboutMe';
import Navbar from './components/Navbar';
import Alert from './components/Alert';

function App() {
  const modelRef = useRef(null);
  const scrolltarget = () => {
    if (modelRef.current) {
      modelRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <Provider store={store} >
      <BrowserRouter >
        <Navbar scrolltarget={scrolltarget} />
        <Alert />
        <Routes >
          <Route path='/about-me' element={<AboutMe />} />
          <Route path='/' element={<Home modelRef={modelRef} scrolltarget={scrolltarget} />} />
        </Routes>
      </BrowserRouter>
    </Provider>
  )
}

export default App
