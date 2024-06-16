export interface Meta {
    audience: string;
    product: string;
    gender: string;
    ageFrom: number;
    ageTo: number;
    salaryFrom: number;
    salaryTo: number;
    width: number;
    height: number;
}

export interface Generation {
    id: number;
    src: string;
    title: string;
    subtitle: string;
}

export interface CaseType {
    id: string;
    images: Generation[];
    meta_information: Meta;
}

export const casesMock: CaseType[] = [
    {
        id: 1,
        images: [
            {
                id: 1,
                src: 'https://steamuserimages-a.akamaihd.net/ugc/862857581989807965/89518896478AB5FC4C81035678DB2B441ACE107A/?imw=512&imh=384&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true',
                title: '1',
                subtitle: 'Lorem ipsum dolor',
            },
            {
                id: 2,
                src: 'https://steamuserimages-a.akamaihd.net/ugc/862857581989807965/89518896478AB5FC4C81035678DB2B441ACE107A/?imw=512&imh=384&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true',
                title: '2',
                subtitle: 'Lorem ipsum dolor',
            },
            {
                id: 3,
                src: 'https://steamuserimages-a.akamaihd.net/ugc/862857581989807965/89518896478AB5FC4C81035678DB2B441ACE107A/?imw=512&imh=384&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true',
                title: '3',
                subtitle: 'Lorem ipsum dolor',
            },
        ],
        meta_information: {
            audience: 'audience',
            product: 'product',
            width: 1024,
            height: 1024,
        },
    },
    {
        id: 2,
        images: [
            {
                id: 1,
                src: 'https://frankmedia.ru/wp-content/uploads/2021/09/63e8cdb3b120.jpeg',
                title: '2',
                subtitle: 'Lorem ipsum dolor',
            },
        ],
        meta_information: {
            audience: 'audience',
            product: 'product',
            width: 1024,
            height: 1024,
        }
    },
    {
        id: 3,
        images: [
            {
                id: 1,
                src: 'https://steamuserimages-a.akamaihd.net/ugc/862857581989807965/89518896478AB5FC4C81035678DB2B441ACE107A/?imw=512&imh=384&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true',
                title: '3',
                subtitle: 'Lorem ipsum dolor',
            },
        ],
        meta_information: {
            audience: 'audience',
            product: 'product',
            width: 1024,
            height: 1024,
        }
    },
    {
        id: 4,
        images: [
            {
                id: 1,
                src: 'https://steamuserimages-a.akamaihd.net/ugc/862857581989807965/89518896478AB5FC4C81035678DB2B441ACE107A/?imw=512&imh=384&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true',
                title: '4',
                subtitle: 'Lorem ipsum dolor',
            },
        ],
        meta_information: {
            audience: 'audience',
            product: 'product',
            width: 1024,
            height: 1024,
        }
    },
]