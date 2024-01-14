import React, { useRef } from 'react'

import MainBody from './MainBody'
import AboutModel from './AboutModel'
import HowitWorks from './HowitWorks'
import Model from './Model'
import Footer from './Footer'


function Home({modelRef, scrolltarget}) {

  return (
    <div class="dark">
      <MainBody scrolltarget={scrolltarget}/>
      <AboutModel />
      <HowitWorks />
      <Model modelRef={modelRef}/>
      <Footer />
    </div>
  )
}

export default Home