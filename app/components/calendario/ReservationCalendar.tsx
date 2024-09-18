"use client";

import { useState } from 'react';

const ReservationCalendar = () => {
  const [checkInDate, setCheckInDate] = useState<string | undefined>(undefined);
  const [checkOutDate, setCheckOutDate] = useState<string | undefined>(undefined);

  const handleCheckInChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setCheckInDate(event.target.value);
  };

  const handleCheckOutChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setCheckOutDate(event.target.value);
  };

  // Envía las fechas a la API de Django
  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
  
    const data = {
      glamping_id: 35, // Aquí deberías obtener dinámicamente el id del glamping
      checkInDate,
      checkOutDate,
    };
  
    try {
      const response = await fetch('http://localhost:8000/crear-reserva/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
    
      if (response.ok) {
        const result = await response.json();
        console.log('Reserva enviada:', result);
      } else {
        const errorText = await response.text();
        console.error('Error en la reserva:', errorText);
      }
    } catch (error) {
      console.error('Error al enviar los datos:', error);
    }
  };

  // Genera un rango de fechas entre la fecha de entrada y la fecha de salida
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
    <div className="bg-primary bg-opacity-50 h-full max-h-full w-auto shadow-xl 
    border-base-content border-4 rounded-xl p-2 m-4 flex-col">
      <h2 className="card-titulo text-xl sm:text-xl">Busquemos qué disponibilidad hay en tu fecha preferida</h2>
      <form onSubmit={handleSubmit} className="flex p-2">
        <div className='flex p-2'>
          <div className="form-control ">
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
          <button
            type="submit"
            className="btn btn-outline btn-accent"
          >
            Confirma tu reserva
          </button>
        </div>
      </form>
      {dateRange.length > 0 && (
        <div className="mt-1">
          <h3 className="text-lg font-semibold mb-1">Rango de Fechas Seleccionado:</h3>
          <div className="grid grid-cols-7 gap-2">
            {dateRange.map(date => (
              <div
                key={date}
                className="p-2 text-center rounded bg-neutral"
              >
                {new Date(date).toLocaleDateString('es-ES', { day: 'numeric', month: 'short' })}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ReservationCalendar;

