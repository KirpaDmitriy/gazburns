import useEmblaCarousel from "embla-carousel-react";
import {useCallback, useEffect} from "react";
import {Thumb} from "../Thumb/Thumb.tsx";
import {Generation} from "../../mocks/cases.ts";

import styles from './style.module.css';
import {DownloadOutlined, FileImageOutlined} from "@ant-design/icons";
import {Tooltip} from "antd";

type PropType = {
    slides: Generation[];
    selected: number;
    setSelected: (index: number) => void;
}

export const Carousel: React.FC<PropType> = ({slides, setSelected, selected}) => {
    const [mainViewportRef, embla] = useEmblaCarousel({skipSnaps: false});
    const [thumbViewportRef, emblaThumbs] = useEmblaCarousel({
        containScroll: "keepSnaps",
        dragFree: true
    });

    useEffect(() => {
        onThumbClick(selected);
    }, [selected]);

    const onThumbClick = useCallback(
        (index: number) => {
            if (!embla || !emblaThumbs) return;
            embla.scrollTo(index);
        },
        [embla, emblaThumbs, selected]
    );

    const onSelect = useCallback(() => {
        if (!embla || !emblaThumbs) return;
        setSelected(embla.selectedScrollSnap());
        emblaThumbs.scrollTo(embla.selectedScrollSnap());
    }, [embla, emblaThumbs, setSelected]);

    useEffect(() => {
        if (!embla) return;
        onSelect();
        embla.on("select", onSelect);
    }, [embla, onSelect]);

    return (
        <>
            <div className="embla">
                <div className="embla__viewport" ref={mainViewportRef}>
                    <div className="embla__container">
                        {slides.map((gen) => (
                            <div className="embla__slide" key={gen.id}>
                                <div className="embla__slide__inner">
                                    <Tooltip title="Скачать баннер">
                                        <a href={gen.src} download target="_blank" className={styles.download}>
                                            <DownloadOutlined/>
                                        </a>
                                    </Tooltip>
                                    <Tooltip title="Скачать png объекта">
                                        <a href={gen.object || ''} download target="_blank" className={styles.downloadObj}>
                                            <FileImageOutlined/>
                                        </a>
                                    </Tooltip>
                                    <img
                                        className="embla__slide__img"
                                        src={gen.src}
                                        alt="A cool cat."
                                    />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            <div className="embla embla--thumb">
                <div className="embla__viewport" ref={thumbViewportRef}>
                    <div className="embla__container embla__container--thumb">
                        {slides.map((gen, index) => (
                            <Thumb
                                onClick={() => onThumbClick(index)}
                                selected={index === selected}
                                imgSrc={gen.src}
                                key={gen.id}
                            />
                        ))}
                    </div>
                </div>
            </div>
        </>
    );
}