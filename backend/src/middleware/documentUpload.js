const path = require("path");
const multer = require("multer");

const UNSUPPORTED_FILE_MESSAGE =
    "Only PDF, CSV, XLSX, and XLS files are allowed";

const ALLOWED_FILE_TYPES = {
    ".pdf": ["application/pdf"],
    ".csv": [
        "text/csv",
        "application/csv",
        "text/comma-separated-values",
        "application/vnd.ms-excel",
    ],
    ".xlsx": [
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ],
    ".xls": ["application/vnd.ms-excel"],
};

const upload = multer({
    storage: multer.memoryStorage(),

    limits: {
        fileSize: 10 * 1024 * 1024,
    },

    fileFilter: (req, file, cb) => {
        const extension = path
            .extname(file.originalname || "")
            .toLowerCase();

        const allowedTypes = ALLOWED_FILE_TYPES[extension];

        if (allowedTypes && allowedTypes.includes(file.mimetype)) {
            return cb(null, true);
        }

        return cb(new Error(UNSUPPORTED_FILE_MESSAGE));
    },
});

module.exports = {
    upload,
    UNSUPPORTED_FILE_MESSAGE,
};
