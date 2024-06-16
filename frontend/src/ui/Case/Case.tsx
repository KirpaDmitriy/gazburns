import styles from './style.module.css';
import caseImg from '../../assets/caseMock.png'
import {FC} from "react";

interface ICaseProps {
    src?: string;
    isFirst?: boolean;
}

const Case: FC<ICaseProps> = ({ src, isFirst }) => {

  return isFirst ? (
      <div className={styles.first}>
          <svg width="70" height="70" viewBox="0 0 70 70" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path
                  d="M40 5C40 2.23858 37.7614 0 35 0C32.2386 0 30 2.23858 30 5V30H5C2.23858 30 0 32.2386 0 35C0 37.7614 2.23858 40 5 40H30V65C30 67.7614 32.2386 70 35 70C37.7614 70 40 67.7614 40 65V40H65C67.7614 40 70 37.7614 70 35C70 32.2386 67.7614 30 65 30H40V5Z"
                  fill="white"/>
          </svg>
          <span>Новая генерация</span>
      </div>
  ) : (
      <div className={styles.container}>
          <img src={src ?? caseImg} className={styles.img} alt="case"/>
      </div>
  )
}

export default Case
