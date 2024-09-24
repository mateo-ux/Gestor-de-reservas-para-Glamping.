'use client'
import CalGeneral from '@/app/components/calendario/CalGeneral';
import CardTipo1 from '@/app/components/cards/CardTipo1';
import React, { useState, useEffect } from 'react';

interface Glamping {
    id: number;
    nombre: string;
    descripcion: string;
    ubicacion: string;
    imagen1?: string;
    imagen2?: string;
    imagen3?: string;
    imagen4?: string;
    imagen5?: string;
    imagen6?: string;
}

const Page = () => {
  // Estado para guardar los glampings disponibles seleccionados desde el hijo
  const [glampingsSeleccionados, setGlampingsSeleccionados] = useState<number[]>([]);
  // Estado para guardar la información de los glampings seleccionados
  const [glampingData, setGlampingData] = useState<Glamping[]>([]);

  // Función para actualizar el valor de los glampings desde el hijo
  const manejarGlampingsSeleccionados = (glampings: number[]) => {
    setGlampingsSeleccionados(glampings);
  };

  // Efecto para realizar la petición a la API con los IDs seleccionados
  useEffect(() => {
    if (glampingsSeleccionados.length > 0) {
      const fetchGlampingData = async () => {
        try {
          const fetchedGlampingData: Glamping[] = [];
          // Iterar sobre cada ID seleccionado y hacer la petición
          for (const id of glampingsSeleccionados) {
            const res = await fetch(`http://localhost:8000/api/glamping/${id}/`);
            if (res.ok) {
              const data: Glamping = await res.json();
              fetchedGlampingData.push(data); // Guardar cada glamping en el array
            }
          }
          setGlampingData(fetchedGlampingData); // Actualizar el estado con los datos obtenidos
        } catch (error) {
          console.error('Error al obtener los datos:', error);
        }
      };

      fetchGlampingData();
    }
  }, [glampingsSeleccionados]);

  return (
    <div className="min-h-screen items-center justify-center">
      <CalGeneral onGlampingsSelect={manejarGlampingsSeleccionados} />
      {glampingData.length > 0 && (
        <div className="flex flex-col items-center justify-center w-full max-w-screen-lg mx-auto my-auto">
          <div className="flex flex-col items-center w-full max-w-full space-y-8 ">
            {glampingData.map((glamping, index) => {
              const imagenes: string[] = [
                glamping.imagen1,
                glamping.imagen2,
                glamping.imagen3,
                glamping.imagen4,
                glamping.imagen5,
                glamping.imagen6,
              ].filter((img): img is string => img !== undefined && img !== null);

              const alignment = index % 2 === 0 ? '-translate-x-8 sm:-translate-x-16 md:-translate-x-24' : 'translate-x-8 sm:translate-x-16 md:translate-x-24';

              return (
                <div
                  key={glamping.id}
                  className={`transform ${alignment} w-full sm:w-11/12 lg:w-3/4 xl:w-full`}
                >
                  <CardTipo1
                    titulo={glamping.nombre}
                    contenido={glamping.descripcion}
                    imagenes={imagenes.length > 0 ? imagenes : ['/images/default-image.png']}
                    id={glamping.id}
                  />
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};

export default Page;
