import { Typography } from '@neo4j-ndl/react';
import Card from '../components/Card';

// Dark mode featured images
import StarterKitImgDark from '../../assets/img/template/StarterKitImg-dark.png';

// Light mode featured images
import StarterKitImgLight from '../../assets/img/template/StarterKitImg-light.png';


import { useContext } from 'react';
import { ThemeWrapperContext } from '../../context/ThemeWrapper';

export default function Templates() {
  const { colorMode } = useContext(ThemeWrapperContext);

  const templatesCards = [
    {
      title: 'Foundation Template',
      description:
        'The Foundation template, because we all starts somewhere, this was the first template we created, combining simple, modern and UX all together for a generic application design.',
      image: colorMode === 'dark' ? StarterKitImgDark : StarterKitImgLight,
      sourceCode: `https://github.com/neo4j-labs/neo4j-needle-starterkit/blob/${
        import.meta.env.PACKAGE_VERSION
      }/src/templates/foundation`,
      previewLink: '/foundation-preview',
    },
  ];

  return (
    <div className='flex flex-col items-center'>
      <Typography variant='h2' className='flex p-5'>
        Landing Page
      </Typography>
      <Typography variant='body-large' className='flex p-5'>
        Write a brief description of what Webify is here.
      </Typography>
      <div className='flex flex-wrap justify-center gap-x-14 gap-y-10 md:grid md:grid-cols-3 md:gap-x-14 md:gap-y-10'>
        {templatesCards.map((card, index) => (
          <div key={index} className='w-full md:w-auto'>
            <Card
              title={card.title}
              description={card.description}
              image={card.image}
              sourceCode={card.sourceCode}
              previewLink={card.previewLink}
            />
          </div>
        ))}
      </div>
    </div>
  );
}
