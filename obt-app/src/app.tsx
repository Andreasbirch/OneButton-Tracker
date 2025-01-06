import ReactDOM from 'react-dom/client';
import './index.css';
import Devices from './devices';
// import FileUpload from './FileUpload';
// import Calendar from './components/calendar/Calendar';
// import { Scope } from './models/enums';


declare global {
  interface Window {
    electron: any;
  }
}

const root = ReactDOM.createRoot(
  document.getElementById('app') as HTMLElement
);

root.render(
  // <React.StrictMode>
  <>
    <h1>React content</h1>
    <Devices></Devices>
    {/* <Calendar/> */}
  </>
  // </React.StrictMode>
);