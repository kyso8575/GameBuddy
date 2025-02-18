import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import "./App.css";
import { Sidebar } from "./layout";
import { AllNotes, ArchiveNotes } from "./pages";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Sidebar />
        <div className="app_container">
          <Routes>
            <Route path="/" element = {<AllNotes />}></Route>
            <Route path="/archive" element = {<ArchiveNotes />}></Route>
            <Route path="/*" element = {<Navigate to={"/404"} />}></Route>
          </Routes>
        </div>
      </BrowserRouter>
    </div>
  );
}

export default App;
