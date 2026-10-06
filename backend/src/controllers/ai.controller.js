const { chatWithAI } = require("../services/aiService");

async function chat(req, res) {
    try {
        const result = await chatWithAI(req.body);

        res.json(result);
    } catch (error) {
        console.error("AI chat request failed:", error.message);

        if (error.status) {
            return res.status(error.status).json({
                message: error.message,
                error: error.details,
            });
        }

        if (error.message === "AI service request timed out") {
            return res.status(504).json({
                message: error.message,
            });
        }

        return res.status(503).json({
            message: error.message,
        });
    }
}

module.exports = {
    chat,
};