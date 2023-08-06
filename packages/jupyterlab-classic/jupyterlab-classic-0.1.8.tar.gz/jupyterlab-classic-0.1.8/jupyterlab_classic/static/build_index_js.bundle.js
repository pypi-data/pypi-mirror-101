/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
(self["webpackChunk_JUPYTERLAB_CORE_OUTPUT"] = self["webpackChunk_JUPYTERLAB_CORE_OUTPUT"] || []).push([["build_index_js"],{

/***/ "./build/extraStyle.js":
/*!*****************************!*\
  !*** ./build/extraStyle.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _jupyterlab_celltags_style_index_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/celltags/style/index.js */ \"../node_modules/@jupyterlab/celltags/style/index.js\");\n\n\n\n//# sourceURL=webpack://_JUPYTERLAB.CORE_OUTPUT/./build/extraStyle.js?");

/***/ }),

/***/ "./build/index.js":
/*!************************!*\
  !*** ./build/index.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ \"webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils\");\n/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);\n// Copyright (c) Jupyter Development Team.\n// Distributed under the terms of the Modified BSD License.\n\n// Inspired by: https://github.com/jupyterlab/jupyterlab/blob/master/dev_mode/index.js\n\n\n\n// Promise.allSettled polyfill, until our supported browsers implement it\n// See https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/allSettled\nif (Promise.allSettled === undefined) {\n  Promise.allSettled = promises =>\n    Promise.all(\n      promises.map(promise =>\n        promise.then(\n          value => ({\n            status: 'fulfilled',\n            value\n          }),\n          reason => ({\n            status: 'rejected',\n            reason\n          })\n        )\n      )\n    );\n}\n\n__webpack_require__(/*! ./style.js */ \"./build/style.js\");\n__webpack_require__(/*! ./extraStyle.js */ \"./build/extraStyle.js\");\n\nfunction loadScript(url) {\n  return new Promise((resolve, reject) => {\n    const newScript = document.createElement('script');\n    newScript.onerror = reject;\n    newScript.onload = resolve;\n    newScript.async = true;\n    document.head.appendChild(newScript);\n    newScript.src = url;\n  });\n}\nasync function loadComponent(url, scope) {\n  await loadScript(url);\n\n  // From MIT-licensed https://github.com/module-federation/module-federation-examples/blob/af043acd6be1718ee195b2511adf6011fba4233c/advanced-api/dynamic-remotes/app1/src/App.js#L6-L12\n  // eslint-disable-next-line no-undef\n  await __webpack_require__.I('default');\n  const container = window._JUPYTERLAB[scope];\n  // Initialize the container, it may provide shared modules and may need ours\n  // eslint-disable-next-line no-undef\n  await container.init(__webpack_require__.S.default);\n}\n\nasync function createModule(scope, module) {\n  try {\n    const factory = await window._JUPYTERLAB[scope].get(module);\n    return factory();\n  } catch (e) {\n    console.warn(\n      `Failed to create module: package: ${scope}; module: ${module}`\n    );\n    throw e;\n  }\n}\n\n/**\n * The main function\n */\nasync function main() {\n  // load extra packages\n  __webpack_require__(/*! @jupyterlab/celltags */ \"webpack/sharing/consume/default/@jupyterlab/celltags/@jupyterlab/celltags\");\n\n  const App = __webpack_require__(/*! @jupyterlab-classic/application */ \"webpack/sharing/consume/default/@jupyterlab-classic/application/@jupyterlab-classic/application\").App;\n  const app = new App();\n\n  const disabled = [];\n  // TODO: formalize the way the set of initial extensions and plugins are specified\n  let mods = [\n    // @jupyterlab-classic plugins\n    __webpack_require__(/*! @jupyterlab-classic/application-extension */ \"webpack/sharing/consume/default/@jupyterlab-classic/application-extension/@jupyterlab-classic/application-extension\"),\n    __webpack_require__(/*! @jupyterlab-classic/docmanager-extension */ \"webpack/sharing/consume/default/@jupyterlab-classic/docmanager-extension/@jupyterlab-classic/docmanager-extension\"),\n    __webpack_require__(/*! @jupyterlab-classic/help-extension */ \"webpack/sharing/consume/default/@jupyterlab-classic/help-extension/@jupyterlab-classic/help-extension\"),\n    __webpack_require__(/*! @jupyterlab-classic/notebook-extension */ \"webpack/sharing/consume/default/@jupyterlab-classic/notebook-extension/@jupyterlab-classic/notebook-extension\"),\n    // to handle opening new tabs after creating a new terminal\n    __webpack_require__(/*! @jupyterlab-classic/terminal-extension */ \"webpack/sharing/consume/default/@jupyterlab-classic/terminal-extension/@jupyterlab-classic/terminal-extension\"),\n\n    // @jupyterlab plugins\n    __webpack_require__(/*! @jupyterlab/apputils-extension */ \"webpack/sharing/consume/default/@jupyterlab/apputils-extension/@jupyterlab/apputils-extension\").default.filter(({ id }) =>\n      [\n        '@jupyterlab/apputils-extension:palette',\n        '@jupyterlab/apputils-extension:settings',\n        '@jupyterlab/apputils-extension:themes',\n        '@jupyterlab/apputils-extension:themes-palette-menu'\n      ].includes(id)\n    ),\n    __webpack_require__(/*! @jupyterlab/codemirror-extension */ \"webpack/sharing/consume/default/@jupyterlab/codemirror-extension/@jupyterlab/codemirror-extension\").default.filter(({ id }) =>\n      [\n        '@jupyterlab/codemirror-extension:services',\n        '@jupyterlab/codemirror-extension:codemirror'\n      ].includes(id)\n    ),\n    __webpack_require__(/*! @jupyterlab/completer-extension */ \"webpack/sharing/consume/default/@jupyterlab/completer-extension/@jupyterlab/completer-extension\").default.filter(({ id }) =>\n      ['@jupyterlab/completer-extension:manager'].includes(id)\n    ),\n    __webpack_require__(/*! @jupyterlab/docmanager-extension */ \"webpack/sharing/consume/default/@jupyterlab/docmanager-extension/@jupyterlab/docmanager-extension\").default.filter(({ id }) =>\n      ['@jupyterlab/docmanager-extension:plugin'].includes(id)\n    ),\n    __webpack_require__(/*! @jupyterlab/mainmenu-extension */ \"webpack/sharing/consume/default/@jupyterlab/mainmenu-extension/@jupyterlab/mainmenu-extension\"),\n    __webpack_require__(/*! @jupyterlab/mathjax2-extension */ \"webpack/sharing/consume/default/@jupyterlab/mathjax2-extension/@jupyterlab/mathjax2-extension\"),\n    __webpack_require__(/*! @jupyterlab/notebook-extension */ \"webpack/sharing/consume/default/@jupyterlab/notebook-extension/@jupyterlab/notebook-extension\").default.filter(({ id }) =>\n      [\n        '@jupyterlab/notebook-extension:factory',\n        '@jupyterlab/notebook-extension:tracker',\n        '@jupyterlab/notebook-extension:widget-factory'\n      ].includes(id)\n    ),\n    __webpack_require__(/*! @jupyterlab/rendermime-extension */ \"webpack/sharing/consume/default/@jupyterlab/rendermime-extension/@jupyterlab/rendermime-extension\"),\n    __webpack_require__(/*! @jupyterlab/shortcuts-extension */ \"webpack/sharing/consume/default/@jupyterlab/shortcuts-extension/@jupyterlab/shortcuts-extension\"),\n    // so new terminals can be create from the menu\n    __webpack_require__(/*! @jupyterlab/terminal-extension */ \"webpack/sharing/consume/default/@jupyterlab/terminal-extension/@jupyterlab/terminal-extension\"),\n    __webpack_require__(/*! @jupyterlab/theme-light-extension */ \"webpack/sharing/consume/default/@jupyterlab/theme-light-extension/@jupyterlab/theme-light-extension\"),\n    __webpack_require__(/*! @jupyterlab/theme-dark-extension */ \"webpack/sharing/consume/default/@jupyterlab/theme-dark-extension/@jupyterlab/theme-dark-extension\")\n  ];\n\n  // The motivation here is to only load a specific set of plugins dependending on\n  // the current page\n  const page = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.getOption('classicPage');\n  if (page === 'tree') {\n    mods = mods.concat([\n      __webpack_require__(/*! @jupyterlab-classic/tree-extension */ \"webpack/sharing/consume/default/@jupyterlab-classic/tree-extension/@jupyterlab-classic/tree-extension\"),\n      __webpack_require__(/*! @jupyterlab/running-extension */ \"webpack/sharing/consume/default/@jupyterlab/running-extension/@jupyterlab/running-extension\")\n    ]);\n  } else if (page === 'notebooks') {\n    mods = mods.concat([\n      __webpack_require__(/*! @jupyterlab/completer-extension */ \"webpack/sharing/consume/default/@jupyterlab/completer-extension/@jupyterlab/completer-extension\").default.filter(({ id }) =>\n        ['@jupyterlab/completer-extension:notebooks'].includes(id)\n      ),\n      __webpack_require__(/*! @jupyterlab/tooltip-extension */ \"webpack/sharing/consume/default/@jupyterlab/tooltip-extension/@jupyterlab/tooltip-extension\").default.filter(({ id }) =>\n        [\n          '@jupyterlab/tooltip-extension:manager',\n          '@jupyterlab/tooltip-extension:notebooks'\n        ].includes(id)\n      )\n    ]);\n  } else if (page === 'edit') {\n    mods = mods.concat([\n      __webpack_require__(/*! @jupyterlab/completer-extension */ \"webpack/sharing/consume/default/@jupyterlab/completer-extension/@jupyterlab/completer-extension\").default.filter(({ id }) =>\n        ['@jupyterlab/completer-extension:files'].includes(id)\n      ),\n      __webpack_require__(/*! @jupyterlab/fileeditor-extension */ \"webpack/sharing/consume/default/@jupyterlab/fileeditor-extension/@jupyterlab/fileeditor-extension\").default.filter(({ id }) =>\n        ['@jupyterlab/fileeditor-extension:plugin'].includes(id)\n      ),\n      __webpack_require__(/*! @jupyterlab-classic/tree-extension */ \"webpack/sharing/consume/default/@jupyterlab-classic/tree-extension/@jupyterlab-classic/tree-extension\").default.filter(({ id }) =>\n        ['@jupyterlab-classic/tree-extension:factory'].includes(id)\n      )\n    ]);\n  }\n\n  /**\n   * Iterate over active plugins in an extension.\n   *\n   * #### Notes\n   * This also populates the disabled\n   */\n  function* activePlugins(extension) {\n    // Handle commonjs or es2015 modules\n    let exports;\n    if (Object.prototype.hasOwnProperty.call(extension, '__esModule')) {\n      exports = extension.default;\n    } else {\n      // CommonJS exports.\n      exports = extension;\n    }\n\n    let plugins = Array.isArray(exports) ? exports : [exports];\n    for (let plugin of plugins) {\n      if (_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.Extension.isDisabled(plugin.id)) {\n        disabled.push(plugin.id);\n        continue;\n      }\n      yield plugin;\n    }\n  }\n\n  const extension_data = JSON.parse(\n    _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.getOption('federated_extensions')\n  );\n\n  const federatedExtensionPromises = [];\n  const federatedMimeExtensionPromises = [];\n  const federatedStylePromises = [];\n\n  const extensions = await Promise.allSettled(\n    extension_data.map(async data => {\n      await loadComponent(\n        `${_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(\n          _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.getOption('fullLabextensionsUrl'),\n          data.name,\n          data.load\n        )}`,\n        data.name\n      );\n      return data;\n    })\n  );\n\n  extensions.forEach(p => {\n    if (p.status === 'rejected') {\n      // There was an error loading the component\n      console.error(p.reason);\n      return;\n    }\n\n    const data = p.value;\n    if (data.extension) {\n      federatedExtensionPromises.push(createModule(data.name, data.extension));\n    }\n    if (data.mimeExtension) {\n      federatedMimeExtensionPromises.push(\n        createModule(data.name, data.mimeExtension)\n      );\n    }\n    if (data.style) {\n      federatedStylePromises.push(createModule(data.name, data.style));\n    }\n  });\n\n  // Add the federated extensions.\n  // TODO: Add support for disabled extensions\n  const federatedExtensions = await Promise.allSettled(\n    federatedExtensionPromises\n  );\n  federatedExtensions.forEach(p => {\n    if (p.status === 'fulfilled') {\n      for (let plugin of activePlugins(p.value)) {\n        mods.push(plugin);\n      }\n    } else {\n      console.error(p.reason);\n    }\n  });\n\n  // Load all federated component styles and log errors for any that do not\n  (await Promise.allSettled(federatedStylePromises))\n    .filter(({ status }) => status === 'rejected')\n    .forEach(({ reason }) => {\n      console.error(reason);\n    });\n\n  app.registerPluginModules(mods);\n\n  await app.start();\n}\n\nwindow.addEventListener('load', main);\n\n\n//# sourceURL=webpack://_JUPYTERLAB.CORE_OUTPUT/./build/index.js?");

