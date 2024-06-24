import styles from './style.module.css';
import Case from "../../ui/Case/Case.tsx";
import {CaseType} from "../../mocks/cases.ts";
import {Link} from 'react-router-dom';
import {useContext, useEffect} from "react";
import {instance} from "../../services/api.config.ts";
import {notification} from "antd";
import CasesContext from "../../contexts/CasesContext.ts";

const CasePage = () => {
    const {cases, setCases} = useContext(CasesContext);

    useEffect(() => {
        instance.get<CaseType[]>('/cases').then(response => {
            setCases(response.data);
        }).catch(() => {
            notification.warning({ message: 'Нет соединения с бекэндом'});
        })
    }, []);

  return (
      <div className={styles.container}>
        <div className={styles.table}>
            <Link to={`/case/0`} className={styles.link}>
                <Case isFirst/>
            </Link>
          {cases.toReversed().map((value) => (
              <Link to={`/case/${value.id}`} key={value.id} className={styles.link}>
                <Case src={value.images[value.images.length - 1]?.src}/>
              </Link>
          ))}
        </div>
      </div>
  )
}

export default CasePage
