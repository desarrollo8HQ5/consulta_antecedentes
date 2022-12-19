const {Router} = require('express');
const router = Router();
const _ = require('underscore');
const spawn = require("child_process").spawn;

router.get('/',(req, res) => {
    res.send('SOLICITUD GET - BUSCAR RESULTADOS');
});

module.exports = router;