/***/ }),

/***/ "./build/style.js":
/*!************************!*\
  !*** ./build/style.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _jupyterlab_classic_application_extension_style_index_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab-classic/application-extension/style/index.js */ \"../packages/application-extension/style/index.js\");\n/* harmony import */ var _jupyterlab_classic_application_style_index_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab-classic/application/style/index.js */ \"../packages/application/style/index.js\");\n/* harmony import */ var _jupyterlab_classic_docmanager_extension_style_index_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab-classic/docmanager-extension/style/index.js */ \"../packages/docmanager-extension/style/index.js\");\n/* harmony import */ var _jupyterlab_classic_help_extension_style_index_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab-classic/help-extension/style/index.js */ \"../packages/help-extension/style/index.js\");\n/* harmony import */ var _jupyterlab_classic_notebook_extension_style_index_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab-classic/notebook-extension/style/index.js */ \"../packages/notebook-extension/style/index.js\");\n/* harmony import */ var _jupyterlab_classic_terminal_extension_style_index_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab-classic/terminal-extension/style/index.js */ \"../packages/terminal-extension/style/index.js\");\n/* harmony import */ var _jupyterlab_classic_tree_extension_style_index_js__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab-classic/tree-extension/style/index.js */ \"../packages/tree-extension/style/index.js\");\n/* harmony import */ var _jupyterlab_classic_ui_components_style_index_js__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab-classic/ui-components/style/index.js */ \"../packages/ui-components/style/index.js\");\n/* harmony import */ var _jupyterlab_apputils_extension_style_index_js__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @jupyterlab/apputils-extension/style/index.js */ \"../node_modules/@jupyterlab/apputils-extension/style/index.js\");\n/* harmony import */ var _jupyterlab_codemirror_extension_style_index_js__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @jupyterlab/codemirror-extension/style/index.js */ \"../node_modules/@jupyterlab/codemirror-extension/style/index.js\");\n/* harmony import */ var _jupyterlab_completer_extension_style_index_js__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @jupyterlab/completer-extension/style/index.js */ \"../node_modules/@jupyterlab/completer-extension/style/index.js\");\n/* harmony import */ var _jupyterlab_docmanager_extension_style_index_js__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @jupyterlab/docmanager-extension/style/index.js */ \"../node_modules/@jupyterlab/docmanager-extension/style/index.js\");\n/* harmony import */ var _jupyterlab_fileeditor_extension_style_index_js__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @jupyterlab/fileeditor-extension/style/index.js */ \"../node_modules/@jupyterlab/fileeditor-extension/style/index.js\");\n/* harmony import */ var _jupyterlab_mainmenu_extension_style_index_js__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @jupyterlab/mainmenu-extension/style/index.js */ \"../node_modules/@jupyterlab/mainmenu-extension/style/index.js\");\n/* harmony import */ var _jupyterlab_mathjax2_extension_style_index_js__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @jupyterlab/mathjax2-extension/style/index.js */ \"../node_modules/@jupyterlab/mathjax2-extension/style/index.js\");\n/* harmony import */ var _jupyterlab_notebook_extension_style_index_js__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @jupyterlab/notebook-extension/style/index.js */ \"../node_modules/@jupyterlab/notebook-extension/style/index.js\");\n/* harmony import */ var _jupyterlab_rendermime_extension_style_index_js__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! @jupyterlab/rendermime-extension/style/index.js */ \"../node_modules/@jupyterlab/rendermime-extension/style/index.js\");\n/* harmony import */ var _jupyterlab_running_extension_style_index_js__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! @jupyterlab/running-extension/style/index.js */ \"../node_modules/@jupyterlab/running-extension/style/index.js\");\n/* harmony import */ var _jupyterlab_terminal_extension_style_index_js__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! @jupyterlab/terminal-extension/style/index.js */ \"../node_modules/@jupyterlab/terminal-extension/style/index.js\");\n/* harmony import */ var _jupyterlab_tooltip_extension_style_index_js__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! @jupyterlab/tooltip-extension/style/index.js */ \"../node_modules/@jupyterlab/tooltip-extension/style/index.js\");\n/* This is a generated file of CSS imports */\n/* It was generated by @jupyterlab/builder in Build.ensureAssets() */\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n//# sourceURL=webpack://_JUPYTERLAB.CORE_OUTPUT/./build/style.js?");

