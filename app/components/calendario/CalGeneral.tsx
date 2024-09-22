"use client";

import { useState, useEffect } from 'react';

const CalGeneral = ({ onGlampingsSelect }: { onGlampingsSelect: (glampings: number[]) => void }) => {
  const [checkInDate, setCheckInDate] = useState<string | undefined>(undefined);
  const [checkOutDate, setCheckOutDate] = useState<string | undefined>(undefined);
  const [fechasOcupadas, setFechasOcupadas] = useState<string[]>([]);
  const [mensaje, setMensaje] = useState<string | undefined>(undefined);
  const [glampingsDisponibles, setGlampingsDisponibles] = useState<number[]>([]);

  const obtenerFechasOcupadas = async () => {
    try {
      const res = await fetch(`http://localhost:8000/todas_fechas-ocupadas/?checkIn=${checkInDate}&checkOut=${checkOutDate}`);
      if (res.ok) {
        const data = await res.json();
        
        setFechasOcupadas(data.fechas_ocupadas);
        setGlampingsDisponibles(data.glampings_disponibles); // Guardar los glampings disponibles
        onGlampingsSelect(data.glampings_disponibles); // Enviar los glampings disponibles al componente padre
      } else {
        console.error('Error al obtener fechas ocupadas');
      }
    } catch (error) {
      console.error('Error en la petición:', error);
    }
  };

  const verificarDisponibilidad = (start: string | undefined, end: string | undefined) => {
    if (!start || !end) return;

    const startDate = new Date(start);
    const endDate = new Date(end);
    const fechasOcupadasSet = new Set(fechasOcupadas);

    while (startDate <= endDate) {
      const dateStr = startDate.toISOString().split('T')[0];
      if (fechasOcupadasSet.has(dateStr)) {
        let nextAvailableDate = new Date(startDate);
        nextAvailableDate.setDate(nextAvailableDate.getDate() + 1);
        while (fechasOcupadasSet.has(nextAvailableDate.toISOString().split('T')[0])) {
          nextAvailableDate.setDate(nextAvailableDate.getDate() + 1);
        }
        setMensaje(`La fecha ${startDate.toLocaleDateString('es-ES')} está ocupada. La próxima fecha libre es ${nextAvailableDate.toLocaleDateString('es-ES')}.`);
        return;
      }
      startDate.setDate(startDate.getDate() + 1);
    }
    setMensaje(undefined); // No hay fechas ocupadas en el rango
  };

  useEffect(() => {
    if (checkInDate && checkOutDate) {
      obtenerFechasOcupadas();
    }
  }, [checkInDate, checkOutDate]);

  const handleCheckInChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setCheckInDate(event.target.value);
    verificarDisponibilidad(event.target.value, checkOutDate);
  };

  const handleCheckOutChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setCheckOutDate(event.target.value);
    verificarDisponibilidad(checkInDate, event.target.value);
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    const data = {
      checkInDate,
      checkOutDate,
    };
  };

  const generateDateRange = (start: string | undefined, end: string | undefined) => {
    if (!start || !end) return [];
    const startDate = new Date(start);
    const endDate = new Date(end);
    const dates = [];
    let currentDate = startDate;

    while (currentDate <= endDate) {
      dates.push(currentDate.toISOString().split('T')[0]);
      currentDate.setDate(currentDate.getDate() + 1);
    }

    return dates;
  };

  const dateRange = generateDateRange(checkInDate, checkOutDate);

  return (
    <div className="bg-primary bg-opacity-50 h-full max-h-full w-auto shadow-xl border-base-content border-2 rounded-xl p-2 m-4 flex-col">
      <h2 className="card-titulo text-xl sm:text-xl">Busquemos qué disponibilidad hay en tu fecha preferida</h2>
      <form onSubmit={handleSubmit} className="flex p-2">
        <div className='flex p-2 '>
          <div className="form-control">
            <label htmlFor="checkIn" className="label">
              <span className="card-normal">Fecha de entrada</span>
            </label>
            <input
              id="checkIn"
              type="date"
              value={checkInDate || ''}
              onChange={handleCheckInChange}
              className={`input input-bordered input-accent max-w-xs bg-primary-content w-full ${checkInDate ? 'bg-primary-content text-neutral' : ''}`}
              required
            />
          </div>
          <div className="form-control px-3">
            <label htmlFor="checkOut" className="label">
              <span className="card-normal">Fecha de salida</span>
            </label>
            <input
              id="checkOut"
              type="date"
              value={checkOutDate || ''}
              onChange={handleCheckOutChange}
              className={`input input-bordered max-w-xs bg-primary-content input-accent w-full ${checkOutDate ? 'bg-primary-content text-neutral' : ''}`}
              required
            />
          </div>
        </div>
      </form>
      {mensaje && (
        <div className="bg-primary bg-opacity-50 h-full max-h-full w-auto shadow-xl border-base-content border-2 rounded-xl p-2 m-4 flex-col">
          {mensaje}
        </div>
      )}
    </div>
  );
};

export default CalGeneral;
