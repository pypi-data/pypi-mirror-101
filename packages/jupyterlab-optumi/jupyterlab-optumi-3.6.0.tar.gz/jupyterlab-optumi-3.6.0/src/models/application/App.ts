/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'

import { ProgressMessage } from '../ProgressMessage';
import { Module, Status } from '../Module';

import { ISignal, Signal } from '@lumino/signaling';

import { ServerConnection } from '@jupyterlab/services';

import { AppTracker } from './AppTracker';
import { OptumiConfig } from '../OptumiConfig';
import { FileUploadConfig } from '../FileUploadConfig';
import { Machine, NoMachine } from '../machine/Machine';
import { Global } from '../../Global';

import { Update } from '../Update';
import { OutputFile } from '../OutputFile';
import { Snackbar } from '../Snackbar';
import FileServerUtils from '../../utils/FileServerUtils';
import NotebookUtils from '../../utils/NotebookUtils';
import FormatUtils from '../../utils/FormatUtils';

import { IdentityAppComponent } from './IdentityAppComponent';
import { AppComponent } from './AppComponent';
import { PopupAppComponent } from './PopupAppComponent';

export enum Phase {
	Initializing = 'initializing',
	Uploading = 'uploading',
	Requisitioning = 'requisitioning',
	Running = 'running',
}

export class App {
	private _changed = new Signal<this, App>(this);

	get changed(): ISignal<this, App> {
		return this._changed;
	}

	private _notebook: any;
	private _config: OptumiConfig;

	// Callback for module to add output to the notebook
	private formatForNotebook = (text: string[]) => {
		// We will not fix overwritten characters in the last line, in case the last line we have wipes out all the characters without writing new ones
		// We will leave the task of removing backspace characters from the last line to the component that renders the lines
		var lastLine = text.pop()
		// Remove overwritten characters and split into lines
		const formatted = NotebookUtils.fixOverwrittenChars(text).split('\n').map(x => x + '\n')
		// Remove the extra '\n'
		formatted[formatted.length-1] = formatted[formatted.length-1].substr(0, formatted[formatted.length-1].length-1);
		// Add the last line back
		formatted.push(lastLine);
		return formatted
	}

	private addOutput = (line: string, modifier: string) => {
		// We do not want to add output to the notebook for an interactive session
		if (!this.interactive) {
			// TODO:JJ If modifier is input, we can not parse it
			if (modifier == 'input') return;
			// TODO:JJ We could get the info that this line is error from either the modifier or the metadata
			try {
				const parsed = JSON.parse(line);
				const metadata = parsed.metadata;
				const outputs: any[] = this._notebook.cells[metadata.cell].outputs;
				// Ignore messages for markdown or raw cells
				if (this._notebook.cells[metadata.cell].cell_type != 'code') return;
				if (metadata.status) {
					if (metadata.status == 'started') {
						this._notebook.cells[metadata.cell].execution_count = '*';
					} else if (metadata.status == 'ended') {
						var count = 1;
						for (let i = 0; i < metadata.cell; i++) {
							if (this._notebook.cells[i].cell_type == ['code']) count++;
						}
						this._notebook.cells[metadata.cell].execution_count = count;
					}
				} else {
					if (modifier == 'output') {
						// We will write our other status updates to output
						if (outputs.length == 0 || outputs[outputs.length-1].name != 'stdout') {
							outputs.push({
								name: 'stdout',
								output_type: 'stream',
								text: this.formatForNotebook([parsed.text]),
							});
						} else {
							const text: string[] = outputs[outputs.length-1].text;
							text.push(parsed.text);
							outputs[outputs.length-1].text = this.formatForNotebook(text)
						}
					} else if (modifier == 'error') {
						// This could be a print to stderr (like a log message) or it could be a caught and formatted exception
						if (parsed.text) {
							if (outputs.length == 0 || outputs[outputs.length-1].name != 'stderr') {
								outputs.push({
									name: 'stderr',
									output_type: 'stream',
									text: this.formatForNotebook([parsed.text]),
								});
							} else {
								const text: string[] = outputs[outputs.length-1].text;
								text.push(parsed.text);
								outputs[outputs.length-1].text = this.formatForNotebook(text)
							}
						} else {
							outputs.push({
								"ename": parsed.ename,
								"evalue": parsed.evalue,
								"output_type": "error",
								"traceback": parsed.traceback,
							});
						}
					} else if (modifier == 'input') {
						// TODO:JJ
					} else {
						console.error('Unknown modifier' + modifier);
					}
				}
			} catch (err) {
				console.warn('Unable to add update line: ' + line);
			}
		}
	}

