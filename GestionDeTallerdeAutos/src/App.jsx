import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [pantalla, setPantalla] = useState('login');

  // Estados para Clientes
  const [clientes, setClientes] = useState([]);
  const [nombreInput, setNombreInput] = useState('');
  const [telefonoInput, setTelefonoInput] = useState('');
  const [emailInput, setEmailInput] = useState('');

  // Estados para Vehículos
  const [vehiculos, setVehiculos] = useState([]);
  const [placaInput, setPlacaInput] = useState('');
  const [marcaInput, setMarcaInput] = useState('');
  const [modeloInput, setModeloInput] = useState('');
  const [anioInput, setAnioInput] = useState('');
  const [idClienteInput, setIdClienteInput] = useState('');

  // Estados para Mecánicos
  const [mecanicos, setMecanicos] = useState([]);
  const [nombreMecanicoInput, setNombreMecanicoInput] = useState('');
  const [especialidadInput, EspecialidadInput] = useState('');

  // Estados para Órdenes
  const [ordenes, setOrdenes] = useState([]);
  const [idVehiculoOrdenInput, setIdVehiculoOrdenInput] = useState('');
  const [idMecanicoOrdenInput, setIdMecanicoOrdenInput] = useState('');
  const [servicioInput, setServicioInput] = useState('');
  const [costoOrdenInput, setCostoOrdenInput] = useState('');

  // --- CARGAS DESDE LA API ---
  const cargarClientes = async () => {
    try {
      const response = await fetch('http://localhost:8000/clientes/');
      const data = await response.json();
      setClientes(data);
    } catch (error) {
      console.error("Error al cargar clientes:", error);
    }
  };

  const cargarVehiculos = async () => {
    try {
      const response = await fetch('http://localhost:8000/vehiculos/');
      const data = await response.json();
      setVehiculos(data);
    } catch (error) {
      console.error("Error al cargar vehículos:", error);
    }
  };

  const cargarMecanicos = async () => {
    try {
      const response = await fetch('http://localhost:8000/mecanicos/');
      const data = await response.json();
      setMecanicos(data);
    } catch (error) {
      console.error("Error al cargar mecánicos:", error);
    }
  };

  const cargarOrdenes = async () => {
    try {
      const response = await fetch('http://localhost:8000/ordenes/');
      const data = await response.json();
      setOrdenes(data);
    } catch (error) {
      console.error("Error al cargar órdenes:", error);
    }
  };

  // Efecto para sincronizar según la pantalla activa
  useEffect(() => {
    if (pantalla === 'clientes') {
      cargarClientes();
    } else if (pantalla === 'vehiculos') {
      cargarVehiculos();
      cargarClientes();
    } else if (pantalla === 'mecanicos') {
      cargarMecanicos();
    } else if (pantalla === 'ordenes') {
      cargarOrdenes();
      cargarVehiculos();
      cargarMecanicos();
    }
  }, [pantalla]);

  // --- ACCIONES DE CLIENTES ---
  const guardarCliente = async () => {
    const partes = nombreInput.trim().split(' ');
    const nombre = partes[0] || 'Desconocido';
    const apellido = partes.slice(1).join(' ') || 'SinApellido';

    if (nombreInput.trim() !== '' && telefonoInput.trim() !== '') {
      try {
        const response = await fetch('http://localhost:8000/clientes/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ nombre, apellido, telefono: telefonoInput, email: emailInput || "correo@ejemplo.com" }),
        });
        if (response.ok) {
          setNombreInput(''); setTelefonoInput(''); setEmailInput('');
          cargarClientes();
        }
      } catch (error) { console.error("Error:", error); }
    } else {
      alert("Por favor, completa los campos obligatorios.");
    }
  };

  const eliminarCliente = async (id) => {
    try {
      const response = await fetch(`http://localhost:8000/clientes/${id}`, { method: 'DELETE' });
      if (response.ok) cargarClientes();
    } catch (error) { console.error("Error:", error); }
  };

  // --- ACCIONES DE VEHÍCULOS ---
  const guardarVehiculo = async () => {
    if (!idClienteInput) {
      alert("Por favor, selecciona un cliente del menú desplegable.");
      return;
    }
    if (placaInput.trim() !== '' && marcaInput.trim() !== '' && modeloInput.trim() !== '') {
      try {
        const response = await fetch('http://localhost:8000/vehiculos/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            placa: placaInput,
            marca: marcaInput,
            modelo: modeloInput,
            anio: parseInt(anioInput) || 2022,
            id_cliente: parseInt(idClienteInput)
          }),
        });
        if (response.ok) {
          setPlacaInput(''); setMarcaInput(''); setModeloInput(''); setAnioInput(''); setIdClienteInput('');
          cargarVehiculos();
        } else {
          alert("Error al registrar el vehículo.");
        }
      } catch (error) { console.error("Error:", error); }
    } else {
      alert("Por favor, completa los campos obligatorios del vehículo.");
    }
  };

  const eliminarVehiculo = async (id) => {
    try {
      const response = await fetch(`http://localhost:8000/vehiculos/${id}`, { method: 'DELETE' });
      if (response.ok) cargarVehiculos();
    } catch (error) { console.error("Error:", error); }
  };

  // --- ACCIONES DE MECÁNICOS ---
  const guardarMecanico = async () => {
    const partes = nombreMecanicoInput.trim().split(' ');
    const nombre = partes[0] || 'Desconocido';
    const apellido = partes.slice(1).join(' ') || 'SinApellido';

    if (nombreMecanicoInput.trim() !== '') {
      try {
        const response = await fetch('http://localhost:8000/mecanicos/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ 
            nombre: nombre, 
            apellido: apellido, 
            especialidad: especialidadInput || 'General' 
          }),
        });
        if (response.ok) {
          setNombreMecanicoInput(''); 
          EspecialidadInput('');
          cargarMecanicos();
        } else {
          alert("Error al registrar el mecánico.");
        }
      } catch (error) { console.error("Error:", error); }
    }
  };

  const eliminarMecanico = async (id) => {
    try {
      const response = await fetch(`http://localhost:8000/mecanicos/${id}`, { method: 'DELETE' });
      if (response.ok) cargarMecanicos();
    } catch (error) { console.error("Error:", error); }
  };

  // --- ACCIONES DE ÓRDENES ---
  const guardarOrden = async () => {
    if (idVehiculoOrdenInput && idMecanicoOrdenInput && servicioInput.trim() !== '' && costoOrdenInput.trim() !== '') {
      try {
        const response = await fetch('http://localhost:8000/ordenes/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ 
            descripcion: servicioInput, 
            estado: 'En Proceso', 
            costo: parseFloat(costoOrdenInput),
            id_mecanico: parseInt(idMecanicoOrdenInput),
            id_vehiculo: parseInt(idVehiculoOrdenInput)
          }),
        });
        if (response.ok) {
          setIdVehiculoOrdenInput(''); 
          setIdMecanicoOrdenInput('');
          setServicioInput(''); 
          setCostoOrdenInput('');
          cargarOrdenes();
        } else {
          alert("Error al registrar la orden.");
        }
      } catch (error) { console.error("Error:", error); }
    } else {
      alert("Por favor, completa todos los campos de la orden.");
    }
  };

  const eliminarOrden = async (id) => {
    try {
      const response = await fetch(`http://localhost:8000/ordenes/${id}`, { method: 'DELETE' });
      if (response.ok) cargarOrdenes();
    } catch (error) { console.error("Error:", error); }
  };

  // 1. VISTA DE LOGIN
  if (pantalla === 'login') {
    return (
      <div style={styles.loginContainer}>
        <div style={styles.loginBox}>
          <h2>INICIAR SESIÓN</h2>
          <input type="text" placeholder="USUARIO" style={styles.input} />
          <input type="password" placeholder="CONTRASEÑA" style={styles.input} />
          <button style={styles.button} onClick={() => setPantalla('dashboard')}>
            INGRESAR
          </button>
        </div>
      </div>
    );
  }

  // 2. VISTAS PRINCIPALES
  return (
    <div style={styles.mainLayoutContainer}>
      <nav className="navbar navbar-expand-lg navbar-dark px-3" style={{ backgroundColor: '#161c27', borderBottom: '1px solid #222d3f' }}>
        <div className="container-fluid">
          <span className="navbar-brand" style={{ fontSize: '14px', cursor: 'pointer', fontWeight: 'bold' }} onClick={() => setPantalla('dashboard')}>
            TALLER DE AUTOS
          </span>
          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav ms-auto">
              <li className="nav-item"><span className="nav-link" style={{ cursor: 'pointer', color: pantalla === 'dashboard' ? '#fff' : '#9ba3af' }} onClick={() => setPantalla('dashboard')}>INICIO</span></li>
              <li className="nav-item"><span className="nav-link" style={{ cursor: 'pointer', color: pantalla === 'clientes' ? '#fff' : '#9ba3af' }} onClick={() => setPantalla('clientes')}>CLIENTES</span></li>
              <li className="nav-item"><span className="nav-link" style={{ cursor: 'pointer', color: pantalla === 'vehiculos' ? '#fff' : '#9ba3af' }} onClick={() => setPantalla('vehiculos')}>VEHÍCULOS</span></li>
              <li className="nav-item"><span className="nav-link" style={{ cursor: 'pointer', color: pantalla === 'mecanicos' ? '#fff' : '#9ba3af' }} onClick={() => setPantalla('mecanicos')}>MECÁNICOS</span></li>
              <li className="nav-item"><span className="nav-link" style={{ cursor: 'pointer', color: pantalla === 'ordenes' ? '#fff' : '#9ba3af' }} onClick={() => setPantalla('ordenes')}>ÓRDENES</span></li>
            </ul>
          </div>
        </div>
      </nav>

      <div style={styles.content}>
        
        {/* DASHBOARD */}
        {pantalla === 'dashboard' && (
          <div className="container-fluid px-0">
            <div className="row mb-4">
              <div className="col-12">
                <h2 className="text-white fw-bold mb-1">Panel de Control</h2>
                <p className="text-muted">Resumen general del taller automotriz</p>
              </div>
            </div>

            {/* Tarjetas de Métricas Superiores */}
            <div className="row g-4 mb-4">
              <div className="col-md-4">
                <div className="card bg-dark text-white border-primary shadow h-100 py-2">
                  <div className="card-body">
                    <div className="d-flex justify-content-between align-items-center">
                      <div>
                        <div className="text-xs fw-bold text-primary text-uppercase mb-1">Vehículos Registrados</div>
                        <div className="h4 fw-bold mb-0">{vehiculos.length}</div>
                      </div>
                      <span className="fs-1 text-primary">🚗</span>
                    </div>
                  </div>
                </div>
              </div>
              <div className="col-md-4">
                <div className="card bg-dark text-white border-success shadow h-100 py-2">
                  <div className="card-body">
                    <div className="d-flex justify-content-between align-items-center">
                      <div>
                        <div className="text-xs fw-bold text-success text-uppercase mb-1">Mecánicos Activos</div>
                        <div className="h4 fw-bold mb-0">{mecanicos.length}</div>
                      </div>
                      <span className="fs-1 text-success">👨‍🔧</span>
                    </div>
                  </div>
                </div>
              </div>
              <div className="col-md-4">
                <div className="card bg-dark text-white border-warning shadow h-100 py-2">
                  <div className="card-body">
                    <div className="d-flex justify-content-between align-items-center">
                      <div>
                        <div className="text-xs fw-bold text-warning text-uppercase mb-1">Órdenes de Trabajo</div>
                        <div className="h4 fw-bold mb-0">{ordenes.length}</div>
                      </div>
                      <span className="fs-1 text-warning">📋</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Sección Inferior: Órdenes Recientes y Resumen del Taller */}
            <div className="row g-4">
              {/* Tabla compacta de órdenes recientes */}
              <div className="col-md-7">
                <div className="card bg-dark text-white border-secondary shadow h-100">
                  <div className="card-header border-secondary fw-bold bg-transparent">Últimas Órdenes Registradas</div>
                  <div className="card-body p-0">
                    <div className="table-responsive">
                      <table className="table table-dark table-hover mb-0 align-middle">
                        <thead>
                          <tr>
                            <th>ID</th>
                            <th>Descripción</th>
                            <th>Estado</th>
                          </tr>
                        </thead>
                        <tbody>
                          {ordenes.slice(0, 5).map((o) => (
                            <tr key={o.id}>
                              <td className="fw-bold">{o.id}</td>
                              <td>{o.descripcion}</td>
                              <td><span className="badge bg-warning text-dark">{o.estado || 'En Proceso'}</span></td>
                            </tr>
                          ))}
                          {ordenes.length === 0 && (
                            <tr>
                              <td colSpan="3" className="text-center text-muted py-3">No hay órdenes registradas aún.</td>
                            </tr>
                          )}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              </div>

              {/* Panel de Estadísticas / Estado del Taller */}
              <div className="col-md-5">
                <div className="card bg-dark text-white border-secondary shadow h-100 p-4">
                  <h5 className="mb-4 fw-bold">Estado del Taller</h5>
                  <div className="mb-3">
                    <div className="d-flex justify-content-between mb-1 small">
                      <span>En Proceso</span>
                      <span className="text-warning fw-bold">Activo</span>
                    </div>
                    <div className="progress" style={{ height: '8px', backgroundColor: '#2b3035' }}>
                      <div className="progress-bar bg-warning" style={{ width: '70%' }}></div>
                    </div>
                  </div>
                  <div className="mb-3">
                    <div className="d-flex justify-content-between mb-1 small">
                      <span>Completadas</span>
                      <span className="text-success fw-bold">Estable</span>
                    </div>
                    <div className="progress" style={{ height: '8px', backgroundColor: '#2b3035' }}>
                      <div className="progress-bar bg-success" style={{ width: '30%' }}></div>
                    </div>
                  </div>
                  <p className="text-muted small mt-3 mb-0">
                    💡 Consejo: Puedes registrar nuevos vehículos y mecánicos desde sus respectivas pestañas para que aparezcan automáticamente en las órdenes.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* CLIENTES */}
        {pantalla === 'clientes' && (
          <div>
            <h2>Gestión de Clientes</h2>
            <div style={styles.formBox}>
              <h3>Registrar Cliente</h3>
              <label style={styles.label}>NOMBRES Y APELLIDOS</label>
              <input type="text" style={styles.input} placeholder="Ej. Carlos Ruiz" value={nombreInput} onChange={(e) => setNombreInput(e.target.value)} />
              <label style={styles.label}>TELÉFONO</label>
              <input type="text" style={styles.input} placeholder="Ej. 987654321" value={telefonoInput} onChange={(e) => setTelefonoInput(e.target.value)} />
              <label style={styles.label}>EMAIL</label>
              <input type="email" style={styles.input} placeholder="Ej. correo@correo.com" value={emailInput} onChange={(e) => setEmailInput(e.target.value)} />
              <button style={styles.button} onClick={guardarCliente}>GUARDAR CLIENTE</button>
            </div>
            
            <table className="table table-dark table-striped table-hover align-middle mt-4">
              <thead className="table-secondary">
                <tr>
                  <th style={{ width: '60px' }}>ID</th>
                  <th>Nombre Completo</th>
                  <th>Teléfono</th>
                  <th>Email</th>
                  <th className="text-end">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {clientes.map((c, index) => (
                  <tr key={c.id || index}>
                    <td className="text-light fw-bold">{c.id}</td>
                    <td className="fw-bold text-light">{c.nombre} {c.apellido}</td>
                    <td>{c.telefono}</td>
                    <td className="text-info">{c.email}</td>
                    <td className="text-end">
                      <button className="btn btn-outline-danger btn-sm" onClick={() => eliminarCliente(c.id)}>Eliminar</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* VEHÍCULOS */}
        {pantalla === 'vehiculos' && (
          <div>
            <h2>Gestión de Vehículos</h2>
            <div style={styles.formBox}>
              <h3>Registrar Nuevo Vehículo</h3>
              <label style={styles.label}>PLACA</label>
              <input type="text" style={styles.input} placeholder="Ej. ABC-123" value={placaInput} onChange={(e) => setPlacaInput(e.target.value)} />
              
              <label style={styles.label}>MARCA</label>
              <input type="text" style={styles.input} placeholder="Ej. Toyota" value={marcaInput} onChange={(e) => setMarcaInput(e.target.value)} />

              <label style={styles.label}>MODELO</label>
              <input type="text" style={styles.input} placeholder="Ej. Corolla" value={modeloInput} onChange={(e) => setModeloInput(e.target.value)} />

              <label style={styles.label}>AÑO</label>
              <input type="text" style={styles.input} placeholder="Ej. 2022" value={anioInput} onChange={(e) => setAnioInput(e.target.value)} />

              <label style={styles.label}>SELECCIONAR CLIENTE</label>
              <select style={styles.input} value={idClienteInput} onChange={(e) => setIdClienteInput(e.target.value)}>
                <option value="">-- Seleccione un cliente --</option>
                {clientes.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.nombre} {c.apellido} (ID: {c.id})
                  </option>
                ))}
              </select>

              <button style={styles.button} onClick={guardarVehiculo}>GUARDAR VEHÍCULO</button>
            </div>

            <table className="table table-dark table-striped table-hover align-middle mt-4">
              <thead className="table-secondary">
                <tr>
                  <th style={{ width: '60px' }}>ID</th>
                  <th>Placa</th>
                  <th>Marca</th>
                  <th>Modelo</th>
                  <th>Año</th>
                  <th>ID Cliente</th>
                  <th className="text-end">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {vehiculos.map((v, index) => (
                  <tr key={v.id || index}>
                    <td className="text-light fw-bold">{v.id}</td>
                    <td className="fw-bold text-light">{v.placa}</td>
                    <td>{v.marca}</td>
                    <td>{v.modelo}</td>
                    <td>{v.anio}</td>
                    <td className="text-info">ID: {v.id_cliente}</td>
                    <td className="text-end">
                      <button className="btn btn-outline-danger btn-sm" onClick={() => eliminarVehiculo(v.id)}>Eliminar</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* MECÁNICOS */}
        {pantalla === 'mecanicos' && (
          <div>
            <h2>Gestión de Mecánicos</h2>
            <div style={styles.formBox}>
              <h3>Registrar Mecánico</h3>
              <label style={styles.label}>NOMBRES Y APELLIDOS</label>
              <input type="text" style={styles.input} placeholder="Ej. Juan Pérez" value={nombreMecanicoInput} onChange={(e) => setNombreMecanicoInput(e.target.value)} />
              <label style={styles.label}>ESPECIALIDAD</label>
              <input type="text" style={styles.input} placeholder="Ej. Motor y Suspensión" value={especialidadInput} onChange={(e) => EspecialidadInput(e.target.value)} />
              <button style={styles.button} onClick={guardarMecanico}>GUARDAR MECÁNICO</button>
            </div>
            <table className="table table-dark table-striped table-hover align-middle mt-4">
              <thead className="table-secondary">
                <tr>
                  <th style={{ width: '60px' }}>ID</th>
                  <th>Nombre Completo</th>
                  <th>Especialidad</th>
                  <th className="text-end">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {mecanicos.map((m, index) => (
                  <tr key={m.id || index}>
                    <td className="text-light fw-bold">{m.id}</td>
                    <td className="fw-bold text-light">{m.nombre} {m.apellido}</td>
                    <td>{m.especialidad}</td>
                    <td className="text-end">
                      <button className="btn btn-outline-danger btn-sm" onClick={() => eliminarMecanico(m.id)}>Eliminar</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* ÓRDENES */}
        {pantalla === 'ordenes' && (
          <div>
            <h2>Órdenes de Trabajo</h2>
            <div style={styles.formBox}>
              <h3>Crear Orden</h3>
              
              <label style={styles.label}>SELECCIONAR VEHÍCULO</label>
              <select 
                style={styles.input} 
                value={idVehiculoOrdenInput} 
                onChange={(e) => setIdVehiculoOrdenInput(e.target.value)}
              >
                <option value="">-- Seleccione un vehículo --</option>
                {vehiculos.map((v) => (
                  <option key={v.id} value={v.id}>
                    {v.placa} - {v.marca} {v.modelo} (ID: {v.id})
                  </option>
                ))}
              </select>

              <label style={styles.label}>SELECCIONAR MECÁNICO</label>
              <select 
                style={styles.input} 
                value={idMecanicoOrdenInput} 
                onChange={(e) => setIdMecanicoOrdenInput(e.target.value)}
              >
                <option value="">-- Seleccione un mecánico --</option>
                {mecanicos.map((m) => (
                  <option key={m.id} value={m.id}>
                    {m.nombre} {m.apellido} - {m.especialidad} (ID: {m.id})
                  </option>
                ))}
              </select>

              <label style={styles.label}>DESCRIPCIÓN DEL SERVICIO</label>
              <input 
                type="text" 
                style={styles.input} 
                placeholder="Ej. Cambio de aceite y filtros" 
                value={servicioInput} 
                onChange={(e) => setServicioInput(e.target.value)} 
              />

              <label style={styles.label}>COSTO (S/)</label>
              <input 
                type="number" 
                style={styles.input} 
                placeholder="Ej. 150.00" 
                value={costoOrdenInput} 
                onChange={(e) => setCostoOrdenInput(e.target.value)} 
              />

              <button style={styles.button} onClick={guardarOrden}>
                CREAR ORDEN
              </button>
            </div>
            
            <table className="table table-dark table-striped table-hover align-middle mt-4">
              <thead className="table-secondary">
                <tr>
                  <th style={{ width: '60px' }}>ID</th>
                  <th>ID Vehículo</th>
                  <th>ID Mecánico</th>
                  <th>Descripción</th>
                  <th>Costo</th>
                  <th>Estado</th>
                  <th className="text-end">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {ordenes.map((o, index) => (
                  <tr key={o.id || index}>
                    <td>{o.id}</td>
                    <td>{o.id_vehiculo}</td>
                    <td>{o.id_mecanico}</td>
                    <td>{o.descripcion}</td>
                    <td>S/ {o.costo}</td>
                    <td><span className="badge bg-warning text-dark">{o.estado || 'En Proceso'}</span></td>
                    <td className="text-end">
                      <button className="btn btn-outline-danger btn-sm" onClick={() => eliminarOrden(o.id)}>Eliminar</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

      </div>
    </div>
  );
}

const styles = {
  loginContainer: { height: '100vh', display: 'flex', justifyContent: 'center', alignItems: 'center' },
  loginBox: { backgroundColor: '#1b2331', padding: '40px', borderRadius: '8px', textAlign: 'center', width: '300px', border: '1px solid #2a3447' },
  mainLayoutContainer: { display: 'flex', flexDirection: 'column', minHeight: '100vh' },
  content: { flex: 1, padding: '40px', overflowY: 'auto' },
  input: { width: '100%', padding: '10px', marginTop: '5px', marginBottom: '15px', backgroundColor: '#d1d5db', color: '#000000', border: 'none', borderRadius: '4px', boxSizing: 'border-box' },
  label: { fontSize: '12px', color: '#9ba3af', display: 'block' },
  button: { width: '100%', padding: '10px', backgroundColor: '#2d3748', color: '#fff', border: '1px solid #4a5568', cursor: 'pointer', borderRadius: '4px' },
  cardsContainer: { display: 'flex', gap: '20px', marginTop: '20px' },
  card: { backgroundColor: '#1b2331', padding: '20px', borderRadius: '6px', width: '150px', textAlign: 'center', border: '1px solid #2a3447' },
  formBox: { backgroundColor: '#1b2331', padding: '25px', borderRadius: '8px', width: '400px', border: '1px solid #2a3447', marginBottom: '20px' }
};

export default App;