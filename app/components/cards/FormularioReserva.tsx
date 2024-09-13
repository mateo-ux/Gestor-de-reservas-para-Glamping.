import React from 'react';

const FormularioReserva = () => {
  return (
    <div className="card w-full max-w-md shadow-xl border-primary 
    border-4 rounded-lg p-4">
      <div className=" inset-0  pointer-events-none rounded-box 
      border-{primary} z-0"></div>
      <h1 className="card-title text-4xl">Formarto de reserva</h1>
      <br />
      <div className="flex flex-col gap-4">
        <label className="flex flex-col gap-2">
          Nombre completo
          <input
            type="text"
            className="resize-y border-primary border-4 rounded p-2"
          />
        </label>
        <label className="flex flex-col gap-2">
          Email
          <input
            type="email"
            className="resize-y border-primary border-4 rounded p-2"
            placeholder="IAConexion@ejemplo.com"
          />
        </label>
        <label className="flex flex-col gap-2">
          Numero de telefono
          <input
            type="tel"
            className="resize-y border-primary border-4 rounded p-2"
            placeholder="+57"
          />
        </label>
        <label className="flex flex-col gap-2">
         Requerimientos especiales
          <input
            type="text"
            className="resize-y border-primary border-4 rounded p-2"
          />
        </label>
        <button className="btn btn-outline border-primary">Ir a pago</button>
      </div>
    </div>
  );
};

export default FormularioReserva;