import styles from './style.module.css';
import {Link} from "react-router-dom";

const NotFoundPage = () => (
    <div className={styles.container}>
        <span>Страница не найдена. Пожалуйста, вернитесь на начальную страницу.</span>
        <Link to="/home">Назад</Link>
    </div>
);

export default NotFoundPage;