	private _path: string;
	private _uuid: string = "";
	private _modules: Module[] = [];

	private _initializing: ProgressMessage;
	private _uploading: ProgressMessage;
	private _requisitioning: ProgressMessage;
	private _running: ProgressMessage;

	private _timestamp: Date;
	private _runNum: number;

	constructor(path: string, notebook: any = {}, config: OptumiConfig = new OptumiConfig(), uuid: string = "",
		initializing: Update[] = [], uploading: Update[] = [], requisitioning: Update[] = [], running: Update[] = [], timestamp = new Date(), runNum: number = 0) {		

		this._notebook = notebook;
		this._config = config.copy();

		this._path = path;
		this._uuid = uuid;

		this._initializing = new ProgressMessage(Phase.Initializing, initializing);
		this._uploading = new ProgressMessage(Phase.Uploading, uploading);
		this._requisitioning = new ProgressMessage(Phase.Requisitioning, requisitioning);
		this._running = new ProgressMessage(Phase.Running, running);
		
		if (this._uuid != "") {
			this._initializing.appUUID = this._uuid;
			this._uploading.appUUID = this._uuid;
			this._requisitioning.appUUID = this._uuid;
			this._running.appUUID = this._uuid;
		}

		this._timestamp = timestamp;
		this._runNum = runNum;

		// Handle errors where we were unable to load some of the updates
		if (this._running.started) {
			if (!this._requisitioning.completed) {
				this._requisitioning.addUpdate(new Update("Unable to retrieve requisitioning updates", ""));
				this._requisitioning.addUpdate(new Update("stop", ""));
			}
			if (!this._uploading.completed) {
				this._uploading.addUpdate(new Update("Unable to retrieve uploading updates", ""));
				this._uploading.addUpdate(new Update("stop", ""));
			}
			if (!this._initializing.completed) {
				this._initializing.addUpdate(new Update("Unable to retrieve initializing updates", ""));
				this._initializing.addUpdate(new Update("stop", ""));
			}
		} else if (this._requisitioning.started) {
			if (!this._uploading.completed) {
				this._uploading.addUpdate(new Update("Unable to retrieve uploading updates", ""));
				this._uploading.addUpdate(new Update("stop", ""));
			}
			if (!this._initializing.completed) {
				this._initializing.addUpdate(new Update("Unable to retrieve initializing updates", ""));
				this._initializing.addUpdate(new Update("stop", ""));
			}
		} else if (this._uploading.started) {
			if (!this._initializing.completed) {
				this._initializing.addUpdate(new Update("Unable to retrieve initializing updates", ""));
				this._initializing.addUpdate(new Update("stop", ""));
			}
		}

		// Handle some errors with requests failing while we get an application up and running
		if (initializing != null) {
			if (this._initializing.started && !this._initializing.completed) {
				if (this._initializing.message == "Compressing files") this._initializing.total = -1;
				this.getCompressionProgress();
				return;
			}
		}

		if (uploading != null) {
			if (this._uploading.started && !this._uploading.completed) {
				this.getUploadProgress();
				return;
			}
		}

		if (requisitioning != null) {
			if (this._requisitioning.started && !this._requisitioning.completed) {
				if (this._requisitioning.message == "Waiting for cloud provider") this._requisitioning.total = -1;
				return;
			}
		}
	}

