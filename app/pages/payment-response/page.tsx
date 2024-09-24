'use client'

import { useSearchParams } from 'next/navigation';

const PaymentResponse = () => {
  const searchParams = useSearchParams();
  const referenceCode = searchParams.get('referenceCode');
  const transactionState = searchParams.get('transactionState');

  return (
    <div className="container mx-auto">
      <h1 className="text-2xl font-bold">Estado del pago</h1>
      <p>Referencia: {referenceCode}</p>
      <p>Estado: {transactionState === '4' ? 'Aprobado' : 'Rechazado'}</p>
    </div>
  );
};

export default PaymentResponse;