/***/ }),

/***/ "../node_modules/css-loader/dist/cjs.js!../packages/application-extension/style/base.css":
/*!***********************************************************************************************!*\
  !*** ../node_modules/css-loader/dist/cjs.js!../packages/application-extension/style/base.css ***!
  \***********************************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"default\": () => (__WEBPACK_DEFAULT_EXPORT__)\n/* harmony export */ });\n/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../node_modules/css-loader/dist/runtime/api.js */ \"../node_modules/css-loader/dist/runtime/api.js\");\n/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__);\n// Imports\n\nvar ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default()(function(i){return i[1]});\n// Module\n___CSS_LOADER_EXPORT___.push([module.id, \"/*-----------------------------------------------------------------------------\\n| Copyright (c) Jupyter Development Team.\\n|\\n| Distributed under the terms of the Modified BSD License.\\n|----------------------------------------------------------------------------*/\\n\\n.jp-ClassicSpacer {\\n  flex-grow: 1;\\n  flex-shrink: 1;\\n}\\n\\n.jp-MainAreaWidget {\\n  height: 100%;\\n}\\n\", \"\"]);\n// Exports\n/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);\n\n\n//# sourceURL=webpack://_JUPYTERLAB.CORE_OUTPUT/../packages/application-extension/style/base.css?../node_modules/css-loader/dist/cjs.js");

