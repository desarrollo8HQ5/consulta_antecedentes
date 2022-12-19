const express = require('express');
const app = express();
const morgan = require('morgan');

// Configuración
// Dar prioridad al puerto dado por servicio en nube
app.set('port', process.env.PORT || 3000);
// Visualización organizada del JSON
app.set('json spaces',2);

// Middlewares
// Mostrar por consola las solicitudes al servidor
app.use(morgan('dev'));
// Permitir recibir formatos tipo JSON
app.use(express.json());

// Rutas
app.use('/api/antecedentes/consultar',require('./routes/consultar'));
app.use('/api/antecedentes/resultados',require('./routes/resultados'));

// Inicializar el servidor
app.listen(app.get('port'),() => {
    console.log(`Server on port ${app.get('port')}`)
});  