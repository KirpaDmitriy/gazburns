import viteLogo from '../../assets/logo.png';
import styles from './style.module.css';
import {useContext} from "react";
import UserContext from "../../contexts/UserContext.ts";
import {Link} from "react-router-dom";
import {Button} from "antd";

const Header = () => {
    const { setToken } = useContext(UserContext);

    const handleClick = () => {
        localStorage.clear();
        setToken('');
    }

    return (
        <div className={styles.container}>
            <img src={viteLogo} className={styles.logo} alt="logo"/>
            <Link to="/login" onClick={handleClick}><Button>Выход</Button></Link>
        </div>
    );
}

export default Header