/***/ }),

/***/ "../node_modules/css-loader/dist/cjs.js!../packages/application/style/base.css":
/*!*************************************************************************************!*\
  !*** ../node_modules/css-loader/dist/cjs.js!../packages/application/style/base.css ***!
  \*************************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"default\": () => (__WEBPACK_DEFAULT_EXPORT__)\n/* harmony export */ });\n/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../node_modules/css-loader/dist/runtime/api.js */ \"../node_modules/css-loader/dist/runtime/api.js\");\n/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__);\n// Imports\n\nvar ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default()(function(i){return i[1]});\n// Module\n___CSS_LOADER_EXPORT___.push([module.id, \"/*-----------------------------------------------------------------------------\\n| Copyright (c) Jupyter Development Team.\\n| Distributed under the terms of the Modified BSD License.\\n|----------------------------------------------------------------------------*/\\n\\n:root {\\n  --jp-private-topbar-height: 28px;\\n  /* Override the layout-2 color for the dark theme */\\n  --md-grey-800: #323232;\\n}\\n\\nbody {\\n  margin: 0;\\n  padding: 0;\\n  background: var(--jp-layout-color2);\\n}\\n\\n#main {\\n  position: absolute;\\n  top: 0;\\n  left: 0;\\n  right: 0;\\n  bottom: 0;\\n}\\n\\n#top-panel-wrapper {\\n  min-height: calc(1.5 * var(--jp-private-topbar-height));\\n  border-bottom: var(--jp-border-width) solid var(--jp-border-color0);\\n  background: var(--jp-layout-color1);\\n}\\n\\n#top-panel {\\n  display: flex;\\n  min-height: calc(1.5 * var(--jp-private-topbar-height));\\n  padding-left: 5px;\\n  padding-right: 5px;\\n  margin-left: auto;\\n  margin-right: auto;\\n  max-width: 1200px;\\n}\\n\\n#menu-panel-wrapper {\\n  min-height: var(--jp-private-topbar-height);\\n  background: var(--jp-layout-color1);\\n  border-bottom: var(--jp-border-width) solid var(--jp-border-color0);\\n  box-shadow: var(--jp-elevation-z1);\\n}\\n\\n#menu-panel {\\n  display: flex;\\n  min-height: var(--jp-private-topbar-height);\\n  background: var(--jp-layout-color1);\\n  padding-left: 5px;\\n  padding-right: 5px;\\n  margin-left: auto;\\n  margin-right: auto;\\n  max-width: 1200px;\\n}\\n\\n#main-panel {\\n  box-shadow: var(--jp-elevation-z4);\\n  margin-left: auto;\\n  margin-right: auto;\\n  max-width: 1200px;\\n}\\n\\n#spacer-widget {\\n  min-height: 16px;\\n}\\n\", \"\"]);\n// Exports\n/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);\n\n\n//# sourceURL=webpack://_JUPYTERLAB.CORE_OUTPUT/../packages/application/style/base.css?../node_modules/css-loader/dist/cjs.js");

/***/ }),

/***/ "../node_modules/css-loader/dist/cjs.js!../packages/docmanager-extension/style/base.css":
/*!**********************************************************************************************!*\
  !*** ../node_modules/css-loader/dist/cjs.js!../packages/docmanager-extension/style/base.css ***!
  \**********************************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"default\": () => (__WEBPACK_DEFAULT_EXPORT__)\n/* harmony export */ });\n/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../node_modules/css-loader/dist/runtime/api.js */ \"../node_modules/css-loader/dist/runtime/api.js\");\n/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__);\n// Imports\n\nvar ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default()(function(i){return i[1]});\n// Module\n___CSS_LOADER_EXPORT___.push([module.id, \".jp-Document {\\n  height: 100%;\\n}\\n\", \"\"]);\n// Exports\n/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);\n\n\n//# sourceURL=webpack://_JUPYTERLAB.CORE_OUTPUT/../packages/docmanager-extension/style/base.css?../node_modules/css-loader/dist/cjs.js");

/***/ }),

