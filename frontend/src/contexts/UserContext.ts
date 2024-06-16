import { createContext } from 'react';

interface UserContext {
    token: string;
    loading: boolean;
    setToken: (token: string) => void;
    setLoading: (val: boolean) => void;
}

// Создаём контекст и задаем значения по умолчанию для него
export default createContext<UserContext>({
    token: '',
    setToken: () => {},
    loading: false,
    setLoading: () => {},
});