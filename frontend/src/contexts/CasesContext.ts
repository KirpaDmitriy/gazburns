import {createContext} from 'react';
import {CaseType} from "../mocks/cases.ts";

interface CasesContext {
    cases: CaseType[];
    setCases: (cases: CaseType[]) => void;
    loading: boolean;
    setLoading: (loading: boolean) => void;
}

export default createContext<CasesContext>({
    cases: [],
    loading: false,
    setLoading: () => {},
    setCases: () => {},
});