/***/ "../node_modules/css-loader/dist/cjs.js!../packages/help-extension/style/base.css":
/*!****************************************************************************************!*\
  !*** ../node_modules/css-loader/dist/cjs.js!../packages/help-extension/style/base.css ***!
  \****************************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"default\": () => (__WEBPACK_DEFAULT_EXPORT__)\n/* harmony export */ });\n/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../node_modules/css-loader/dist/runtime/api.js */ \"../node_modules/css-loader/dist/runtime/api.js\");\n/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__);\n// Imports\n\nvar ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default()(function(i){return i[1]});\n// Module\n___CSS_LOADER_EXPORT___.push([module.id, \".jp-AboutClassic-header {\\n  display: flex;\\n  flex-direction: row;\\n  align-items: center;\\n  padding: var(--jp-flat-button-padding);\\n}\\n\\n.jp-AboutClassic-header-text {\\n  margin-left: 16px;\\n}\\n\\n.jp-AboutClassic-body {\\n  display: flex;\\n  font-size: var(--jp-ui-font-size2);\\n  padding: var(--jp-flat-button-padding);\\n  color: var(--jp-ui-font-color1);\\n  text-align: left;\\n  flex-direction: column;\\n  min-width: 360px;\\n  overflow: hidden;\\n}\\n\\n.jp-AboutClassic-about-body pre {\\n  white-space: pre-wrap;\\n}\\n\\n.jp-AboutClassic-about-externalLinks {\\n  display: flex;\\n  flex-direction: column;\\n  justify-content: flex-start;\\n  align-items: flex-start;\\n  padding-top: 12px;\\n  color: var(--jp-warn-color0);\\n}\\n\\n.jp-AboutClassic-shortcuts {\\n  padding: 10px;\\n}\\n\\n.jp-AboutClassic-shortcuts pre {\\n  padding: 5px;\\n  margin: 0 0 10px;\\n  background: var(--jp-layout-color2);\\n  border: 1px solid var(--jp-border-color0);\\n  border-radius: 2px;\\n  word-break: break-all;\\n}\\n\", \"\"]);\n// Exports\n/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);\n\n\n//# sourceURL=webpack://_JUPYTERLAB.CORE_OUTPUT/../packages/help-extension/style/base.css?../node_modules/css-loader/dist/cjs.js");

/***/ }),

/***/ "../node_modules/css-loader/dist/cjs.js!../packages/notebook-extension/style/base.css":
/*!********************************************************************************************!*\
  !*** ../node_modules/css-loader/dist/cjs.js!../packages/notebook-extension/style/base.css ***!
  \********************************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"default\": () => (__WEBPACK_DEFAULT_EXPORT__)\n/* harmony export */ });\n/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../node_modules/css-loader/dist/runtime/api.js */ \"../node_modules/css-loader/dist/runtime/api.js\");\n/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__);\n// Imports\n\nvar ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default()(function(i){return i[1]});\n// Module\n___CSS_LOADER_EXPORT___.push([module.id, \"/*-----------------------------------------------------------------------------\\n| Copyright (c) Jupyter Development Team.\\n|\\n| Distributed under the terms of the Modified BSD License.\\n|----------------------------------------------------------------------------*/\\n\\n.jp-ClassicKernelLogo {\\n  flex: 0 0 auto;\\n  display: flex;\\n  align-items: center;\\n  text-align: center;\\n  margin-right: 8px;\\n}\\n\\n.jp-ClassicKernelLogo img {\\n  max-width: 28px;\\n  max-height: 28px;\\n  display: flex;\\n}\\n\\n.jp-ClassicKernelStatus {\\n  font-size: var(--jp-ui-font-size1);\\n  margin: 0;\\n  font-weight: normal;\\n  color: var(--jp-ui-font-color0);\\n  font-family: var(--jp-ui-font-family);\\n  line-height: var(--jp-private-title-panel-height);\\n  padding-left: 5px;\\n  padding-right: 5px;\\n}\\n\\n.jp-ClassicKernelStatus-error {\\n  background-color: var(--jp-error-color0);\\n}\\n\\n.jp-ClassicKernelStatus-warn {\\n  background-color: var(--jp-warn-color0);\\n}\\n\\n.jp-ClassicKernelStatus-info {\\n  background-color: var(--jp-info-color0);\\n}\\n\\n.jp-ClassicKernelStatus-fade {\\n  animation: 0.5s fade-out forwards;\\n}\\n\\n@keyframes fade-out {\\n  0% {\\n    opacity: 1;\\n  }\\n  100% {\\n    opacity: 0;\\n  }\\n}\\n\\n#jp-title h1 {\\n  cursor: pointer;\\n  font-size: 18px;\\n  margin: 0;\\n  font-weight: normal;\\n  color: var(--jp-ui-font-color0);\\n  font-family: var(--jp-ui-font-family);\\n  line-height: calc(1.5 * var(--jp-private-title-panel-height));\\n  text-overflow: ellipsis;\\n  overflow: hidden;\\n  white-space: nowrap;\\n}\\n\\n#jp-title h1:hover {\\n  background: var(--jp-layout-color2);\\n}\\n\\n.jp-ClassicCheckpoint {\\n  font-size: 14px;\\n  margin-left: 5px;\\n  margin-right: 5px;\\n  font-weight: normal;\\n  color: var(--jp-ui-font-color0);\\n  font-family: var(--jp-ui-font-family);\\n  line-height: calc(1.5 * var(--jp-private-title-panel-height));\\n  text-overflow: ellipsis;\\n  overflow: hidden;\\n  white-space: nowrap;\\n}\\n\\n/* Mobile View */\\n\\nbody[data-format='mobile'] .jp-ClassicCheckpoint {\\n  display: none;\\n}\\n\\nbody[data-format='mobile'] .jp-InputArea,\\nbody[data-format='mobile'] .jp-OutputArea-child {\\n  flex-direction: column;\\n}\\n\\nbody[data-format='mobile'] .jp-InputPrompt,\\nbody[data-format='mobile'] .jp-OutputPrompt {\\n  flex: 0 0 auto;\\n  text-align: left;\\n}\\n\\nbody[data-format='mobile'] .jp-InputArea-editor {\\n  margin-left: var(--jp-notebook-padding);\\n}\\n\\nbody[data-format='mobile'] .jp-OutputArea-child .jp-OutputArea-output {\\n  margin-left: var(--jp-notebook-padding);\\n}\\n\", \"\"]);\n// Exports\n/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);\n\n\n//# sourceURL=webpack://_JUPYTERLAB.CORE_OUTPUT/../packages/notebook-extension/style/base.css?../node_modules/css-loader/dist/cjs.js");

