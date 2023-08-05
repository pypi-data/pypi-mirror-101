(self["webpackChunksas2nb"] = self["webpackChunksas2nb"] || []).push([["lib_index_js"],{

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestAPI": () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'sas2nb', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/iconImport.js":
/*!***************************!*\
  !*** ./lib/iconImport.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "sasIcon": () => (/* binding */ sasIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_icons_sas_svg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../style/icons/sas.svg */ "./style/icons/sas.svg");


const sasIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'sas2nb:sas',
    svgstr: _style_icons_sas_svg__WEBPACK_IMPORTED_MODULE_1__.default
});


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _iconImport__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./iconImport */ "./lib/iconImport.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");





/**
 * Initialization data for the sas2nb extension.
 */
const extension = {
    id: 'sas2nb:plugin',
    autoStart: true,
    optional: [_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__.ILauncher],
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__.IFileBrowserFactory],
    activate: async (app, factory) => {
        console.log('JupyterLab extension sas2nb is activated!');
        app.docRegistry.addFileType({
            name: 'sas',
            icon: _iconImport__WEBPACK_IMPORTED_MODULE_3__.sasIcon,
            displayName: 'SAS File',
            extensions: ['.sas'],
            fileFormat: 'text',
            contentType: 'file',
            mimeTypes: ['text/plain'],
        });
        await (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('convert')
            .then(data => {
            console.log(data);
        })
            .catch(reason => {
            console.error(`The sas2nb server extension appears to be missing.\n${reason}`);
        });
        app.commands.addCommand('sas2nb/context-menu:open', {
            label: 'Convert SAS to ipynb',
            caption: 'Convert a SAS file to a notebook',
            icon: _iconImport__WEBPACK_IMPORTED_MODULE_3__.sasIcon,
            execute: async () => {
                const file = factory.tracker.currentWidget.selectedItems().next();
                // POST request
                const dataToSend = { fpath: file.path, origin: origin };
                try {
                    const reply = await (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('convert', {
                        body: JSON.stringify(dataToSend),
                        method: 'POST',
                    });
                    console.log(reply);
                    (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                        title: 'Converted',
                        body: `${file.path} was converted to a notebook.`,
                        buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton()],
                    }).catch((e) => console.log(e));
                }
                catch (reason) {
                    console.error(`Error on POST /sas2nb/convert ${dataToSend}.\n${reason}`);
                }
            },
        });
        app.contextMenu.addItem({
            command: 'sas2nb/context-menu:open',
            selector: '.jp-DirListing-item[data-file-type="sas"]',
            rank: 0,
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ }),

/***/ "./style/icons/sas.svg":
/*!*****************************!*\
  !*** ./style/icons/sas.svg ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<!-- Generator: Adobe Illustrator 24.0.1, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->\n<svg version=\"1.1\" id=\"Layer_1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" x=\"0px\" y=\"0px\"\n\t viewBox=\"0 0 48 48\" style=\"enable-background:new 0 0 48 48;\" xml:space=\"preserve\">\n<style type=\"text/css\">\n\t.st0{fill:#007DC3;}\n\t.st1{fill:#FFFFFF;}\n</style>\n<rect class=\"st0\" width=\"47.7\" height=\"47.7\"/>\n<g>\n\t<g>\n\t\t<g>\n\t\t\t<g>\n\t\t\t\t<path class=\"st1\" d=\"M27,16.4l-0.7-0.8c-0.9-1.1-2.4-1.1-3.5-0.2s-1.4,2.4-0.5,3.5c0,0,0.1,0.1,0.3,0.4\"/>\n\t\t\t\t<path class=\"st1\" d=\"M22.7,19.3c2.1,2.5,4.8,5.8,4.8,5.8c3.5,4.2,1.9,9.4-2.8,12.3C20.6,40,13,39.1,10.4,34.8\n\t\t\t\t\tc2,6,8.8,9.9,16.4,8c6.5-1.6,13.8-10,5.8-19.7L26.7,16\"/>\n\t\t\t</g>\n\t\t\t<path class=\"st1\" d=\"M23.3,28.3c-2-2.4-4.5-5.4-4.5-5.4c-3.5-4.2-1.9-9.4,2.8-12.3C25.8,8,33.4,8.9,36,13.2c-2-6-8.8-9.9-16.4-8\n\t\t\t\tc-6.5,1.6-13.8,10-5.8,19.7l5.7,6.8\"/>\n\t\t\t<path class=\"st1\" d=\"M18.5,30.6l1.3,1.6c0.9,1.1,2.4,1.1,3.5,0.2s1.4-2.4,0.5-3.5c0,0-0.5-0.6-1.3-1.6\"/>\n\t\t</g>\n\t</g>\n\t<g>\n\t\t<path class=\"st1\" d=\"M37,34.9c0-0.7,0.5-1.2,1.2-1.2c0.7,0,1.2,0.5,1.2,1.2c0,0.7-0.5,1.3-1.2,1.3C37.5,36.2,37,35.6,37,34.9z\n\t\t\t M38.2,36.4c0.8,0,1.5-0.6,1.5-1.5c0-0.9-0.7-1.5-1.5-1.5c-0.8,0-1.5,0.6-1.5,1.5C36.6,35.8,37.4,36.4,38.2,36.4z M37.9,35h0.3\n\t\t\tl0.5,0.8h0.3L38.4,35c0.3,0,0.4-0.2,0.4-0.5c0-0.3-0.2-0.5-0.6-0.5h-0.7v1.7h0.3C37.9,35.8,37.9,35,37.9,35z M37.9,34.8v-0.5h0.4\n\t\t\tc0.2,0,0.4,0,0.4,0.3c0,0.3-0.2,0.3-0.4,0.3L37.9,34.8L37.9,34.8z\"/>\n\t</g>\n</g>\n</svg>\n");

/***/ })

}]);
//# sourceMappingURL=lib_index_js.0de9f797445bafb2c71d.js.map