/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
(self["webpackChunk_JUPYTERLAB_CORE_OUTPUT"] = self["webpackChunk_JUPYTERLAB_CORE_OUTPUT"] || []).push([["packages_docmanager-extension_lib_index_js-_654e0"],{

/***/ "../packages/docmanager-extension/lib/index.js":
/*!*****************************************************!*\
  !*** ../packages/docmanager-extension/lib/index.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"default\": () => (__WEBPACK_DEFAULT_EXPORT__)\n/* harmony export */ });\n/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ \"webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils\");\n/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/docmanager */ \"webpack/sharing/consume/default/@jupyterlab/docmanager/@jupyterlab/docmanager\");\n/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__);\n// Copyright (c) Jupyter Development Team.\n// Distributed under the terms of the Modified BSD License.\n\n\n/**\n * A plugin to open document in a new browser tab.\n *\n * TODO: remove and use a custom doc manager?\n */\nconst opener = {\n    id: '@jupyterlab-classic/docmanager-extension:opener',\n    requires: [_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__.IDocumentManager],\n    autoStart: true,\n    activate: (app, docManager) => {\n        const baseUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.getBaseUrl();\n        // patch the `docManager.open` option to prevent the default behavior\n        const docOpen = docManager.open;\n        docManager.open = (path, widgetName = 'default', kernel, options) => {\n            const ref = options === null || options === void 0 ? void 0 : options.ref;\n            if (ref === '_noref') {\n                docOpen.call(docManager, path, widgetName, kernel, options);\n                return;\n            }\n            const ext = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PathExt.extname(path);\n            const route = ext === '.ipynb' ? 'notebooks' : 'edit';\n            window.open(`${baseUrl}classic/${route}/${path}`);\n            return undefined;\n        };\n    }\n};\n/**\n * Export the plugins as default.\n */\nconst plugins = [opener];\n/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);\n\n\n//# sourceURL=webpack://_JUPYTERLAB.CORE_OUTPUT/../packages/docmanager-extension/lib/index.js?");

/***/ })

}]);