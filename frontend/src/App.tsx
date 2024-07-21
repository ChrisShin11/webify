import { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import '@neo4j-ndl/base/lib/neo4j-ds-styles.css';

import ThemeWrapper from './context/ThemeWrapper';

import Home from './landingPage/Home';
import PageNotFound from './templates/shared/components/PageNotFound';

import Foundation from './templates/foundation/Home';
import Cybersecurity from './templates/cybersecurity/Home';
import Movie from './templates/movie/Home';

import Chatbot from './templates/shared/components/Chatbot';
import messagesData from './templates/shared/assets/ChatbotMessages.json';
import ConnectionModal from './templates/shared/components/ConnectionModal';
import Header from './templates/shared/components/Header';
import User from './templates/shared/components/User';

import { FileContextProvider } from './context/connectionFile';

import './ConnectionModal.css';
import FileTable from './templates/shared/components/FileTable';
import { FileTableProps } from './types';

function App() {
  const messages = messagesData.listMessages;
  const [activeTab, setActiveTab] = useState<string>('Home');
  const [isExpanded, setIsExpanded] = useState<boolean>(false);
  const [connectionStatus, setConnectionStatus] = useState<boolean>(true);

  const onInspect = (fileName: string) => {
    console.log('inspect file: ', fileName);
  };

  const fileTableProps: FileTableProps = {
    isExpanded,
    connectionStatus,
    setConnectionStatus,
    onInspect,
  }
  return (
    <BrowserRouter>
      <ThemeWrapper>
        <Routes>
          <Route path='/' element={<Home />} />
          <Route path='/foundation-preview' element={<Foundation />} />
          <Route path='/movie-preview' element={<Movie />} />
          <Route path='/cybersecurity-preview' element={<Cybersecurity />} />
          <Route
            path='/connection-modal-preview'
            element={
              <FileContextProvider>
                <ConnectionModal open={true} setOpenConnection={() => null} setConnectionStatus={() => null} />
              </FileContextProvider>
            }
          />
          <Route path='/chat-widget-preview' element={<Chatbot messages={messages} />} />
          <Route path='/file' element={<FileTable {...fileTableProps} />} /> 
          <Route
            path='/header-preview'
            element={
              <Header
                title='Header Component'
                navItems={['Home', 'Tab1', 'TabX']}
                useNeo4jConnect={false}
                activeNavItem={activeTab}
                setActiveNavItem={setActiveTab}
              />
            }
          />
          <Route path='/user-preview' element={<User />} />
          <Route path='*' element={<PageNotFound />} />
        </Routes>
      </ThemeWrapper>
    </BrowserRouter>
  );
}

export default App;
