const express = require("express")

const router = express.Router();

router.get("/health",(req,res)=>{
res.json({
    status :"Okay",
    server:"Documind-AI"
})
})

module.exports = router;

