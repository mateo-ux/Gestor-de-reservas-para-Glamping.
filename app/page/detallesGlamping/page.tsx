// app/page/detallesGlamping/page.tsx

interface Glamping {
    id: number;
    nombre: string;
    descripcion: string;
    ubicacion: string;
  }
  
  const DetallesGlamping = async () => {
    const res = await fetch('http://localhost:8000/api/glamping/?_=' + new Date().getTime());  // Agregar un parámetro para evitar caché
    if (!res.ok) {
      throw new Error('Error al obtener los datos');
    }
    
    const data: Glamping[] = await res.json(); // Tipamos los datos correctamente
  
    return (
      <div>
        <h1>Lista de Glampings</h1>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '20px' }}>
          {data.map((glamping) => (
            <div
              key={glamping.id}
              style={{
                border: '1px solid #ccc',
                padding: '20px',
                width: '300px',
              }}
            >
              <h2>{glamping.nombre}</h2>
              <p>{glamping.descripcion}</p>
              <p><strong>Ubicación:</strong> {glamping.ubicacion}</p>
            </div>
          ))}
        </div>
      </div>
    );
  };
  
  export default DetallesGlamping;
  