const {Router} = require('express');
const router = Router();
const _ = require('underscore');
const spawn = require("child_process").spawn;

router.post('/',(req, res) => {;
    let respuesta="";
    let errores=[];
    let status='';
    const body = req.body;
    const {primer_nombre,segundo_nombre,primer_apellido,segundo_apellido,documento,fecha_exp} = req.body;
    if(primer_nombre && primer_apellido && documento && fecha_exp){
        respuesta='SE GENERA CONSULTA'
        // console.log(body)
        status=200;
        let py_response = ""
        // Iniciar la ejecución del script de python
        const pythonProcess = spawn("Python",["generar_consulta.py"]);
        pythonProcess.stdin.write(JSON.stringify(body));
        pythonProcess.stdout.on('data',function(data){
            py_response += data.toString();
        });
        pythonProcess.stdout.on('end',function(data){
            console.log(py_response);
        });
        pythonProcess.stderr.on('data',function(data){
            console.log(data.toString());
        });           
        pythonProcess.stdin.end();
    }
    else {
        status=500;
        if(!primer_nombre){
            errores.push('primer nombre es un dato obligatorio');
        }
        if(!primer_apellido){
            errores.push('primer apellido es un dato obligatorio');
        }
        if(!documento){
            errores.push('documento es un dato obligatorio');
        }
        if(!fecha_exp){
            errores.push('fecha exp es un dato obligatorio');
        }
    }
    res.status(status).json({data:{results:respuesta},error:errores});
});

module.exports = router;