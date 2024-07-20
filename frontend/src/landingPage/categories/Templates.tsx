import { Button, Typography } from '@neo4j-ndl/react';
import Card from '../components/Card';
import './templates.css';
// Dark mode featured images
import StarterKitImgDark from '../../assets/img/template/StarterKitImg-dark.png';

// Light mode featured images
import StarterKitImgLight from '../../assets/img/template/StarterKitImg-light.png';

import { useContext } from 'react';
import { ThemeWrapperContext } from '../../context/ThemeWrapper';

export default function Templates() {
  const { colorMode } = useContext(ThemeWrapperContext);


  return (
    <div className='landing-home flex flex-col items-center'>
      <Typography variant='h2' className=' flex p-5'>
        <div>
          Empowering Efficient <span className='colored-text'>Data-Driven</span>
          <br />
          Decisions for <span className='colored-text'>Enterprises</span>

        </div>
      </Typography>
      <Typography variant='body-large' className='paragraph-text flex w-1/2 p-5'>
        Webify provides an intuitive platform for visualizing and accessing corporate enterprise data, streamlining
        organizational management and retrieval through GraphRAG.
      </Typography>
      <Button href='/foundation-preview'>Get started</Button>
     

    </div>
  );
}