	// Static function for generating an app from controller synchronization structure
	public static reconstruct(appMap: any): App {
		// Reconstruct the app
        const initializing: Update[] = [];
        for (let i = 0; i < appMap.initializing.length; i++) {
            initializing.push(new Update(appMap.initializing[i], appMap.initializingmod[i]));
        }
        const uploading: Update[] = [];
        for (let i = 0; i < appMap.uploading.length; i++) {
            uploading.push(new Update(appMap.uploading[i], appMap.uploadingmod[i]));
        }
        const requisitioning: Update[] = [];
        for (let i = 0; i < appMap.requisitioning.length; i++) {
            requisitioning.push(new Update(appMap.requisitioning[i], appMap.requisitioningmod[i]));
        }
        const running: Update[] = [];
        for (let i = 0; i < appMap.running.length; i++) {
            running.push(new Update(appMap.running[i], appMap.runningmod[i]));
        }
		var app: App = new App(appMap.name, JSON.parse(appMap.notebook), new OptumiConfig(JSON.parse(appMap.nbConfig)), appMap.uuid, initializing, uploading, requisitioning, running, new Date(appMap.timestamp), appMap.runNum);
		// Add modules
		for (let module of appMap.modules) {
            const output: Update[] = [];
            for (let i = 0; i < module.output.length; i++) {
				output.push(new Update(module.output[i], module.outputmod[i]));
            }
			const updates: Update[] = [];
            for (let i = 0; i < module.updates.length; i++) {
				updates.push(new Update(module.updates[i], module.updatesmod[i]));
            }
            const files: OutputFile[] = [];
            for (let i = 0; i < module.files.length; i++) {
                if (module.files[i] != '') {
                    files.push(new OutputFile(module.files[i], module.filesmod[i], module.filessize[i]));
                }
			}
			var mod: Module = new Module(module.uuid, appMap.uuid, app.addOutput, module.machine ? Object.setPrototypeOf(module.machine, Machine.prototype) : null, module.token, output, updates, files);
			app._modules.push(mod);
			if (mod.modStatus == Status.RUNNING) {
                // The module is still running
                if (!app._initializing.completed || !app._uploading.completed || !app._requisitioning.completed || !app._running.completed) {
                    // Don't poll the module if the app is not running
					if (app.interactive) mod.startSessionHandler();
                }
			}
		}
		return app;
	}

	public handleUpdate(body: any): boolean {
		let updated = false
		if (body.initializing != null) {
			if (body.initializing.length > 0) updated = true;
			for (let i = 0; i < body.initializing.length; i++) {
				this._initializing.addUpdate(new Update(body.initializing[i], body.initializingmod[i]), false);
			}
		}
		if (body.uploading != null) {
			if (body.uploading.length > 0) updated = true;
			for (let i = 0; i < body.uploading.length; i++) {
				this._uploading.addUpdate(new Update(body.uploading[i], body.uploadingmod[i]), false);
			}
		}
		if (body.requisitioning != null) {
			if (body.requisitioning.length > 0) updated = true;
			for (let i = 0; i < body.requisitioning.length; i++) {
				this._requisitioning.addUpdate(new Update(body.requisitioning[i], body.requisitioningmod[i]), false);
				// Special case a warning when we fail to get a machine and start trying a new one
				if ((body.requisitioning[i] as string).startsWith('Machine unavailable, trying another')) {
					if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
					Global.snackbarChange.emit(new Snackbar(
						this.name + ": " + body.requisitioning[i],
						{ variant: 'warning', }
					));
				}
				// Special case loading bar while waiting for a server
				if (this._requisitioning.message == "Waiting for cloud provider") {
					this._requisitioning.total = -1;
				} else {
					this._requisitioning.total = 0;
				}
			}
		}
		if (body.running != null) {
			if (body.running.length > 0) updated = true;
			for (let i = 0; i < body.running.length; i++) {
				if (body.running[i] == 'Completed') {
					if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
					Global.snackbarChange.emit(new Snackbar(
						this.name + ": " + body.running[i],
						{ variant: 'success', }
					));
				} else if (body.running[i] == 'Failed') {
					if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
					Global.snackbarChange.emit(new Snackbar(
						this.name + ": " + body.running[i],
						{ variant: 'error', }
					));
				} else if (body.running[i] == 'Terminated') {
					// We will proactively disconnect the session here
					for (var module of this._modules) {
						module.stopSessionHandler();
					}
				}
				this._running.addUpdate(new Update(body.running[i], body.runningmod[i]), false);
			}
		}
		return updated;
	}

