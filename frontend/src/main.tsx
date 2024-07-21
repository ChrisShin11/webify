import './polyfill-process.ts'
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.tsx';
import './index.css';
import '@neo4j-ndl/base/lib/neo4j-ds-styles.css';
import { FileContextProvider } from './context/UserFiles.tsx';


ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <FileContextProvider>


    <App />
    </FileContextProvider>
  </React.StrictMode>
);