/***/ }),

/***/ "../node_modules/css-loader/dist/cjs.js!../packages/terminal-extension/style/base.css":
/*!********************************************************************************************!*\
  !*** ../node_modules/css-loader/dist/cjs.js!../packages/terminal-extension/style/base.css ***!
  \********************************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"default\": () => (__WEBPACK_DEFAULT_EXPORT__)\n/* harmony export */ });\n/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../node_modules/css-loader/dist/runtime/api.js */ \"../node_modules/css-loader/dist/runtime/api.js\");\n/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__);\n// Imports\n\nvar ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default()(function(i){return i[1]});\n// Module\n___CSS_LOADER_EXPORT___.push([module.id, \"\", \"\"]);\n// Exports\n/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);\n\n\n//# sourceURL=webpack://_JUPYTERLAB.CORE_OUTPUT/../packages/terminal-extension/style/base.css?../node_modules/css-loader/dist/cjs.js");

/***/ }),

/***/ "../node_modules/css-loader/dist/cjs.js!../packages/tree-extension/style/base.css":
/*!****************************************************************************************!*\
  !*** ../node_modules/css-loader/dist/cjs.js!../packages/tree-extension/style/base.css ***!
  \****************************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"default\": () => (__WEBPACK_DEFAULT_EXPORT__)\n/* harmony export */ });\n/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../node_modules/css-loader/dist/runtime/api.js */ \"../node_modules/css-loader/dist/runtime/api.js\");\n/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__);\n// Imports\n\nvar ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default()(function(i){return i[1]});\n// Module\n___CSS_LOADER_EXPORT___.push([module.id, \".jp-FileBrowser {\\n  height: 100%;\\n}\\n\\n.lm-TabPanel {\\n  height: 100%;\\n}\\n\\n.jp-TreePanel .lm-TabPanel-tabBar {\\n  border: none;\\n  overflow: visible;\\n  min-height: 32px;\\n}\\n\\n.jp-TreePanel .lm-TabBar-tab {\\n  color: var(--jp-ui-font-color0);\\n  font-size: var(--jp-ui-font-size1);\\n  padding: 8px;\\n}\\n\\n.jp-TreePanel .lm-TabBar-tabLabel {\\n  padding-left: 5px;\\n  padding-right: 5px;\\n}\\n\\n/* Override the style from upstream JupyterLab */\\n.jp-FileBrowser-toolbar.jp-Toolbar\\n  .jp-Toolbar-item:first-child\\n  .jp-ToolbarButtonComponent {\\n  width: auto;\\n  background: unset;\\n  padding-left: 5px;\\n  padding-right: 5px;\\n}\\n\\n.jp-FileBrowser-toolbar.jp-Toolbar\\n  .jp-Toolbar-item:first-child\\n  .jp-ToolbarButtonComponent:hover {\\n  background-color: var(--jp-layout-color2);\\n}\\n\\n.jp-FileBrowser-toolbar.jp-Toolbar .jp-ToolbarButtonComponent {\\n  width: unset;\\n}\\n\", \"\"]);\n// Exports\n/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);\n\n\n//# sourceURL=webpack://_JUPYTERLAB.CORE_OUTPUT/../packages/tree-extension/style/base.css?../node_modules/css-loader/dist/cjs.js");

/***/ }),

/***/ "../node_modules/css-loader/dist/cjs.js!../packages/ui-components/style/base.css":
/*!***************************************************************************************!*\
  !*** ../node_modules/css-loader/dist/cjs.js!../packages/ui-components/style/base.css ***!
  \***************************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"default\": () => (__WEBPACK_DEFAULT_EXPORT__)\n/* harmony export */ });\n/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../node_modules/css-loader/dist/runtime/api.js */ \"../node_modules/css-loader/dist/runtime/api.js\");\n/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__);\n// Imports\n\nvar ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default()(function(i){return i[1]});\n// Module\n___CSS_LOADER_EXPORT___.push([module.id, \"\", \"\"]);\n// Exports\n/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);\n\n\n//# sourceURL=webpack://_JUPYTERLAB.CORE_OUTPUT/../packages/ui-components/style/base.css?../node_modules/css-loader/dist/cjs.js");

/***/ }),

/***/ "../packages/application-extension/style/base.css":
/*!********************************************************!*\
  !*** ../packages/application-extension/style/base.css ***!
  \********************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

eval("var content = __webpack_require__(/*! !!../../../node_modules/css-loader/dist/cjs.js!./base.css */ \"../node_modules/css-loader/dist/cjs.js!../packages/application-extension/style/base.css\");\ncontent = content.__esModule ? content.default : content;\n\nif (typeof content === 'string') {\n  content = [[module.id, content, '']];\n}\n\nvar options = {}\n\noptions.insert = \"head\";\noptions.singleton = false;\n\nvar update = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ \"../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js\")(content, options);\n\nif (content.locals) {\n  module.exports = content.locals;\n}\n\n\n//# sourceURL=webpack://_JUPYTERLAB.CORE_OUTPUT/../packages/application-extension/style/base.css?");

/***/ }),

