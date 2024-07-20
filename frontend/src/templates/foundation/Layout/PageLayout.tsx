import SideNav from './SideNav';
import Content from '../Content';
import messagesData from '../../shared/assets/ChatbotMessages.json';
import ChatbotSideNav from './ChatbotSideNav';
import { useState } from 'react';
import DrawerChatbot from '../../shared/components/DrawerChatbot';



export default function PageLayout() {
  const messages = messagesData.listMessages
  const [isRightExpanded, setIsRightExpanded] = useState<boolean>(true);
  const [clearHistoryData, setClearHistoryData] = useState<boolean>(false);
  const [showDrawerChatbot, setShowDrawerChatbot] = useState<boolean>(true);




  const toggleRightDrawer = () => setIsRightExpanded(!isRightExpanded);
  const deleteOnClick = async () => {
    try {
      setClearHistoryData(true);
      setClearHistoryData(false);
    } catch (error) {
      console.log(error);
      setClearHistoryData(false);
    }
  };

  return (
    <div className='h-[calc(100vh-58px)] w-full flex'>
      <SideNav />
      <Content />

      {showDrawerChatbot && (
        <DrawerChatbot messages={messages} isExpanded={isRightExpanded} clearHistoryData={clearHistoryData} />
      )}
      <ChatbotSideNav 
       messages={messages}
       isExpanded={isRightExpanded}
       position='right'
       toggleDrawer={toggleRightDrawer}
      //  deleteOnClick={deleteOnClick}
       showDrawerChatbot={showDrawerChatbot}
      //  setShowDrawerChatbot={setShowDrawerChatbot}
       setIsRightExpanded={setIsRightExpanded}
       clearHistoryData={clearHistoryData}
      />
      {/* <Chatbot messages={messages} /> */}
    </div>
  );
}
