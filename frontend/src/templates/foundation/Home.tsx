import Header from '../shared/components/Header';
import PageLayout from './Layout/PageLayout';

export default function Home() {
  return (
    <div>
      <Header title={'Webify'} navItems={[]} useNeo4jConnect={false} userHeader={true} />
      <PageLayout />
    </div>
  );
}
