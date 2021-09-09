const dboperations = require('./dboperations');

var express = require('express');
var bodyParser = require('body-parser');
var cors = require('cors');
var app = express();
var router = express.Router();

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(cors());
app.use('/api', router);

router.use((request, response, next)=>{
    //console.log('Middleware');
    next();
})

router.route('/lakes').get((request, response)=>{
    dboperations.getLakes().then(result => {
        //console.log(result);
        response.json(result[0]);
    })
})

router.route('/lakes/:id').get((request, response)=>{
    dboperations.getLake(request.params.id).then(result => {
        //console.log(result);
        response.json(result[0]);
    })
})

router.route('/lakes/:idL/measurement/:idM').get((request, response)=>{
    dboperations.getLastLakeMeasurement(request.params.idL, request.params.idM).then(result => {
        //console.log(result);
        response.json(result[0]);
    })
})

router.route('/lakes/:idL/parameter/:idP').get((request, response)=>{
    dboperations.getLastLakeParameter(request.params.idL, request.params.idP).then(result => {
        //console.log(result);
        response.json(result[0]);
    })
})

router.route('/lakesRank').get((request, response)=>{
    dboperations.getLastLakesRank().then(result => {
        //console.log(result);
        response.json(result[0]);
    })
})

router.route('/lakes/:idL/rank/:idR').get((request, response)=>{
    dboperations.getLastLakeRank(request.params.idL, request.params.idR).then(result => {
        //console.log(result);
        response.json(result[0]);
    })
})


var port = process.env.PORT || 8090;
app.listen(port);
console.log('LakeEye API is running and listening at ' + port);