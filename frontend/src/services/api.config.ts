import axios from "axios";

export const baseUrl = "http://81.94.150.144:8000/";

export const instance = axios.create({
    // к запросу будет приуепляться cookies
    withCredentials: false,
    baseURL: baseUrl,
});


// создаем перехватчик запросов
// который к каждому запросу добавляет accessToken из localStorage
instance.interceptors.request.use(
    (config) => {
        config.headers.Authorization = `Bearer ${localStorage.getItem("access_token")}`;
        return config;
    }
)


// создаем перехватчик ответов
// который в случае невалидного accessToken попытается его обновить
// и переотправить запрос с обновленным accessToken
instance.interceptors.response.use(
    // в случае валидного accessToken ничего не делаем:
    (config) => {
        return config;
    },
    // в случае просроченного accessToken пытаемся его обновить:
    async (error) => {
        // предотвращаем зацикленный запрос, добавляя свойство _isRetry
        const originalRequest = {...error.config};
        originalRequest._isRetry = true;
        if (
            // проверим, что ошибка именно из-за невалидного accessToken
            error.response.status === 401
        ) {
            window.location.href = "http://localhost:5173/login";
        }
        // на случай, если возникла другая ошибка (не связанная с авторизацией)
        // пробросим эту ошибку
        throw error;
    }
);