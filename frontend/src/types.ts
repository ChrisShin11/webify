// import { AlertColor, AlertPropsColorOverrides } from '@mui/material';
// import { AxiosResponse } from 'axios';
import { Dispatch, SetStateAction, ReactNode } from 'react';
import type { Node, Relationship } from '@neo4j-nvl/base';

export interface CustomFileBase extends Partial<globalThis.File> {
  processing: number | string;
  status: string;
  NodesCount: number;
  relationshipCount: number;
  model: string;
  fileSource: string;
  source_url?: string;
  wiki_query?: string;
  gcsBucket?: string;
  gcsBucketFolder?: string;
  errorMessage?: string;
  uploadprogess?: number;
  processingStatus?: boolean;
  google_project_id?: string;
  language?: string;
  processingProgress?: number;
  access_token?: string;
  checked?: boolean;
}
export interface CustomFile extends CustomFileBase {
  id: string;
  // total_pages: number | 'N/A';
}

export type UserCredentials = {
  uri: string;
  userName: string;
  password: string;
  database: string;
} & { [key: string]: any };

export type ChatbotProps = {
  messages: Messages[];
  setMessages: Dispatch<SetStateAction<Messages[]>>;
  isLoading: boolean;
  clear?: boolean;
  isFullScreen?: boolean;
};
export interface GraphViewModalProps {
  open: boolean;
  inspectedName?: string;
  setGraphViewOpen: Dispatch<SetStateAction<boolean>>;
  viewPoint: string;
  nodeValues?: Node[];
  relationshipValues?: Relationship[];
  selectedRows?: CustomFile[] | undefined;
}

export interface chunk {
  id: string;
  score: number;
}
export interface MessagesContextProviderProps {
  children: ReactNode;
}

export interface Messages {
  id: number;
  message: string;
  user: string;
  datetime: string;
  isTyping?: boolean;
  sources?: string[];
  model?: string;
  isLoading?: boolean;
  response_time?: number;
  chunk_ids?: chunk[];
  total_tokens?: number;
  speaking?: boolean;
  copying?: boolean;
  mode?: string;
  cypher_query?: string;
  graphonly_entities?: [];
}

export interface SideNavProps {
  isExpanded: boolean;
  position: 'left' | 'right';
  toggleDrawer: () => void;
  deleteOnClick?: () => void;
  setShowDrawerChatbot?: Dispatch<SetStateAction<boolean>>;
  showDrawerChatbot?: boolean;
  setIsRightExpanded?: Dispatch<SetStateAction<boolean>>;
  messages?: Messages[];
  clearHistoryData?: boolean;
}
