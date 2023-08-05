/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { ServerConnection } from '@jupyterlab/services';
import { Global } from '../Global';
import { Update } from './Update';
import { OutputFile } from './OutputFile';
import { Machine } from './machine/Machine';

export enum Status {
	INITIALIZING,
	RUNNING,
	COMPLETED,
}

export class Module {
	private _sessionReady: boolean = false;

	get sessionReady(): boolean {
		return this._sessionReady;
	}

	private addOutput: (line: string, modifier: string) => void;

	private readonly _uuid: string;
	private readonly _workloadUUID: string;

	private _sessionToken: string;
	private _sessionPort: string;

    private _machine: Machine;
    
    private _output: Update[];
    private _files: OutputFile[];
    private _updates: Update[];

	constructor(uuid: string, workloadUUID: string, addOutput: (line: string, modifier: string) => void, machine: Machine = null, sessionToken: string = null, output: Update[] = [], updates: Update[] = [], files: OutputFile[] = []) {
		this._uuid = uuid;
		this._workloadUUID = workloadUUID;
		this.addOutput = addOutput;

		this._sessionToken = sessionToken;

        this._machine = machine;

		this._output = output;
		for (var l of this._output) {
			this.addOutput(l.line, l.modifier);
		}
		this._sessionReady = output.map(x => x.line.includes('Jupyter Server ') && x.line.includes(' is running at:')).includes(true);

		this._updates = updates;
		this._files = files;
	}

	get uuid(): string {
		return this._uuid;
	}

	////
	/// We are not using the module stdin yet
	//

	get sessionToken(): string {
        return this._sessionToken;
	}
	
	get sessionPort(): string {
        return this._sessionPort;
    }

    get machine(): Machine {
        return this._machine;
    }

	get updates(): Update[] {
        return this._updates;
    }

    get output(): Update[] {
        return this._output;
    }

	get files(): OutputFile[] {
		return this._files;
	}

	get modStatus(): Status {
		for (var update of this._updates) {
			if (update.modifier == "stop") return Status.COMPLETED;
		}
		return Status.RUNNING;
	}

	get error(): boolean {
		for (var update of this._updates) {
			if (update.line == "error") return true;
		}
		return false;
    }

	public handleUpdate(body: any): boolean {
		let updated = false
		if (body.output != null) {
			if (body.output.length > 0) updated = true;
			for (let i = 0; i < body.output.length; i++) {
				this.addOutput(body.output[i], body.outputmod[i]);
				this._output.push(new Update(body.output[i], body.outputmod[i]));
				if (body.output[i].includes('Jupyter Server ') && body.output[i].includes(' is running at:')) {
					this._sessionReady = true;
					window.open('http://localhost:' + this._sessionPort + '?token=' + this._sessionToken, '_blank');
				}
			}
		}
		if (body.files != null) {
			this._files = [];
			for (let i = 0; i < body.files.length; i++) {
				if (body.files[i] != '') {
					updated = true
					this._files.push(new OutputFile(body.files[i], body.filesmod[i], body.filessize[i]));
				}
			}
		}
		if (body.token != null) {
			updated = true
			this._sessionToken = body.token;
		}
		if (body.updates != null) {
			if (body.updates.length > 0) updated = true;
			for (let i = 0; i < body.updates.length; i++) {
				this._updates.push(new Update(body.updates[i], body.updatesmod[i]));
				if (body.updatesmod[i] == "stop") {
					this.stopSessionHandler();
				} else if (body.updates[i] == "launched") {
				} else if (body.updates[i] == "closed") {
					this.stopSessionHandler();
				}
			}
		}
		if (body.machine != null) {
			updated = true;
			this._machine = Object.setPrototypeOf(body.machine, Machine.prototype);
		}
		return updated;
	}

    public pushModuleInput = (line: string) => {
        const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/push-module-input";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				workloadUUID: this._workloadUUID,
				moduleUUID: this._uuid,
                line: line,
			}),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
		});
    }

	public startSessionHandler() {
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/connect-session";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				module: this._uuid,
			}),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
			return response.json();
		}).then((body: any) => {
			if (body.port) {
				this._sessionPort = body.port;
			}
		});
	}

	public stopSessionHandler() {
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/disconnect-session";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				module: this._uuid,
			}),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
			return response.text();
		});
	}
}
