import { AlertColor, AlertPropsColorOverrides } from '@mui/material';
import { AxiosResponse } from 'axios';
import { Dispatch, SetStateAction, ReactNode } from 'react';
import type { Node, Relationship } from '@neo4j-nvl/base';
import { OverridableStringUnion } from '@mui/types';

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
export interface OptionType {
  readonly value: string;
  readonly label: string;
}

export interface SourceNode {
  fileName: string;
  fileSize: number;
  fileType: string;
  nodeCount?: number;
  processingTime?: string;
  relationshipCount?: number;
  model: string;
  status: string;
  url?: string;
  awsAccessKeyId?: string;
  fileSource: string;
  gcsBucket?: string;
  gcsBucketFolder?: string;
  errorMessage?: string;
  uploadprogress?: number;
  gcsProjectId?: string;
  language?: string;
  processed_chunk?: number;
  total_chunks?: number;
  // total_pages?: number;
  access_token?: string;
}

export type GraphType = 'Document' | 'Entities' | 'Chunk';

export interface CustomAlertProps {
  open: boolean;
  handleClose: () => void;
  alertMessage: string;
  severity?: OverridableStringUnion<AlertColor, AlertPropsColorOverrides> | undefined;
}

export type UserCredentials = {
  uri: string;
  userName: string;
  password: string;
  database: string;
} & { [key: string]: any };

export interface FileContextProviderProps {
  children: ReactNode;
}
export interface PollingAPI_Response extends Partial<AxiosResponse> {
  data: statusupdate;
}
export interface SourceListServerData {
  data: SourceNode[];
  status: string;
  error?: string;
  message?: string;
}

export interface labelsAndTypes {
  labels: string[];
  relationshipTypes: string[];
}

export interface orphanNode {
  id: string;
  elementId: string;
  description: string;
  labels: string[];
  embedding: null | string;
}

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

export interface orphanNodeProps {
  documents: string[];
  chunkConnections: number;
  e: orphanNode;
  checked?: boolean;
}
interface orphanTotalNodes {
  total: number;
}
export interface uploadData {
  file_size: number;
  // total_pages: number;
  file_name: string;
  message: string;
}


export interface fileStatus {
  fileName: string;
  status: string;
  processingTime?: number;
  nodeCount?: number;
  relationshipCount?: number;
  model: string;
  total_chunks?: number;
  // total_pages?: number;
  processed_chunk?: number;
}

export interface commonserverresponse {
  status: string;
  error?: string;
  message?: string | orphanTotalNodes;
  file_name?: string;
  data?: labelsAndTypes | labelsAndTypes[] | uploadData | orphanNodeProps[];
}

export interface chunk {
  id: string;
  score: number;
}
export interface MessagesContextProviderProps {
  children: ReactNode;
}

export interface eventResponsetypes {
  fileName: string;
  status: string;
  processingTime: number;
  nodeCount: number;
  relationshipCount: number;
  model: string;
  total_chunks: number | null;
  // total_pages: number;
  fileSize: number;
  processed_chunk?: number;
  fileSource: string;
}

export interface FileTableProps {
  isExpanded: boolean;
  connectionStatus: boolean;
  setConnectionStatus: Dispatch<SetStateAction<boolean>>;
  onInspect: (id: string) => void;
}
export type alertStateType = {
  showAlert: boolean;
  alertType: OverridableStringUnion<AlertColor, AlertPropsColorOverrides> | undefined;
  alertMessage: string;
};

export interface statusupdate {
  status: string;
  message: string;
  file_name: fileStatus;
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
