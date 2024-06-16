import styles from './style.module.css';
import {Link, useNavigate, useParams} from 'react-router-dom';
import {Breadcrumb, Button, Flex, Form, InputNumber, notification, Select, Spin, Steps} from "antd";
import {useContext, useEffect, useState} from "react";
import TextArea from "antd/es/input/TextArea";
import {Carousel} from "../../ui/Carousel/Carousel.tsx";
import {CaseType} from "../../mocks/cases.ts";
import CasesContext from "../../contexts/CasesContext.ts";
import {genderOptions, segmentOptions} from "../../assets/options.ts";
import {useForm} from "antd/lib/form/Form";
import {instance} from "../../services/api.config.ts";

interface ICaseForm {
    segment?: string[];
    audience?: string;
    product?: string;
    ageFrom?: string;
    ageTo?: string;
    gender?: string;
    salaryFrom?: string;
    salaryTo?: string;
    title?: string;
    subtitle?: string;
    size: number;
}

const options = [
    {
        id: 1,
        height: 1024,
        width: 1024,
        name: "Квадрат"
    },
    {
        id: 2,
        height: 900,
        width: 1600,
        name: "Web"
    },
    {
        id: 3,
        height: 200,
        width: 500,
        name: "Mobile"
    },
    {
        id: 3,
        height: 400,
        width: 1000,
        name: "Mobile 2"
    },
    {
        id: 3,
        height: 300,
        width: 900,
        name: "Mobile 3"
    },
];

const steps = [
    {
        title: 'Запрос',
        content: 'First-content',
    },
    {
        title: 'Контент',
        content: 'Second-content',
    },
];

