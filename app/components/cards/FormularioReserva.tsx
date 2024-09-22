import React from 'react';
interface FormularioReservaProps {
  fecha_de_entrada: string | undefined;
  fecha_de_salida: string | undefined;
  
}

const FormularioReserva: React.FC<FormularioReservaProps> = ({fecha_de_entrada, fecha_de_salida}) => {
  return (
    <div className="card w-full max-w-md shadow-xl border-black 
    border-2 rounded-lg p-4 m-4">
      <div className=" inset-0  pointer-events-none rounded-box 
      border-{primary} z-0"></div>

      <h1 className="card-title text-4xl">Formarto de reserva</h1>
      <br />
      <label className="flex flex-col gap-2">
        Fecha de entrada
        <input
        type="text"
        placeholder={fecha_de_entrada}
        className="input input-bordered input-accent w-full max-w-xs"
        disabled />
        </label>
      <br />
        <label className="flex flex-col gap-2">
        Fecha de salida
        <input
        type="text"
        placeholder={fecha_de_salida}
        className="input input-bordered input-accent w-full max-w-xs"
        disabled />
        </label>
      <br />
      <div className="flex flex-col gap-4">
        <label className="flex flex-col gap-2">
          Nombre completo
          <input
            type="text"
            className=" input input-bordered input-accent w-full max-w-xs text-black"
          />
        </label>
        <label className="flex flex-col gap-2">
          Email
          <input
            type="email"
            className="input input-bordered input-accent w-full max-w-xs text-black"
            placeholder="Raices@ejemplo.com"
          />
        </label>
        <label className="flex flex-col gap-2">
          Numero de telefono
          <input
            type="tel"
            className="input input-bordered input-accent w-full max-w-xs text-black"
            placeholder="+57"
          />
        </label>
        <label className="flex flex-col gap-2">
         Requerimientos especiales
          <input
            type="text"
            className="input input-bordered input-accent w-full max-w-xs text-black"
          />
        </label>
        <div className="w-auto text-center mb-4">
        <button
          className="btn btn-outline btn-accent"
        >
          Ir al pago
        </button>
      </div>
      </div>
    </div>
  );
};

export default FormularioReserva;