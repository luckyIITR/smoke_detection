import React, { useRef } from 'react'
import Navbar from './Navbar'
import MainBody from './MainBody'
import AboutModel from './AboutModel'
import HowitWorks from './HowitWorks'
import Model from './Model'
import Footer from './Footer'


function Home() {
  const targetRef = useRef(null);

  const scrollToElement = () => {
    if (targetRef.current) {
      const elementTop = targetRef.current.offsetTop;
      const scrollStep = (elementTop - window.scrollY) / 15;

      const scrollInterval = setInterval(() => {
        if (window.scrollY < elementTop) {
          window.scrollBy(0, scrollStep);
        } else {
          clearInterval(scrollInterval);
        }
      }, 30);
    }
  };
  return (
    <div class="dark">
      <Navbar scrollToElement = {scrollToElement}/>
      <MainBody scrollToElement = {scrollToElement}/>
      <AboutModel />
      <HowitWorks />
      <Model targetRef={targetRef}/>
      <Footer />
    </div>
  )
}

export default Home