import { useState } from 'react';

interface PlayButtonProps {
  fecha_de_entrada: string | undefined;
  fecha_de_salida: string | undefined;
  precio:string;
  nombre: string;
  
}

const PayButton: React.FC<PlayButtonProps> = ({fecha_de_entrada, fecha_de_salida, precio, nombre}) => {
  const [loading, setLoading] = useState(false);

  const handlePayment = async () => {
    setLoading(true);

    // Hacer la solicitud al backend para obtener la URL de PayU
    const response = await fetch('http://localhost:8000/create-payment/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        amount: `${precio}`,  // Monto de ejemplo
        currency: 'COP',  // Cambia según tu moneda
        description: `Reserva de glamping ${nombre} de la fecha ${fecha_de_entrada} a la fecha ${fecha_de_salida}`,
        referenceCode: 'ref2',  // Código único por transacción
      }),
    });

    const data = await response.json();

    if (data.payu_url && data.payment_data) {
      // Crear un formulario temporal para enviar los datos a PayU
      const form = document.createElement('form');
      form.action = data.payu_url;
      form.method = 'POST';

      Object.keys(data.payment_data).forEach((key) => {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = key;
        input.value = data.payment_data[key];
        form.appendChild(input);
      });

      document.body.appendChild(form);
      form.submit();  // Redirige a PayU
    }

    setLoading(false);
  };

  return (
    <div>
      <button
        onClick={handlePayment}
        disabled={loading}
        className="bg-blue-500 text-white py-2 px-4 rounded"
      >
        {loading ? 'Procesando...' : 'Pagar'}
      </button>
    </div>
  );
};

export default PayButton;
