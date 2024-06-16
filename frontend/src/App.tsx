import './App.css'
import HomePage from "./pages/HomePage/HomePage.tsx";
import {BrowserRouter, Route, Routes} from "react-router-dom";
import CasePage from "./pages/CasePage/CasePage.tsx";
import {ConfigProvider} from "antd";
import './assets/embla.css';
import LoginPage from "./pages/LoginPage/LoginPage.tsx";
import PrivateRoute from "./ui/PrivateRoute/PrivateRoute.tsx";
import UserProvider from "./contexts/UserContextProvider.tsx";
import NotFoundPage from "./pages/NotFoundPage/NotFoundPage.tsx";
import CasesProvider from "./contexts/CasesContextProvider.tsx";

function App() {

    return (
        <div className="app">
            <ConfigProvider theme={{token: {colorPrimary: '#4F6AE8',}}}>
                <CasesProvider>
                    <UserProvider>
                        <BrowserRouter>
                            <Routes>
                                <Route path="/" element={<PrivateRoute/>}>
                                    <Route path="home" element={<HomePage/>}/>
                                    <Route path="case/:caseId" element={<CasePage/>}/>
                                </Route>
                                <Route path="login" element={<LoginPage/>}/>
                                <Route path='*' element={<NotFoundPage/>}/>
                            </Routes>
                        </BrowserRouter>
                    </UserProvider>
                </CasesProvider>
            </ConfigProvider>
        </div>
    )
}

export default App
