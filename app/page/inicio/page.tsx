import CardTipo1 from '@/app/components/cards/CardTipo1';
import React from 'react';

interface Glamping {
  id: number;
  nombre: string;
  descripcion: string;
  imagen1?: string;
  imagen2?: string;
  imagen3?: string;
  imagen4?: string;
  imagen5?: string;
  imagen6?: string;
}

const Page = async () => {
  const res = await fetch('http://localhost:8000/api/glamping/?_=' + new Date().getTime());
  if (!res.ok) {
    throw new Error('Error al obtener los datos');
  }

  const data: Glamping[] = await res.json();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4 container mx-6 px-4">
      <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold mb-8 text-center">Lista de Glampings</h1>
      <div className="flex flex-col items-center w-full max-w-full space-y-8">
        {data.map((glamping, index) => {
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
              className={`transform ${alignment} w-full sm:w-11/12 md:w-4/5 lg:w-3/4 xl:w-2/3 mx-auto`}
            >
              <CardTipo1
                titulo={glamping.nombre}
                contenido={glamping.descripcion}
                imagenes={imagenes.length > 0 ? imagenes : ['/images/default-image.png']}
              />
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Page;
