import {Button, Form, Input, notification, Spin} from "antd";
import {UserOutlined, LockOutlined} from '@ant-design/icons';

import styles from './style.module.css';
import {baseUrl} from "../../services/api.config.ts";
import {useContext} from "react";
import UserContext from "../../contexts/UserContext.ts";
import axios from "axios";
import {useNavigate} from "react-router-dom";

interface ILoginForm {
    username: string;
    password: string;
}

const LoginPage = () => {
    const navigate = useNavigate();
    const {setToken, setLoading, loading} = useContext(UserContext);
    const onFinish = ({username, password}: ILoginForm) => {
        setLoading(true);
        axios.post(baseUrl + "token", {username, password}).then(response => {
            if (response.data?.access_token) {
                setToken(response.data?.access_token);
                localStorage.setItem("access_token", response.data?.access_token);
                navigate('/home');
                setLoading(false);
            }
        }).catch(error => {
            setLoading(false);
            if (error.response) {
                notification.warning({message: error.response.data});
            } else if (error.request) {
                // Запрос был сделан, но ответ не получен
                // `error.request`- это экземпляр XMLHttpRequest в браузере и экземпляр
                // http.ClientRequest в node.js
                notification.warning({message: error.request});
            } else {
                // Произошло что-то при настройке запроса, вызвавшее ошибку
                notification.warning({message: "Нет соединения с сервером"});
            }
        })
    };

    return loading ? (
        <div className={styles.container}>
            <Spin/>
        </div>
    ) : (
        <div className={styles.container}>
            <Form
                name="normal_login"
                className={styles.loginForm}
                onFinish={onFinish}
            >
                <Form.Item
                    name="username"
                    rules={[
                        {
                            required: true,
                            message: 'Пожалуйста, введите логин',
                        },
                    ]}
                >
                    <Input prefix={<UserOutlined/>} placeholder="Username"/>
                </Form.Item>
                <Form.Item
                    name="password"
                    rules={[
                        {
                            required: true,
                            message: 'Пожалуйста, введите пароль',
                        },
                    ]}
                >
                    <Input
                        prefix={<LockOutlined/>}
                        type="password"
                        placeholder="Password"
                    />
                </Form.Item>

                <Form.Item>
                    <Button type="primary" htmlType="submit" className={styles.loginFormButton}>
                        Войти
                    </Button>
                    {/*Or <a href="">register now!</a>*/}
                </Form.Item>
            </Form>
            <div className={styles.test}>
                <p>Тестовые пользователи:</p>
                <p><b>Логин: test1 Пароль: test1</b></p>
                <p>Логин: user2 Пароль: password2</p>
                <a href="https://disk.yandex.com/i/dHjkcExhZrD5xA" target="_blank">Инструкция пользователя</a>
            </div>
        </div>
    );
}

export default LoginPage;