	get notebook(): any {
		return this._notebook;
	}

	get config(): OptumiConfig {
		return this._config;
	}

	set config(config: OptumiConfig) {
		// Make sure we don't have a reference to configuration that will be changed
		this._config = config.copy();

		// Tell the controller about the change
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/push-workload-config";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				workload: this._uuid,
				nbConfig: JSON.stringify(config),
			}),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response)
		});
	}

	get path(): string {
		return this._path;
	}

	get name(): string {
		return this._path.split('/').pop().replace('.ipynb', '');
	}

	get uuid(): string {
		return this._uuid;
	}

	get modules(): Module[] {
		return this._modules;
	}

	get initializing(): ProgressMessage {
		return this._initializing;
	}

	get uploading(): ProgressMessage {
		return this._uploading;
	}

	get requisitioning(): ProgressMessage {
		return this._requisitioning;
	}

	get running(): ProgressMessage {
		return this._running;
	}

	get timestamp(): Date {
		return this._timestamp;
	}

	get runNum(): number {
		return this._runNum;
	}

	get failed(): boolean {
		for (let mod of this.modules) {
			if (mod.error) return true;
		}
		return this._initializing.error || this._uploading.error || this._requisitioning.error || this._running.error;
	}

	get interactive(): boolean {
		return this._config.interactive;
	}

	get sessionToken(): string {
        for (let mod of this.modules) {
			if (mod.sessionToken) return mod.sessionToken;
        }
        return undefined;
	}
	
	get sessionPort(): string {
        for (let mod of this.modules) {
			if (mod.sessionPort) return mod.sessionPort;
        }
        return undefined;
    }

    get machine(): Machine {
        for (let mod of this.modules) {
			if (mod.machine) return mod.machine;
        }
        return undefined;
	}

    public getComponent(openUserDialogTo: (page: number) => Promise<void>): React.CElement<any, AppComponent> {
        return React.createElement(AppComponent, {key: this.uuid, app: this, openUserDialogTo: openUserDialogTo});
    }

    public getPopupComponent(onOpen: () => void, onClose: () => void, openUserDialogTo: (page: number) => Promise<void>): React.CElement<any, PopupAppComponent> {
        return React.createElement(PopupAppComponent, {key: this.uuid, app: this, onOpen: onOpen, onClose: onClose, openUserDialogTo: openUserDialogTo});
    }

    public getIdentityComponent(): React.CElement<any, IdentityAppComponent> {
        return React.createElement(IdentityAppComponent, {key: this.path, app: this});
    }
	
	public async previewNotebook(printRecommendations: boolean): Promise<Machine[]> {
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/preview-notebook";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				nbConfig: JSON.stringify(this._config),
			}),
		};
		return ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
			return response.json();
		}).then((body: any) => {
			if (printRecommendations) {
				console.log("////");
				console.log("///  Start Recommendations: ");
				console.log("//");

				for (let machine of body.machines) {
					console.log(Object.setPrototypeOf(machine, Machine.prototype));
				}

				console.log("//");
				console.log("///  End Recommendations: ");
				console.log("////");
			}
            if (body.machines.length == 0) return [new NoMachine()]; // we have no recommendations
            const machines: Machine[] = [];
            for (let machine of body.machines) {
                machines.push(Object.setPrototypeOf(machine, Machine.prototype));
            }
			return machines;
		});
	}

	// We only want to add this app to the app tracker if the initialization succeeds
	public async setupNotebook(appTracker: AppTracker) {
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/setup-notebook";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				name: this._path,
				timestamp: this._timestamp.toISOString(),
				notebook: {
					path: this._path,
					content: JSON.stringify(this._notebook),
				},
				nbConfig: JSON.stringify(this._config),
			}),
		};
		return ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
			return response.json();
		}).then((body: any) => {
			if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
			Global.jobLaunched.emit(void 0);
			this._uuid = body.uuid;
			this._runNum = body.runNum;
			this._initializing.appUUID = this._uuid;
			this._uploading.appUUID = this._uuid;
			this._requisitioning.appUUID = this._uuid;
			this._running.appUUID = this._uuid;
			this._initializing.addUpdate(new Update("Initializing", ""));
			appTracker.addApp(this);
			if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
			this._changed.emit(this);
			this.launchNotebook();
		});
	}

	private previousLaunchStatus: any;
	private pollingDelay = 500;
	private getLaunchStatus() {
        // If there is an unsigned agreement, do not poll
        if (Global.user != null && Global.user.unsignedAgreement) {
            if (!this.failed) {
				if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
				setTimeout(() => this.getLaunchStatus(), this.pollingDelay);
			}
            return;
        }
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/get-launch-status";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				uuid: this._uuid,
			}),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
			if (response.status == 204) {
				if (!this.failed) {
					if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
					setTimeout(() => this.getLaunchStatus(), this.pollingDelay);
				}
				return;
			}
			return response.json();
		}).then((body: any) => {
			if (body) {
				if (body.status == "Finished") {
					for (let i = 0; i < body.modules.length; i++) {
						const mod = new Module(body.modules[i], this._uuid, this.addOutput);
						this._modules.push(mod);
						if (this.interactive) mod.startSessionHandler();
					}
				} else if (body.status == "Failed") {
					if (!this._initializing.completed) {
						this._initializing.addUpdate(new Update(body.message || 'Initialization failed', ""));
						this._initializing.addUpdate(new Update("error", ""));
						this._initializing.addUpdate(new Update("stop", ""));
					} else if (!this._uploading.completed) {
						this._uploading.addUpdate(new Update(body.message || 'File upload failed', ""));
						this._uploading.addUpdate(new Update("error", ""));
						this._uploading.addUpdate(new Update("stop", ""));
					}
					if (body.snackbar) {
						if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
						Global.snackbarChange.emit(new Snackbar(
                            this.name + ": " + body.snackbar,
                            { variant: 'error', }
                        ));
					}
				} else {
					if (!this.failed) {
						if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
						setTimeout(() => this.getLaunchStatus(), this.pollingDelay);
					}
                }
				if (JSON.stringify(body) !== JSON.stringify(this.previousLaunchStatus)) {
					if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
					this._changed.emit(this);
					this.previousLaunchStatus = body
				}
            }
		}, (error: ServerConnection.ResponseError) => {
			if (!this.failed) {
				if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
				setTimeout(() => this.getLaunchStatus(), this.pollingDelay);
			}
		});
	}

	private previousCompressionProgress: any
	private getCompressionProgress() {
        // If there is an unsigned agreement, do not poll
        if (Global.user != null && Global.user.unsignedAgreement) {
            if (!this.failed) {
				if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
				setTimeout(() => this.getCompressionProgress(), this.pollingDelay);
			}
            return;
        }
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/get-launch-compression-progress";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				uuid: this._uuid,
			}),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
			if (response.status == 204) {
				if (!this.failed) {
					if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
					setTimeout(() => this.getCompressionProgress(), this.pollingDelay);
				}
				return;
			}
			return response.json();
		}).then((body: any) => {
			if (body) {
				if (this._initializing.message != "Compressing files") {
					this._initializing.addUpdate(new Update("Compressing files", ""));
				}
				this._initializing.loaded = body.read;
				this._initializing.total = body.total;
				if (body.read != 0 && body.read == body.total) {
                    // Do nothing
                } else {
					if (!this.failed) {
						if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
						setTimeout(() => this.getCompressionProgress(), this.pollingDelay);
					}
				}
				if (JSON.stringify(body) !== JSON.stringify(this.previousCompressionProgress)) {
					if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
					this._changed.emit(this);
					this.previousCompressionProgress = body
				}
			}
		}, (error: ServerConnection.ResponseError) => {
			if (!this.failed) {
				if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
				setTimeout(() => this.getCompressionProgress(), this.pollingDelay);
			}
		});
	}

	private previousUploadProgress: any
	private getUploadProgress() {
        // If there is an unsigned agreement, do not poll
        if (Global.user != null && Global.user.unsignedAgreement) {
            if (!this.failed) {
				if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
				setTimeout(() => this.getUploadProgress(), this.pollingDelay);
			}
            return;
        }
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/get-launch-upload-progress";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				uuid: this._uuid,
			}),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
			if (response.status == 204) {
				if (!this.failed) {
					if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
					setTimeout(() => this.getUploadProgress(), this.pollingDelay);
				}
				return;
			}
			return response.json();
		}).then((body: any) => {
			if (body) {
				if (!this._initializing.completed) {
					this._initializing.total = 0;
					this._initializing.addUpdate(new Update("stop", ""));
					this._uploading.addUpdate(new Update("Uploading files", ""));
				}
				this._uploading.loaded = body.read;
				this._uploading.total = body.total;
				if (body.read != 0 && body.read == body.total) {
					this._uploading.addUpdate(new Update("stop", ""));
				} else {
					if (!this.failed) {
						if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
						setTimeout(() => this.getUploadProgress(), this.pollingDelay);
					}
				}
				if (JSON.stringify(body) !== JSON.stringify(this.previousUploadProgress)) {
					if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
					this._changed.emit(this);
					this.previousUploadProgress = body
				}
			}
		}, (error: ServerConnection.ResponseError) => {
			if (!this.failed) {
				if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
				setTimeout(() => this.getUploadProgress(), this.pollingDelay);
			}
		});
	}

	// Convert and send a python notebook to the REST interface for deployment
	private async launchNotebook() {
		const uploadFiles: FileUploadConfig[] = this._config.upload.files;
		const requirements: string = this._config.upload.requirements;
		const compressFiles = Global.user.compressFilesEnabled;

		var data: any = {};

		if (requirements != null) {
			data.requirementsFile =  requirements;
		}

		data.dataFiles = [];
		for (var uploadEntry of uploadFiles) {
			if (uploadEntry.type == 'directory') {
				for (var file of (await FileServerUtils.getRecursiveTree(uploadEntry.path))) {
					data.dataFiles.push(file);
				}
			} else {
				data.dataFiles.push(uploadEntry.path);
			}
		}
		data.compress = compressFiles;

		data.uuid = this._uuid;
		data.notebook = {
			path: this._path,
			content: JSON.stringify(this._notebook),
		}
		data.timestamp = this._timestamp.toISOString();

		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/launch-notebook";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify(data),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
		}, (error: ServerConnection.ResponseError) => {
			this._initializing.addUpdate(new Update('Initialization failed', ""));
			this._initializing.addUpdate(new Update('error', ""));
			this._initializing.addUpdate(new Update('stop', ""));
		});
		this.getLaunchStatus();
		if (compressFiles && data.dataFiles.length != 0) this.getCompressionProgress();
		this.getUploadProgress();
	}

	getAppStatus(): Status {
		if (this.initializing.error && !this.uploading.started) return Status.COMPLETED;
		if (this.uploading.error && !this.requisitioning.started) return Status.COMPLETED;
		if (this.requisitioning.error && !this.running.started) return Status.COMPLETED;
		for (var mod of this._modules) {
			if (mod.modStatus == Status.RUNNING) return Status.RUNNING;
		}
		if (this.running.completed) return Status.COMPLETED;
		if (this.uploading.completed) return Status.RUNNING;
		return Status.INITIALIZING;
	}

	getAppMessage(): string {
		var message = "";
		if (this._initializing.message != "") message = this._initializing.message;
		if (this._uploading.message != "") message = this._uploading.message;
		if (this._requisitioning.message != "") message = this._requisitioning.message;
		if (this._running.message != "") message = this._running.message;
		// We will say a session is starting until we can connect to it
		if (this.interactive && message == 'Running' && !(this.modules.length > 0 && this.modules[0].sessionReady)) return 'Starting';
		// We call a terminated app 'closed'
		if (this.interactive && message == 'Terminated') return 'Closed';
		return message;
    }
    
    getTimeElapsed(): string {
        if (!this._initializing.completed) return undefined;
		if (!this._uploading.completed) return undefined;
		if (!this._requisitioning.completed) return undefined;
        return this._running.elapsed;
	}
	
	getEndTime(): Date {
		if (!this._initializing.completed) return undefined;
		if (!this._uploading.completed) return undefined;
		if (!this._requisitioning.completed) return undefined;
        return this._running.endTime;
	}


    getCost(): string {
		if (this.getTimeElapsed() == undefined) return undefined;
		if (this.machine == undefined) return undefined;
		var rate = this.machine.rate;
		const split = this.getTimeElapsed().split(':');
		if (split.length == 3) {
			const hours = +split[0]
			const minutes = +split[1];
			const seconds = +split[2];
			const cost = ((hours * rate) + (minutes * rate / 60) + (seconds * rate / 3600));
        	return (cost.toFixed(2) == '0.00' ? '< $0.01' : '~ $' + cost.toFixed(2));
		} else {
			const minutes = +split[0];
			const seconds = +split[1];
			const cost = ((minutes * rate / 60) + (seconds * rate / 3600));
			return (cost.toFixed(2) == '0.00' ? '< $0.01' : '~ $' + cost.toFixed(2));
		} 
    }

	getShowLoading(): boolean {
		if (this._running.started) return this._running.loaded != this._running.total;
		if (this._requisitioning.started) return this._requisitioning.loaded != this._requisitioning.total;
		if (this._uploading.started) return this._uploading.loaded != this._uploading.total;
		if (this._initializing.started) return this._initializing.loaded != this._initializing.total;
		return false;
	}

	getPercentLoaded(): number {
		if (!this._initializing.completed) return undefined;
		if (!this._uploading.completed) return this._uploading.total == -1 ? undefined : this._uploading.loaded / this._uploading.total;
		if (!this._requisitioning.completed) return this._requisitioning.total == -1 ? undefined : this._requisitioning.loaded / this._requisitioning.total;
		if (!this._running.completed) return this._running.total == -1 ? undefined : this._running.loaded / this._running.total;
		return undefined;
	}

	getLoadingTooltip(): string {
		if (!this.getShowLoading()) return undefined;
		if (!this._initializing.completed) return this._initializing.loaded + '/' + this._initializing.total + ' files';
		if (!this._uploading.completed) return this._uploading.total == -1 ? '' : FormatUtils.styleCapacityUnitValue()(this._uploading.loaded) + '/' + FormatUtils.styleCapacityUnitValue()(this._uploading.total);
		if (!this._requisitioning.completed) return this._requisitioning.total == -1 ? '' : FormatUtils.styleCapacityUnitValue()(this._requisitioning.loaded / Math.pow(1024, 2)) + '/' + FormatUtils.styleCapacityUnitValue()(this._requisitioning.total / Math.pow(1024, 2));
		if (!this._running.completed) return this._running.total == -1 ? '' : FormatUtils.styleCapacityUnitValue()(this._running.loaded / Math.pow(1024, 2)) + '/' + FormatUtils.styleCapacityUnitValue()(this._running.total / Math.pow(1024, 2));
	}

	getError() {
		if (this.failed) {
			return true;
		}
		for (var mod of this._modules) {
			if (mod.error) {
				return true;
			}
		}
		return false;
	}

	// private formatTime = (): string => {
	// 	var app: App = this
	// 	var yesterday: Date = new Date()
	// 	yesterday.setDate(yesterday.getDate() - 1)
	// 	if (app.timestamp == undefined) return undefined;
	// 	var startTime = app.timestamp < yesterday ? app.timestamp.toLocaleDateString() : app.timestamp.toLocaleTimeString();
	// 	if (app.getEndTime() == undefined) return startTime;
	// 	var endTime = app.getEndTime() < yesterday ? app.getEndTime().toLocaleDateString() : app.getEndTime().toLocaleTimeString();
	// 	return startTime == endTime ? startTime : startTime + " - " + endTime;
	// };
}