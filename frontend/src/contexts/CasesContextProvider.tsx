import {FC, ReactNode, useState} from "react";
import CasesContext from "./CasesContext.ts";
import {CaseType} from "../mocks/cases.ts";

interface Props {
    children: ReactNode;
}

const CasesProvider: FC<Props> = ({ children }) => {
    const [cases, setCases] = useState<CaseType[]>([]);
    const [loading, setLoading] = useState<boolean>(false);

    return (
        <CasesContext.Provider value={{ cases, setCases, loading, setLoading }}>
            {children}
        </CasesContext.Provider>
    );
};

export default CasesProvider;