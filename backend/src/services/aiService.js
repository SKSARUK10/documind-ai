const axios = require("axios");

const AI_SERVICE_URL = process.env.AI_SERVICE_URL;

const aiClient = axios.create({
    baseURL: AI_SERVICE_URL,
    timeout: 30000,
});

async function chatWithAI(payload) {
    try {
        const response = await aiClient.post("/agent/chat", payload);

        return response.data;
    } catch (error) {
        if (error.code === "ECONNABORTED") {
            throw new Error("AI service request timed out");
        }

        if (error.response) {
            const serviceError = new Error("AI service returned an error");

            serviceError.status = error.response.status;
            serviceError.details = error.response.data;

            throw serviceError;
        }

        throw new Error("AI service is unavailable");
    }
}

module.exports = {
    chatWithAI,
};