const express = require("express");
const multer = require("multer");

const {
    getAllDocuments,
    uploadDocument,
} = require("../controllers/document.controller");

const {
    upload,
    UNSUPPORTED_FILE_MESSAGE,
} = require("../middleware/documentUpload");

const router = express.Router();

const uploadFile = upload.single("file");

function handleUpload(req, res, next) {
    uploadFile(req, res, (error) => {
        if (!error) {
            return next();
        }

        if (
            error instanceof multer.MulterError &&
            error.code === "LIMIT_FILE_SIZE"
        ) {
            return res.status(413).json({
                message: "File is too large. Maximum size is 10 MB.",
            });
        }

        const message =
            error.message === UNSUPPORTED_FILE_MESSAGE
                ? error.message
                : "Invalid upload request.";

        return res.status(400).json({ message });
    });
}

router.get("/", getAllDocuments);

router.post(
    "/upload",
    handleUpload,
    uploadDocument
);

module.exports = router;
