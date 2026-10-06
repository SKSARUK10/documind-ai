const express = require("express");

const {
    getAllDocuments,
    uploadDocument,
} = require("../controllers/document.controller");

const { upload } = require("../middleware/documentUpload");

const router = express.Router();

router.get("/", getAllDocuments);

router.post(
    "/upload",
    upload.single("file"),
    uploadDocument
);

module.exports = router;