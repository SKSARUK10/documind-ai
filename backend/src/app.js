const express = require("express");
const cors = require("cors");

const healthRoutes = require("./routes/health.routes");
const aiRoutes = require("./routes/ai.routes")

const app = express()

app.use(cors())
app.use(express.json())

app.use("/", healthRoutes)
app.use("/api/ai", aiRoutes)

module.exports = app