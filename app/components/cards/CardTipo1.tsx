"use client";

import React, { useState, useEffect, useRef } from 'react';

interface CardTipo1Props {
  titulo: string;
  contenido: string;
  imagenes: (string | null)[];
}

const CardTipo1: React.FC<CardTipo1Props> = ({ titulo, contenido, imagenes }) => {
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const carouselRef = useRef<HTMLDivElement>(null);

  const slideToNextImage = () => {
    setCurrentImageIndex((prevIndex) => {
      const nextIndex = (prevIndex + 1) % imagenes.length;
      if (carouselRef.current) {
        carouselRef.current.scrollTo({
          left: nextIndex * carouselRef.current.offsetWidth,
          behavior: 'smooth',
        });
      }
      return nextIndex;
    });
  };

  useEffect(() => {
    if (imagenes.length > 0) {
      const interval = setInterval(slideToNextImage, 5000);
      return () => clearInterval(interval);
    }
  }, [imagenes.length]);

  return (
    <div className="bg-primary bg-opacity-50 w-full max-w-full h-auto shadow-xl flex flex-col sm:flex-row border-base-content border-4 rounded-xl p-4">
      <div
        className="w-full sm:w-3/5 overflow-hidden flex-shrink-0"
        ref={carouselRef}
        style={{ whiteSpace: 'nowrap', scrollBehavior: 'smooth' }}
      >
        <div className="flex">
          {imagenes.map((img, index) => (
            <img
              key={index}
              src={img || '/images/default-image.png'}
              alt={titulo}
              className="rounded-xl flex-shrink-0 w-full h-auto"
              style={{ minWidth: '100%' }}
            />
          ))}
        </div>
      </div>
      <div className="w-full sm:w-2/5 p-4 flex flex-col justify-center">
        <h1 className="card-titulo text-center mb-3 text-xl sm:text-2xl">{titulo}</h1>
        <p className="text-justify leading-relaxed whitespace-normal break-words">
          {contenido}
        </p>
      </div>
    </div>
  );
};

export default CardTipo1;
