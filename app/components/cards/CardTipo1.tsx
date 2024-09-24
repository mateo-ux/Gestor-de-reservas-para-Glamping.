"use client";

import React, { useState, useEffect, useRef } from 'react';
import ReservationCalendar from '../calendario/ReservationCalendar';
 // Importa tu componente de reserva aquí

interface CardTipo1Props {
  nombre: string;
  contenido: string;
  precio: string;
  imagenes: (string | null)[];
  id: number;
}

const CardTipo1: React.FC<CardTipo1Props> = ({ nombre, contenido, imagenes, id, precio }) => {
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [mostrarReserva, setMostrarReserva] = useState(false); // Estado para controlar si se muestra el componente de reserva
  const carouselRef = useRef<HTMLDivElement>(null);
  const modalRef = useRef<HTMLDivElement>(null); // Referencia para el modal
  

  // Función para cambiar la imagen en el carrusel
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

  // Detectar clic fuera del modal para cerrarlo
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (modalRef.current && !modalRef.current.contains(event.target as Node)) {
        setMostrarReserva(false); // Cerrar modal si se hace clic fuera
      }
    };

    if (mostrarReserva) {
      document.addEventListener("mousedown", handleClickOutside);
    }

    // Limpiar el event listener cuando se desmonte el modal o se cierre
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [mostrarReserva]);

  // Iniciar el carrusel
  useEffect(() => {
    if (imagenes.length > 0) {
      const interval = setInterval(slideToNextImage, 5000);
      return () => clearInterval(interval);
    }
  }, [imagenes.length]);

  return (
    <div className="bg-primary bg-opacity-50 h-full max-h-full w-auto shadow-xl 
    border-base-content border-4 rounded-xl p-4 flex flex-col">
      {/* Contenedor del título */}
      <div className="w-auto text-center mb-4">
        <h1 className="card-titulo text-xl sm:text-3xl">{nombre}</h1>
      </div>

      {/* Contenedor de la imagen */}
      <div className="flex flex-col sm:flex-row justify-between">
        <div
          className="w-full sm:w-3/5 overflow-hidden flex items-center justify-center flex-shrink-0"
          ref={carouselRef}
          style={{ whiteSpace: 'nowrap', scrollBehavior: 'smooth' }}
        >
          <div className="flex">
            {imagenes.map((img, index) => (
              <img
                key={index}
                src={img || '/images/default-image.png'}
                alt={nombre}
                className="rounded-xl flex-shrink-0 w-full h-auto"
                style={{ minWidth: '100%' }}
              />
            ))}
          </div>
        </div>

        {/* Contenedor del texto descriptivo */}
        <div className="w-full sm:w-2/5 p-4 flex flex-col justify-center">
          <p className="text-justify leading-relaxed whitespace-normal break-words">
            {contenido}
          </p>
          <h1 className="card-titulo text-xl sm:text-3xl">Valor por noche: {precio}</h1>
        </div>
      </div>

      {/* Botón de reserva */}
      <div className="w-auto text-center mb-4">
        <button
          className="btn btn-outline btn-accent"
          onClick={() => setMostrarReserva(true)} // Mostrar el componente al hacer clic
        >
          Reserva tu estadía con nosotros
        </button>
      </div>

      {/* Mostrar el componente de reserva si el estado está en true */}
      {mostrarReserva && (        
          <div ref={modalRef} className="w-full px-8">
            <ReservationCalendar 
            id={id} 
            precio={precio}
            nombre={nombre}
            />
           
          </div>       
      )}
    </div>
  );
};

export default CardTipo1;
