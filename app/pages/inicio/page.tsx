
import CardTipo1 from '@/app/components/cards/CardTipo1';
import Link from 'next/link';
import React from 'react';

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

const Page = async () => {
  const res = await fetch('http://localhost:8000/api/glamping/?_=' + new Date().getTime());
  if (!res.ok) {
    throw new Error('Error al obtener los datos');
  }
  
  const data: Glamping[] = await res.json();

  return (
    <>
    <div className="w-auto text-center p-4">
        <Link href="BuscarFecha">
          <button className="btn btn-outline btn-accent">
            Dinos tu fecha ideal y te mostraremos nuestros glampings disponibles.
          </button>
        </Link>
      </div>
      </>
  );
};

export default Page;
