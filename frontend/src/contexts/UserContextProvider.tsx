import UserContext from './UserContext.ts';
import {FC, ReactNode, useEffect, useState} from "react";

interface Props {
    children: ReactNode;
}

const UserProvider: FC<Props> = ({ children }) => {
    const [token, setToken] = useState('');
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (!token) setToken(localStorage.getItem('access_token') || '');
    });

    return (
        <UserContext.Provider value={{ token, setToken, loading, setLoading }}>
            {children}
        </UserContext.Provider>
    );
};

export default UserProvider;