import FormularioReserva from '@/app/components/cards/FormularioReserva';
import React from 'react'

const page = () => {
  return (
  <div className="flex justify-center items-center " >
    <div style={{margin:25}}>
    <FormularioReserva></FormularioReserva>
    </div> 
    <div></div>   
  </div>   
  )
}

export default page;
