const {
    getDocuments,
    uploadDocument: sendDocumentToAI,
} = require("../services/documentService");
async function getAllDocuments(req, res) {
    try {
        const documents = await getDocuments();

        res.json(documents);
    } catch (error) {
        console.error(
            "Document list request failed:",
            error.message
        );

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

async function uploadDocument(req, res) {
    try {
        if (!req.file) {
            return res.status(400).json({
                message: "PDF file is required",
            });
        }

        const document = await sendDocumentToAI(req.file);

        return res.status(201).json(document);
    } catch (error) {
        console.error(
            "Document upload request failed:",
            error.message
        );

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
    getAllDocuments,
    uploadDocument
};