/***/ "../packages/application/style/base.css":
/*!**********************************************!*\
  !*** ../packages/application/style/base.css ***!
  \**********************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

eval("var content = __webpack_require__(/*! !!../../../node_modules/css-loader/dist/cjs.js!./base.css */ \"../node_modules/css-loader/dist/cjs.js!../packages/application/style/base.css\");\ncontent = content.__esModule ? content.default : content;\n\nif (typeof content === 'string') {\n  content = [[module.id, content, '']];\n}\n\nvar options = {}\n\noptions.insert = \"head\";\noptions.singleton = false;\n\nvar update = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ \"../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js\")(content, options);\n\nif (content.locals) {\n  module.exports = content.locals;\n}\n\n\n//# sourceURL=webpack://_JUPYTERLAB.CORE_OUTPUT/../packages/application/style/base.css?");

/***/ }),

/***/ "../packages/docmanager-extension/style/base.css":
/*!*******************************************************!*\
  !*** ../packages/docmanager-extension/style/base.css ***!
  \*******************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

eval("var content = __webpack_require__(/*! !!../../../node_modules/css-loader/dist/cjs.js!./base.css */ \"../node_modules/css-loader/dist/cjs.js!../packages/docmanager-extension/style/base.css\");\ncontent = content.__esModule ? content.default : content;\n\nif (typeof content === 'string') {\n  content = [[module.id, content, '']];\n}\n\nvar options = {}\n\noptions.insert = \"head\";\noptions.singleton = false;\n\nvar update = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ \"../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js\")(content, options);\n\nif (content.locals) {\n  module.exports = content.locals;\n}\n\n\n//# sourceURL=webpack://_JUPYTERLAB.CORE_OUTPUT/../packages/docmanager-extension/style/base.css?");

/***/ }),

/***/ "../packages/help-extension/style/base.css":
/*!*************************************************!*\
  !*** ../packages/help-extension/style/base.css ***!
  \*************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

eval("var content = __webpack_require__(/*! !!../../../node_modules/css-loader/dist/cjs.js!./base.css */ \"../node_modules/css-loader/dist/cjs.js!../packages/help-extension/style/base.css\");\ncontent = content.__esModule ? content.default : content;\n\nif (typeof content === 'string') {\n  content = [[module.id, content, '']];\n}\n\nvar options = {}\n\noptions.insert = \"head\";\noptions.singleton = false;\n\nvar update = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ \"../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js\")(content, options);\n\nif (content.locals) {\n  module.exports = content.locals;\n}\n\n\n//# sourceURL=webpack://_JUPYTERLAB.CORE_OUTPUT/../packages/help-extension/style/base.css?");

/***/ }),

/***/ "../packages/notebook-extension/style/base.css":
/*!*****************************************************!*\
  !*** ../packages/notebook-extension/style/base.css ***!
  \*****************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

eval("var content = __webpack_require__(/*! !!../../../node_modules/css-loader/dist/cjs.js!./base.css */ \"../node_modules/css-loader/dist/cjs.js!../packages/notebook-extension/style/base.css\");\ncontent = content.__esModule ? content.default : content;\n\nif (typeof content === 'string') {\n  content = [[module.id, content, '']];\n}\n\nvar options = {}\n\noptions.insert = \"head\";\noptions.singleton = false;\n\nvar update = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ \"../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js\")(content, options);\n\nif (content.locals) {\n  module.exports = content.locals;\n}\n\n\n//# sourceURL=webpack://_JUPYTERLAB.CORE_OUTPUT/../packages/notebook-extension/style/base.css?");

/***/ }),

/***/ "../packages/terminal-extension/style/base.css":
/*!*****************************************************!*\
  !*** ../packages/terminal-extension/style/base.css ***!
  \*****************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

eval("var content = __webpack_require__(/*! !!../../../node_modules/css-loader/dist/cjs.js!./base.css */ \"../node_modules/css-loader/dist/cjs.js!../packages/terminal-extension/style/base.css\");\ncontent = content.__esModule ? content.default : content;\n\nif (typeof content === 'string') {\n  content = [[module.id, content, '']];\n}\n\nvar options = {}\n\noptions.insert = \"head\";\noptions.singleton = false;\n\nvar update = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ \"../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js\")(content, options);\n\nif (content.locals) {\n  module.exports = content.locals;\n}\n\n\n//# sourceURL=webpack://_JUPYTERLAB.CORE_OUTPUT/../packages/terminal-extension/style/base.css?");

/***/ }),

/***/ "../packages/tree-extension/style/base.css":
/*!*************************************************!*\
  !*** ../packages/tree-extension/style/base.css ***!
  \*************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

eval("var content = __webpack_require__(/*! !!../../../node_modules/css-loader/dist/cjs.js!./base.css */ \"../node_modules/css-loader/dist/cjs.js!../packages/tree-extension/style/base.css\");\ncontent = content.__esModule ? content.default : content;\n\nif (typeof content === 'string') {\n  content = [[module.id, content, '']];\n}\n\nvar options = {}\n\noptions.insert = \"head\";\noptions.singleton = false;\n\nvar update = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ \"../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js\")(content, options);\n\nif (content.locals) {\n  module.exports = content.locals;\n}\n\n\n//# sourceURL=webpack://_JUPYTERLAB.CORE_OUTPUT/../packages/tree-extension/style/base.css?");

/***/ }),

