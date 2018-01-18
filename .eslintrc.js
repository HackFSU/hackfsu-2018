module.exports = {
    "env": {
        "es6": true,
        "node": true
    },
    "extends": "eslint:recommended",
    "parserOptions": {
        "sourceType": "module",
        "ecmaVersion": 8,
    },
    "rules": {
        "indent": [
            "error",
            4
        ],
        "linebreak-style": [
            "error",
            "unix"
        ],
        "quotes": [
            "warn",
            "single",
            { "allowTemplateLiterals": true }
        ],
        "semi": [
            "error",
            "always"
        ],
        "no-console": [
            "off"
        ],
        "no-unused-vars": [
            "warn"
        ]
    }
};
