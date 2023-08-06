class App {
	/**
	 * @param jQueryInstance: Object
	 * @param mainCOntainerId: String
	 * @param config: Object
	 */
	constructor(jQueryInstance, mainCOntainerId, config){
		this.$ = jQueryInstance;
		this.$mainContainer = this.$(`#${mainCOntainerId}`);
		this.config = config;

		this.dirContext = URLUtils.getUrlParam("context") || "";

		let hostInfo = URLUtils.getHostInfo();
		let hotsPort = hostInfo.port ? `:${hostInfo.port}` : ""
		this.appURL = `${hostInfo.protocol}//${hostInfo.hostname}${hotsPort}`;

		this.dropzone = null;

		this._renderUI();
		this._renderDiskInfo();
		this._renderControls();
		this._renderFileList();
		this._renderDropZone();
	}

	_renderUI(){
		let dirContext = this.dirContext ? this.dirContext : "/";
		let ui = `
		<div class="app">
			<div class="app-header">
				<div class="app-header-top">
					<div id="dir-context">"${dirContext}"</div>
					<div id="disk-info"></div>
				</div>
				<div class="app-header-bottom">
					<div id="controls"></div>
				</div>
			</div>
			<div id="file-list"></div>
			<div id="fileupload" class="dropzone"></div>
		</div>`
		this.$mainContainer.html(ui);
	}
	
	_renderDropZone() {
		this.dropzone = new Dropzone("#fileupload", { url: `/api/upload/${this.dirContext}`});
		this.dropzone.options.paramName = 'file';
		this.dropzone.options.chunking = true;
		this.dropzone.options.forceChunking = true;
		this.dropzone.options.maxFilesize = 2*1024; // megabytes = 2 GB
		this.dropzone.options.chunkSize = 5*1024*1024 // bytes = 5 MB
		this.dropzone.options.autoProcessQueue = true;
		this.dropzone.options.paralelUploads = false;
		this.dropzone.on("complete", (event)=>{
			this._renderFileList();
		});
		this.dropzone.on("queuecomplete", (event)=>{
			this._renderFileList();
			this._renderDiskInfo();
			this.dropzone.destroy();
			this._renderDropZone();
		});
	}
	
	_renderDiskInfo(){
		this._callApi("GET", `disk/`, {}, (data)=> {
			if (data) {
				let container = this.$mainContainer.find("#disk-info");
				container.empty();
				let total = Utils.formatFileSize(data.diskUsage.total);
				let used = Utils.formatFileSize(data.diskUsage.used);
				let free = Utils.formatFileSize(data.diskUsage.free);
				let html = `<div>Storage - </div>` +
						`<div class="free">free: ${free},</div>` +
						`<div class="used">used: ${used},</div>` +
						`<div class="total">total: ${total}</div>`;
				container.append(html);
			}
		});
	}

	_renderControls(){
		let container = this.$mainContainer.find("#controls");
		let html = `<div class="control-item">`+
			`Copy link as: `+
				`<input id="copy-as-url" type="radio" name="radio-copy-as" value="url" title="Copy simple URL" checked> <label for="copy-as-url">URL</label>` +
				`<input id="copy-as-md" type="radio" name="radio-copy-as" value="md" title="Copy as MarkDown link"><label for="copy-as-md">MD</label>` +
				`<input id="copy-as-html" type="radio" name="radio-copy-as" value="html" title="Copy as HTML link"><label for="copy-as-html">HTML</label>` +
			`</div>` +
			`<div class="control-item img-buttons">`+
				`<button id="controls-button-add-dir" data-param="New directory" title="Add new dir"><img src="/static/img/folder-plus-solid.svg"/></button>` +
			`</div>`;
		container.empty();
		container.append(html);

		this.$mainContainer.find("#controls-button-add-dir").click((event)=>{
			let param = event.currentTarget.getAttribute("data-param");
			this._callApi("POST", `dir/${this.dirContext}/${param}`, {}, (data)=>{
				this._renderFileList();
			});
		});
	}

	_renderFileList(){
		this._callApi("GET", `dir/${this.dirContext}`, {}, (data)=>{
			if(data){
				let container = this.$mainContainer.find("#file-list");
				container.empty();
				this.dirContext = data.context;
				for(let item of data.result) {
					let type = item.type;
					let filename = item.name;
					let filepath = item.path;
					let filesize = Utils.formatFileSize(item.size);
					let token = item.token;

					let html = "";
					if(type == "file") {
						if(token){
						html =
							`<div class="file-container-token">` +
								`<div class="file-wrapper">` +
									`<div class="file"><a href="/share/${filepath}?token=${token}" target="_blank">${filename}</a></div>` +
									`<div class="filesize">${filesize}</div>` +
								`</div>` +
								`<div class="img-buttons">` +
									`<button class="file-button-copy-url" data-param-path="${filepath}?token=${token}" data-param-name="${filename}" title="Copy link"><img src="/static/img/copy-regular.svg"/></button>` +
									`<button class="file-button-new-token" data-param="${filepath}" title="New token"><img src="/static/img/share-alt-solid.svg"/></button>` +
									`<button class="file-button-delete-token" data-param="${filepath}" title="Delete token"><img src="/static/img/share-alt-square-solid.svg"/></button>` +
									`<button class="file-button-delete-file" data-param="${filepath}" title="Delete file"><img src="/static/img/trash-solid.svg"/></button>` +
								`</div>` +
							`</div>`
						} else {
							html =
							`<div class="file-container">` +
								`<div class="file-wrapper">` +
									`<div class="file">${filename}</div>` +
									`<div class="filesize">${filesize}</div>` +
								`</div>` +
								`<div class="img-buttons">` +
									`<button class="file-button-new-token" data-param="${filepath}" title="Add token"><img src="/static/img/share-alt-solid.svg"/></button>` +
									`<button class="file-button-rename-file" data-param-path="${filepath}" data-param-name="${filename}" title="Rename file"><img src="/static/img/edit-regular.svg"/></button>` +
									`<button class="file-button-delete-file" data-param="${filepath}" title="Delete file"><img src="/static/img/trash-solid.svg"/></button>` +
								`</div>` +
							`</div>`
						}
					} else {
						if(filename == "/" || filename == ".."){
							html =
								`<div class="dir-container">` +
									`<div class="dir"><a href="?context=${filepath}">${filename}</a></div>` +
									`<div class="img-buttons"></div>` +
								`</div>`;
						} else {
							html =
								`<div class="dir-container">` +
									`<div class="dir"><a href="?context=${filepath}">${filename}</a></div>` +
									`<div class="img-buttons">` +
										`<button class="dir-button-rename-dir" data-param-path="${filepath}" data-param-name="${filename}" title="Rename dir"><img src="/static/img/edit-regular.svg"/></button>` +
										`<button class="dir-button-delete-dir" data-param="${filepath}" title="Delete dir"><img src="/static/img/trash-solid.svg"/></button>` +
									`</div>` +
								`</div>`;
						}
					}
					container.append(html);
				}
				// add buttons handlers
				this.$mainContainer.find(".file-button-copy-url").click((event)=>{
					let paramPath = event.currentTarget.getAttribute("data-param-path");
					let paramName = event.currentTarget.getAttribute("data-param-name");
					let copyMethod = this.$(this.$mainContainer.find("input[name=\"radio-copy-as\"]:checked")).val();
					let fullUrl = `${this.appURL}/share/${paramPath}`;
					let textToClipboard = null;
					switch (copyMethod) {
						case "md": textToClipboard = `[${paramName}](${fullUrl})`; break;
						case "html": textToClipboard = `<a href="${fullUrl}">${paramName}</a>`; break;
						default: textToClipboard = fullUrl;
					}
					Utils.copyToClipboard(textToClipboard, event.currentTarget);
				});
				this.$mainContainer.find(".file-button-new-token").click((event)=>{
					let param = event.currentTarget.getAttribute("data-param");
					this._callApi("POST", `token/${param}`, {}, (data)=>{this._renderFileList()})
				});
				this.$mainContainer.find(".file-button-rename-file").click((event)=>{
					let paramPath = event.currentTarget.getAttribute("data-param-path");
					let paramName = event.currentTarget.getAttribute("data-param-name");
					let newFileName = prompt(`Rename file '${paramName}'`, paramName);
					if(newFileName) {
						this._callApi("PUT", `file/${paramPath}?rename=${newFileName}`, {}, (data) => {this._renderFileList()})
					}
				});
				this.$mainContainer.find(".file-button-delete-token").click((event)=>{
					let param = event.currentTarget.getAttribute("data-param");
					this._callApi("DELETE", `token/${param}`, {}, (data)=>{this._renderFileList()})
				});
				this.$mainContainer.find(".file-button-delete-file").click((event)=>{
					let param = event.currentTarget.getAttribute("data-param");
					this._callApi("DELETE", `file/${param}`, {}, (data)=>{this._renderFileList()})
				});
				this.$mainContainer.find(".dir-button-rename-dir").click((event)=>{
					let paramPath = event.currentTarget.getAttribute("data-param-path");
					let paramName = event.currentTarget.getAttribute("data-param-name");
					let newFileName = prompt(`Rename directory '${paramName}'`, paramName);
					if(newFileName) {
						this._callApi("PUT", `dir/${paramPath}?rename=${newFileName}`, {}, (data) => {this._renderFileList()})
					}
				});
				this.$mainContainer.find(".dir-button-delete-dir").click((event)=>{
					let param = event.currentTarget.getAttribute("data-param");
					this._callApi("DELETE", `dir/${param}`, {}, (data)=>{this._renderFileList()})
				});
			}
		});
	}

	_callApi(method, command, params = {}, callback = null){
		let _this = this;
		let getParams = URLUtils.convertParams(params);
		let apiCall = getParams == "" ? `${this.config.apiURL}/${command}` : `${this.config.apiURL}/${command}?${getParams}`;
		this.$.ajax({
			url: apiCall,
			method: method,
			success: (data)=>{
				if(callback) callback(data);
			},
			error: (response)=>{
				if (response.responseJSON && response.responseJSON.message) {
					alert(`Error: ${response.responseJSON.message}`);
				}
			},
		});
	}

}
