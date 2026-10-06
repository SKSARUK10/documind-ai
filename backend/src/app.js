const express = require("express");
const cors = require("cors");

const healthRoutes = require("./routes/health.routes");
const aiRoutes = require("./routes/ai.routes")
const documentRoutes = require("./routes/document.routes")

const app = express()

app.disable("x-powered-by")

const allowedOrigins = (
    process.env.CORS_ORIGINS ||
    "http://localhost:5173,http://localhost:3000,http://localhost:4000"
)
    .split(",")
    .map((origin) => origin.trim())
    .filter(Boolean)

app.use(cors({
    origin: allowedOrigins,
}))
app.use(express.json())

app.use("/", healthRoutes)
app.use("/api/ai", aiRoutes)
app.use("/api/documents", documentRoutes)


module.exports = app