/***/ "../packages/ui-components/style/base.css":
/*!************************************************!*\
  !*** ../packages/ui-components/style/base.css ***!
  \************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

eval("var content = __webpack_require__(/*! !!../../../node_modules/css-loader/dist/cjs.js!./base.css */ \"../node_modules/css-loader/dist/cjs.js!../packages/ui-components/style/base.css\");\ncontent = content.__esModule ? content.default : content;\n\nif (typeof content === 'string') {\n  content = [[module.id, content, '']];\n}\n\nvar options = {}\n\noptions.insert = \"head\";\noptions.singleton = false;\n\nvar update = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ \"../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js\")(content, options);\n\nif (content.locals) {\n  module.exports = content.locals;\n}\n\n\n//# sourceURL=webpack://_JUPYTERLAB.CORE_OUTPUT/../packages/ui-components/style/base.css?");

/***/ }),

/***/ "../packages/application-extension/style/index.js":
/*!********************************************************!*\
  !*** ../packages/application-extension/style/index.js ***!
  \********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _jupyterlab_classic_application_style_index_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab-classic/application/style/index.js */ \"../packages/application/style/index.js\");\n/* harmony import */ var _lumino_widgets_style_index_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets/style/index.js */ \"../node_modules/@lumino/widgets/style/index.js\");\n/* harmony import */ var _base_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./base.css */ \"../packages/application-extension/style/base.css\");\n/* harmony import */ var _base_css__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_base_css__WEBPACK_IMPORTED_MODULE_2__);\n\n\n\n\n\n\n//# sourceURL=webpack://_JUPYTERLAB.CORE_OUTPUT/../packages/application-extension/style/index.js?");

/***/ }),

/***/ "../packages/application/style/index.js":
/*!**********************************************!*\
  !*** ../packages/application/style/index.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _jupyterlab_application_style_index_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application/style/index.js */ \"../node_modules/@jupyterlab/application/style/index.js\");\n/* harmony import */ var _jupyterlab_mainmenu_style_index_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/mainmenu/style/index.js */ \"../node_modules/@jupyterlab/mainmenu/style/index.js\");\n/* harmony import */ var _jupyterlab_ui_components_style_index_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components/style/index.js */ \"../node_modules/@jupyterlab/ui-components/style/index.js\");\n/* harmony import */ var _base_css__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./base.css */ \"../packages/application/style/base.css\");\n/* harmony import */ var _base_css__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_base_css__WEBPACK_IMPORTED_MODULE_3__);\n/*-----------------------------------------------------------------------------\n| Copyright (c) Jupyter Development Team.\n| Distributed under the terms of the Modified BSD License.\n|----------------------------------------------------------------------------*/\n\n\n\n\n\n\n\n\n//# sourceURL=webpack://_JUPYTERLAB.CORE_OUTPUT/../packages/application/style/index.js?");

/***/ }),

/***/ "../packages/docmanager-extension/style/index.js":
/*!*******************************************************!*\
  !*** ../packages/docmanager-extension/style/index.js ***!
  \*******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _base_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./base.css */ \"../packages/docmanager-extension/style/base.css\");\n/* harmony import */ var _base_css__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_base_css__WEBPACK_IMPORTED_MODULE_0__);\n\n\n\n//# sourceURL=webpack://_JUPYTERLAB.CORE_OUTPUT/../packages/docmanager-extension/style/index.js?");

/***/ }),

/***/ "../packages/help-extension/style/index.js":
/*!*************************************************!*\
  !*** ../packages/help-extension/style/index.js ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _base_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./base.css */ \"../packages/help-extension/style/base.css\");\n/* harmony import */ var _base_css__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_base_css__WEBPACK_IMPORTED_MODULE_0__);\n\n\n\n//# sourceURL=webpack://_JUPYTERLAB.CORE_OUTPUT/../packages/help-extension/style/index.js?");

/***/ }),

/***/ "../packages/notebook-extension/style/index.js":
/*!*****************************************************!*\
  !*** ../packages/notebook-extension/style/index.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _base_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./base.css */ \"../packages/notebook-extension/style/base.css\");\n/* harmony import */ var _base_css__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_base_css__WEBPACK_IMPORTED_MODULE_0__);\n\n\n\n//# sourceURL=webpack://_JUPYTERLAB.CORE_OUTPUT/../packages/notebook-extension/style/index.js?");

/***/ }),

/***/ "../packages/terminal-extension/style/index.js":
/*!*****************************************************!*\
  !*** ../packages/terminal-extension/style/index.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _base_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./base.css */ \"../packages/terminal-extension/style/base.css\");\n/* harmony import */ var _base_css__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_base_css__WEBPACK_IMPORTED_MODULE_0__);\n\n\n\n//# sourceURL=webpack://_JUPYTERLAB.CORE_OUTPUT/../packages/terminal-extension/style/index.js?");

/***/ }),

/***/ "../packages/tree-extension/style/index.js":
/*!*************************************************!*\
  !*** ../packages/tree-extension/style/index.js ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _jupyterlab_filebrowser_style_index_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/filebrowser/style/index.js */ \"../node_modules/@jupyterlab/filebrowser/style/index.js\");\n/* harmony import */ var _base_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./base.css */ \"../packages/tree-extension/style/base.css\");\n/* harmony import */ var _base_css__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_base_css__WEBPACK_IMPORTED_MODULE_1__);\n\n\n\n\n\n//# sourceURL=webpack://_JUPYTERLAB.CORE_OUTPUT/../packages/tree-extension/style/index.js?");

/***/ }),

/***/ "../packages/ui-components/style/index.js":
/*!************************************************!*\
  !*** ../packages/ui-components/style/index.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _base_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./base.css */ \"../packages/ui-components/style/base.css\");\n/* harmony import */ var _base_css__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_base_css__WEBPACK_IMPORTED_MODULE_0__);\n/*-----------------------------------------------------------------------------\n| Copyright (c) Jupyter Development Team.\n| Distributed under the terms of the Modified BSD License.\n|----------------------------------------------------------------------------*/\n\n\n\n\n//# sourceURL=webpack://_JUPYTERLAB.CORE_OUTPUT/../packages/ui-components/style/index.js?");

/***/ })

}]);