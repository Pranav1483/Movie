import { BrowserRouter, Routes, Route } from "react-router-dom"
import LoginPage from "./pages/Login";
import DashboardPage from "./pages/DashBoard";
import SearchPage from "./pages/Search";
import ViewPage from "./pages/View";
import LikesPage from "./pages/Likes";
import WatchListPage from "./pages/WatchList";
import WatchedPage from "./pages/Watched";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage/>}/>
        <Route path="/" element={<DashboardPage/>}/>
        <Route path="/search" element={<SearchPage/>}/>
        <Route path="/watch" element={<ViewPage/>}/>
        <Route path="/likes" element={<LikesPage/>}/>
        <Route path="/watchlist" element={<WatchListPage/>}/>
        <Route path="/watched" element={<WatchedPage/>}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