const CasePage = () => {
    const {cases, loading, setCases, setLoading} = useContext(CasesContext);
    const {caseId} = useParams();
    const stepItems = steps.map((item) => ({key: item.title, title: item.title}));
    const [step, setStep] = useState(0);
    const currentCase = cases.find(item => item.id === caseId);
    const [selectedIndex, setSelectedIndex] = useState(0);
    const [title, setTitle] = useState(currentCase?.images[selectedIndex]?.title);
    const [subtitle, setSubtitle] = useState(currentCase?.images[selectedIndex]?.subtitle);
    const [form] = useForm<ICaseForm>();
    const navigate = useNavigate();

    useEffect(() => {
        if (currentCase) {
            form.setFieldsValue({
                audience: currentCase.meta_information.audience,
                product: currentCase.meta_information.product,
                gender: currentCase.meta_information.gender,
                salaryFrom: currentCase.meta_information.salaryFrom?.toString?.(),
                salaryTo: currentCase.meta_information.salaryTo?.toString?.(),
                ageFrom: currentCase.meta_information.ageFrom?.toString?.(),
                ageTo: currentCase.meta_information.ageTo?.toString?.(),
                size: options.findIndex(it => it.height === currentCase.meta_information?.height && it.width === currentCase.meta_information?.width),
            });
            setStep(1);
        }
    }, [currentCase]);

    useEffect(() => {
        console.log(selectedIndex);
        if (currentCase) {
            form.setFieldValue('subtitle', currentCase.images[selectedIndex]?.subtitle);
            form.setFieldValue('title', currentCase.images[selectedIndex]?.title);
        }
    }, [selectedIndex]);

    const onFinish = ({
                          segment = [],
                          audience = '',
                          ageFrom = '',
                          ageTo = '',
                          product = '',
                          gender = '',
                          salaryFrom = '',
                          salaryTo = '',
                          subtitle = '',
                          title = '',
                          size = 0,
                      }: ICaseForm) => {
        // console.log({audience, ageTo, ageFrom, salaryFrom, salaryTo, title, subtitle, product, gender});
        setLoading(true);
        if (!step) {
            instance.post<CaseType>('generate', {
                segment,
                audience,
                ageTo,
                ageFrom,
                salaryFrom,
                salaryTo,
                gender,
                product,
                height: options[size].height,
                width: options[size].width,
            }).then((response) => {
                setCases([...cases, response.data]);
                next();
                navigate('/case/' + response.data.id, { replace: true });
            }).catch(() => {
                notification.error({message: 'Произошла ошибка на стороне сервера'})
            }).finally(() => setLoading(false));
        }
        else instance.post<CaseType>('add_text', {
            case_id: currentCase?.id,
            picture_id: currentCase?.images[selectedIndex].id,
            title,
            subtitle
        }).then((response) => {
            setCases(cases.map(it => it.id === response.data.id ? {...response.data, images: response.data.images} : it));
            setSelectedIndex(currentCase ? currentCase.images.length - 1 : 0);
        }).catch(() => {
            notification.error({message: 'Произошла ошибка на стороне сервера'})
        }).finally(() => setLoading(false));
    }

    const handleChangeFrom = (val: number) => {
        form.setFieldValue('ageFrom', val > form.getFieldValue("ageTo") ? form.getFieldValue("ageTo") : val);
    };

    const handleChangeTo = (val: number) => {
        form.setFieldValue('ageTo', val < form.getFieldValue("ageFrom") ? form.getFieldValue("ageFrom") : val);
    };
    const handleChangeSalaryFrom = (val: number) => {
        form.setFieldValue('salaryFrom', val > form.getFieldValue("salaryTo") ? form.getFieldValue("salaryTo") : val);
    };

    const handleChangeSalaryTo = (val: number) => {
        form.setFieldValue('salaryTo', val < form.getFieldValue("salaryFrom") ? form.getFieldValue("salaryFrom") : val);
    };

    // const handleGenText = () => {
    //     setLoading(true);
    //     instance.get("generate_text?case_id=" + currentCase?.id).then((response) => {
    //         form.setFieldValue("title", response.data.title);
    //         form.setFieldValue("subtitle", response.data.subtitle);
    //     }).catch(() => {
    //         notification.error({message: 'Произошла ошибка на стороне сервера'})
    //     }).finally(() => setLoading(false));
    // };

    const handleRegenerate = () => {
        setLoading(true);
        instance.post("regenerate", {
            case_id: currentCase?.id,
        }).then((response) => {
            setCases(cases.map(it => it.id === response.data.id ? {...response.data, images: response.data.images} : it));
            setSelectedIndex(currentCase ? currentCase.images.length - 1 : 0);
        }).catch(() => {
            notification.error({message: 'Произошла ошибка на стороне сервера'})
        }).finally(() => setLoading(false));
    };

    const handleClearText = () => {
        setLoading(true);
        instance.post<CaseType>('add_text', {
            case_id: currentCase?.id,
            picture_id: currentCase?.images[selectedIndex].id,
            title: "",
            subtitle: "",
        }).then((response) => {
            setCases(cases.map(it => it.id === response.data.id ? {...response.data, images: response.data.images} : it));
            setSelectedIndex(currentCase ? currentCase.images.length - 1 : 0);
        }).catch(() => {
            notification.error({message: 'Произошла ошибка на стороне сервера'})
        }).finally(() => setLoading(false));
    };

    const next = () => setStep(step + 1);
    const round = (x: number, y: number) => (x / y === Math.round(x / y)) ? x / y : (x / y).toFixed(1);

    return loading ? (
        <div className={styles.loading}>
            <Spin/>
            <span>Пожалуйста, подождите.</span>
            <span>Обычно генерация занимает не больше 20 секунд.</span>
        </div>
    ) : (
        <div className={styles.container}>
            <Breadcrumb
                className={styles.link}
                items={[
                    {
                        title: <Link to={'/home'}>Главная</Link>,
                    },
                    {
                        title: 'Генерация',
                    },
                ]}
            />
            <div className={styles.formWrapper}>
                <Steps type="navigation" current={step} items={stepItems} onChange={(val) => setStep(val)} className={styles.step} size="small"/>
                <Form className={styles.form} onFinish={onFinish} layout='vertical' form={form}>
                    {!step ? (
                        <>
                            <Form.Item label='Описание пользователя'>
                                <Form.Item name="segment" label='Сегмент' rules={[{required: true, message: 'Пожалуйста, выберите сегменты'}]}>
                                    <Select
                                        mode="multiple"
                                        allowClear
                                        style={{width: '100%'}}
                                        placeholder="Сегмент пользователей"
                                        options={segmentOptions}
                                        disabled={!!currentCase?.id}
                                    />
                                </Form.Item>
                                <Form.Item label='Возраст'>
                                    <Flex justify='space-between'>
                                        <Form.Item name="ageFrom" style={{margin: 0}}>
                                            <InputNumber min={14} max={99} onChange={handleChangeFrom} placeholder="От"
                                                         style={{width: '95%'}} disabled={!!currentCase?.id}/>
                                        </Form.Item>
                                        <Form.Item name="ageTo" style={{margin: 0}}>
                                            <InputNumber min={14} max={99} onChange={handleChangeTo} placeholder="До"
                                                         style={{width: '95%'}} disabled={!!currentCase?.id}/>
                                        </Form.Item>
                                    </Flex>
                                </Form.Item>
                                <Form.Item name="gender">
                                    <Select
                                        allowClear
                                        style={{width: '100%'}}
                                        defaultActiveFirstOption
                                        placeholder="Пол"
                                        options={genderOptions}
                                        disabled={!!currentCase?.id}
                                    />
                                </Form.Item>
                                <Form.Item name="salaryFrom" label="Сумма зарплатных поступлений за 12 месяцев (тыс. р.)" rules={[{required: true, message: 'Пожалуйста, введите сумму поступлений'}]}>
                                    <Flex justify='space-between'>
                                        <Form.Item name="salaryFrom" style={{margin: 0}}>
                                            <InputNumber min={1} max={500000} onChange={handleChangeSalaryFrom} placeholder="От" style={{width: '95%'}} disabled={!!currentCase?.id}/>
                                        </Form.Item>
                                        <Form.Item name="salaryTo" style={{margin: 0}}>
                                            <InputNumber min={1} max={500000} onChange={handleChangeSalaryTo} placeholder="До" style={{width: '95%'}} disabled={!!currentCase?.id}/>
                                        </Form.Item>
                                    </Flex>
                                </Form.Item>
                                <Form.Item name="audience" style={{margin: 0}}>
                                    <TextArea className={styles.text} placeholder="Дополнительное описание" disabled={!!currentCase?.id}/>
                                </Form.Item>
                            </Form.Item>
                            <Form.Item name="product" label='Описание продукта' rules={[{required: true}]}>
                                <TextArea className={styles.text} placeholder="Опишите продукт: что продаем?" disabled={!!currentCase?.id}/>
                            </Form.Item>
                            <Form.Item name="size" label="Формат изображения"
                                       rules={[{required: true, message: 'Пожалуйста, выберите формат'}]}>
                                <Select size="middle" disabled={!!currentCase?.id} options={options.map((opt, index) => ({
                                    value: index,
                                    label:
                                        <span><b>1:{round(opt.width, opt.height)}</b> {opt.name} ({opt.height}x{opt.width})</span>
                                }))}/>
                            </Form.Item>
                            <Form.Item className={styles.generateWrapper}>
                                <Button type="primary" htmlType="submit" className={styles.generate} disabled={!!currentCase?.id}>Сгенерировать
                                    картинку</Button>
                            </Form.Item>
                        </>
                    ) : (
                        <>
                            <Form.Item name='title'>
                                <TextArea className={styles.text} placeholder="Заголовок" value={title}
                                          onChange={(e) => setTitle(e.target.value)}/>
                            </Form.Item>
                            <Form.Item name='subtitle'>
                                <TextArea className={styles.text} placeholder="Подзаголовок" value={subtitle}
                                          onChange={(e) => setSubtitle(e.target.value)}/>
                            </Form.Item>
                            <Flex justify='space-between' className={styles.buttonGroup}>
                                <Button type="primary" htmlType="submit" size="large" onClick={next}>Применить</Button>
                                <Button type="dashed" danger size="large" onClick={handleClearText}>Сбросить текст</Button>
                            </Flex>
                            {/*<Form.Item>*/}
                            {/*    <Button type="primary" size="large" onClick={handleGenText}*/}
                            {/*            className={styles.altButton}>Сгенерировать*/}
                            {/*        текст автоматически</Button>*/}
                            {/*</Form.Item>*/}
                        </>
                    )}
                </Form>
            </div>
            <div className={styles.workspace}>
                {(currentCase?.images || []).length ? (
                    <>
                        <div className={styles.imgWrapper}>
                            <Carousel slides={currentCase?.images || []} selected={selectedIndex}
                                      setSelected={setSelectedIndex}/>
                        </div>
                        <Button type="primary" onClick={handleRegenerate}>Сгенерировать другую</Button>
                    </>
                ) : (
                    <span className={styles.notYet}>Еще не создано</span>
                )}
            </div>
        </div>
    )
}

export default CasePage
