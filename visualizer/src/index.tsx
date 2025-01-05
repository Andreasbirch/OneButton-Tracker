import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import FileUpload from './FileUpload';
import Calendar from './components/calendar/Calendar';
import { Scope } from './models/enums';
const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  // <React.StrictMode>
  <>
    <App />
    <Calendar/>
  </>
  // </React.StrictMode>
);