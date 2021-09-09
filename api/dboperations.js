var config = require('./dbconfig')
const sql = require('mssql')

async function getLakes() {
    try{
        let pool = await sql.connect(config);
        let lakes = await pool.request().query('SELECT * FROM LAKE');
        return lakes.recordsets;
    }
    catch(error){
        console.log(error)
    }
}

async function getLake(lakeID){
    try{
        let pool = await sql.connect(config);
        let lake = await pool.request()
            .input('lID', sql.VarChar, lakeID)
            .query('SELECT * FROM LAKE WHERE ID = @lID');
        return lake.recordsets;
    }
    catch(error){
        console.log(error)
    }
}

async function getLastLakeMeasurement(lakeID, mID){
    try{
        let pool = await sql.connect(config);
        let lkm = await pool.request()
            .input('lID', sql.VarChar, lakeID)
            .input('mID', sql.Int, mID)
            .query('SELECT LM.LAKE_ID, L.NAME AS NAME, M.NAME AS MEASUREMENT, LM.LAT, LM.LON, LM.VAL_QTY, LM.MEASUREMENT_DT AS LAST_DT FROM LAKE_MEASUREMENT LM JOIN LAKE L ON LM.LAKE_ID=L.ID JOIN MEASUREMENT M ON LM.MEASUREMENT_ID = M.ID INNER JOIN (SELECT LM.LAKE_ID, M.NAME AS MEASUREMENT, MAX(LM.MEASUREMENT_DT) LAST_DT FROM LAKE_MEASUREMENT LM JOIN LAKE L ON LM.LAKE_ID=L.ID JOIN MEASUREMENT M ON LM.MEASUREMENT_ID = M.ID GROUP BY LM.LAKE_ID, M.NAME) A ON L.ID = A.LAKE_ID AND M.NAME = A.MEASUREMENT AND LM.MEASUREMENT_DT = A.LAST_DT WHERE L.ID = @lID AND M.ID = @mID ORDER BY LM.LAKE_ID, M.NAME')
        return lkm.recordsets;
    }
    catch(error){
        console.log(error)
    }
}

async function getLastLakeParameter(lakeID, paramID){
    try{
        let pool = await sql.connect(config);
        let lkp = await pool.request()
            .input('lID', sql.VarChar, lakeID)
            .input('pID', sql.Int, paramID)
            .query('SELECT LP.LAKE_ID, L.NAME AS NAME, LP.MODEL, P.NAME AS PARAMETER, LP.VAL_NUM, LP.MODIFICATION_DT FROM LAKE_PARAMETER LP JOIN LAKE L ON LP.LAKE_ID = L.ID JOIN PARAMETER P ON LP.PARAMETER_ID = P.ID INNER JOIN(SELECT LP.LAKE_ID, P.NAME AS PARAMETER, MAX(LP.MODIFICATION_DT) LAST_DT FROM LAKE_PARAMETER LP JOIN LAKE L ON LP.LAKE_ID = L.ID JOIN PARAMETER P ON LP.PARAMETER_ID = P.ID GROUP BY LP.LAKE_ID, P.NAME) A ON LP.LAKE_ID = A.LAKE_ID AND P.NAME = A.PARAMETER AND LP.MODIFICATION_DT = A.LAST_DT WHERE LP.LAKE_ID = @lID AND P.ID = @pID')
        return lkp.recordsets;
    }
    catch(error){
        console.log(error)
    }
}

async function getLastLakeRank(lakeID, rankID){
    try{
        let pool = await sql.connect(config);
        let lkr = await pool.request()
            .input('lID', sql.VarChar, lakeID)
            .input('rID', sql.Int, rankID)
            .query('SELECT LR.LAKE_ID, L.NAME, R.NAME AS RANK, LR.VAL_NUM, LR.MODIFICATION_DT FROM LAKE_RANK LR JOIN LAKE L ON LR.LAKE_ID = L.ID JOIN RANK R ON LR.RANK_ID = R.ID INNER JOIN (SELECT LR.LAKE_ID, R.ID, MAX(LR.MODIFICATION_DT) AS LAST_DT FROM LAKE_RANK LR JOIN LAKE L ON LR.LAKE_ID = L.ID JOIN RANK R ON LR.RANK_ID = R.ID GROUP BY LR.LAKE_ID, R.ID) A ON LR.LAKE_ID = A.LAKE_ID AND R.ID = A.ID AND LR.MODIFICATION_DT = A.LAST_DT WHERE LR.LAKE_ID = @lID AND R.ID = @rID')
        return lkr.recordsets;
    }
    catch(error){
        console.log(error)
    }
}

async function getLastLakesRank(){
    try{
        let pool = await sql.connect(config);
        let lkr = await pool.request()
            .query('SELECT R1.LAKE_ID,R1.NAME,R1.RANK1,ROUND(LP.VAL_NUM, 2) AS RANK1PCT,R2.RANK2,R1.MODIFICATION_DT FROM (SELECT LR.LAKE_ID, L.NAME, LR.VAL_NUM AS RANK1, LR.MODIFICATION_DT FROM LAKE_RANK LR JOIN LAKE L ON LR.LAKE_ID = L.ID JOIN RANK R ON LR.RANK_ID = R.ID INNER JOIN (SELECT LR.LAKE_ID, R.ID, MAX(LR.MODIFICATION_DT) AS LAST_DT FROM LAKE_RANK LR JOIN LAKE L ON LR.LAKE_ID = L.ID JOIN RANK R ON LR.RANK_ID = R.ID GROUP BY LR.LAKE_ID, R.ID) A ON LR.LAKE_ID = A.LAKE_ID AND R.ID = A.ID AND LR.MODIFICATION_DT = A.LAST_DT WHERE R.ID = 1) R1 JOIN (SELECT LR.LAKE_ID, L.NAME, LR.VAL_NUM AS RANK2, LR.MODIFICATION_DT FROM LAKE_RANK LR JOIN LAKE L ON LR.LAKE_ID = L.ID JOIN RANK R ON LR.RANK_ID = R.ID INNER JOIN (SELECT LR.LAKE_ID, R.ID, MAX(LR.MODIFICATION_DT) AS LAST_DT FROM LAKE_RANK LR JOIN LAKE L ON LR.LAKE_ID = L.ID JOIN RANK R ON LR.RANK_ID = R.ID GROUP BY LR.LAKE_ID, R.ID) A ON LR.LAKE_ID = A.LAKE_ID AND R.ID = A.ID AND LR.MODIFICATION_DT = A.LAST_DT WHERE R.ID = 2) R2 ON R1.LAKE_ID = R2.LAKE_ID AND R1.MODIFICATION_DT = R2.MODIFICATION_DT JOIN LAKE_PARAMETER LP ON R1.LAKE_ID = LP.LAKE_ID AND R1.MODIFICATION_DT = LP.MODIFICATION_DT AND LP.PARAMETER_ID = 1')
        return lkr.recordsets;
    }
    catch(error){
        console.log(error)
    }
}

module.exports = {
    getLakes: getLakes,
    getLake: getLake,
    getLastLakeMeasurement: getLastLakeMeasurement,
    getLastLakeParameter: getLastLakeParameter,
    getLastLakeRank: getLastLakeRank,
    getLastLakesRank: getLastLakesRank
}