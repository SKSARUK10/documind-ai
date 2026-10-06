const axios = require("axios");
const FormData = require("form-data");

const AI_SERVICE_URL = process.env.AI_SERVICE_URL;

const aiClient = axios.create({
    baseURL: AI_SERVICE_URL,
    timeout: 30000,
});

async function getDocuments() {
    try {
        const response = await aiClient.get("/documents");

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

async function uploadDocument(file) {
    try {
        const formData = new FormData();

        formData.append(
            "file",
            file.buffer,
            {
                filename: file.originalname,
                contentType: file.mimetype,
            }
        );

        const response = await aiClient.post(
            "/documents/upload",
            formData,
            {
                headers: formData.getHeaders(),
            }
        );

        return response.data;
    } catch (error) {
        if (error.code === "ECONNABORTED") {
            throw new Error("AI service request timed out");
        }

        if (error.response) {
            const serviceError = new Error(
                "AI service returned an error"
            );

            serviceError.status = error.response.status;
            serviceError.details = error.response.data;

            throw serviceError;
        }

        throw new Error("AI service is unavailable");
    }
}

module.exports = {
    getDocuments,
    uploadDocument,
};