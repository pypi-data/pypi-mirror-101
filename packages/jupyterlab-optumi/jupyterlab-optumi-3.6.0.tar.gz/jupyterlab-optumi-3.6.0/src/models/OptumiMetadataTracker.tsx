/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { ServerConnection } from '@jupyterlab/services';

import { ISignal, Signal } from '@lumino/signaling';

import { NotebookPanel, NotebookTracker } from '@jupyterlab/notebook';
import { OptumiConfig } from './OptumiConfig';
import { Global } from '../Global'
import { OptumiMetadata } from './OptumiMetadata';

export class OptumiMetadataTracker {
    private _optumiMetadata = new Map<string, TrackedOptumiMetadata>();

    private _tracker: NotebookTracker;

    constructor(tracker: NotebookTracker) {
        this._tracker = tracker;
        tracker.currentChanged.connect(() => {
            this.handleCurrentChanged(this._tracker.currentWidget);
        });
        this.handleCurrentChanged(this._tracker.currentWidget);
	}

	private handleCurrentChanged = async (current: NotebookPanel) => {
        if (current == null) {
            if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
            setTimeout(() => this.handleCurrentChanged(this._tracker.currentWidget), 250);
            return;
        }
        if (!current.context.isReady) await current.context.ready;
        // If the path changes we need to add a new entry into our map
        current.context.pathChanged.connect(() => this.handleCurrentChanged(current));
        const path = current.context.path;
        const rawMetadata = current.model.metadata;
        var metadata = new OptumiMetadata(rawMetadata.get("optumi") || {});

        var trackedMetadata: TrackedOptumiMetadata;
        // Handle conversion from old metadata stored in file
        const fromFile : any = (rawMetadata.get("optumi") || {})
        if ("intent" in fromFile &&
            "compute" in fromFile &&
            "graphics" in fromFile &&
            "memory" in fromFile &&
            "storage" in fromFile &&
            "upload" in fromFile &&
            "interactive" in fromFile &&
            "version" in fromFile
        ) {
            // Take the metadata from the file
            trackedMetadata = new TrackedOptumiMetadata(path, metadata, new OptumiConfig(fromFile, fromFile.version));
        } else {
            // Get the metadata from the controller
            const config = (await this.fetchConfig(metadata));
            // If this is a duplicated notebook, we want to give it a new uuid, but we will use the old uuid to pick up the config
            for (var entry of this._optumiMetadata) {
                if (entry[1].metadata.nbKey == metadata.nbKey && entry[0] != path) {
                    metadata = new OptumiMetadata();
                }
            }
            trackedMetadata = new TrackedOptumiMetadata(path, metadata, config);
        }
        trackedMetadata.metadata.version = Global.version;
        this._optumiMetadata.set(path, trackedMetadata);

        // Save the metadata in the file to make sure all files have valid metadata
		rawMetadata.set("optumi", JSON.parse(JSON.stringify(metadata)));
        // Save the metadata to the controller, in case something was updated above
        this.setMetadata(trackedMetadata);

        // Once all of this is done, emit a signal that the metadata changed
        if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
        this._metadataChanged.emit(void 0);
	}

    private fetchConfig = (metadata: OptumiMetadata) : Promise<OptumiConfig> => {
        // If there is no user signed in, there is no config
        if (Global.user == null) return Promise.resolve(new OptumiConfig());
        // Fetch the config for this user + notebook from the controller
        const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/get-notebook-config";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				nbKey: metadata.nbKey,
			}),
		};
		return ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response)
            return response.text();
		}).then((response: string) => {
            try {
                var map = {};
                map = JSON.parse(response);
                return new OptumiConfig(map, metadata.version);
            } catch (err) { console.log(err) }
            return new OptumiConfig();
        }, () => new OptumiConfig());
    }

    public refreshMetadata = async () : Promise<void> => {
        // When the user logs in, we need to refresh metadata for them
        for (var entry of this._optumiMetadata.entries()) {
            const path = entry[0];
            const metadata = entry[1].metadata;
            this._optumiMetadata.set(path, new TrackedOptumiMetadata(path, metadata, (await this.fetchConfig(metadata))));
        }
        return Promise.resolve();
    }

	public getMetadata = (): TrackedOptumiMetadata => {
        const path: string = this._tracker.currentWidget.context.path;
        if (!this._optumiMetadata.has(path)) {
            return undefined
        }
        return this._optumiMetadata.get(path);
	}

    public setMetadata = (optumi: TrackedOptumiMetadata) => {
        const rawMetadata = this._tracker.find(x => x.context.path == optumi.path).model.metadata;
		rawMetadata.set("optumi", JSON.parse(JSON.stringify(optumi.metadata)));
        this._optumiMetadata.set(optumi.path, optumi);

        if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
        this._metadataChanged.emit(void 0);

        if (Global.user == null) return;

        // Tell the controller about the change
        const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/set-notebook-config";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				nbKey: optumi.metadata.nbKey,
                nbConfig: JSON.stringify(optumi.config),
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

	public getMetadataChanged = (): ISignal<this, void> => {
		return this._metadataChanged;
	}

    private _metadataChanged = new Signal<this, void>(this);
}

export class TrackedOptumiMetadata {
    public path: string;
    public metadata: OptumiMetadata;
    public config: OptumiConfig;

    constructor(path: string, metadata: OptumiMetadata, config: OptumiConfig) {
        this.path = path;
        this.metadata = metadata;
        this.config = config;
    }

    get uuid(): string {
        return this.metadata.nbKey;
    }
}
