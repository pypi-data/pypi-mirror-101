/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../Global';

import { ServerConnection } from '@jupyterlab/services';

import {
	Divider,
} from '@material-ui/core';
import { Machine } from '../models/machine/Machine';
import { CSSProperties } from '@material-ui/core/styles/withStyles';
import { Credits } from './machines/Credits';
import { Rate } from './machines/Rate';
import { Budget } from './machines/Budget';

interface IProps {
    style?: CSSProperties
}

interface IState {
    machines: Machine[],
}

export class MachinesPage extends React.Component<IProps, IState> {
	// We need to know if the component is mounted to change state
	_isMounted = false;
    private polling = false;

    constructor(props: IProps) {
        super(props);
        this.state = {
            machines: Global.lastMachines,
        }
    }

    private previousMachines: any
    private updateMachines = () => {
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/get-machines";
		const init = {
			method: 'GET',
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
            if (this.polling) {
                // If we are polling, send a new request in 2 seconds
                if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
                setTimeout(() => this.updateMachines(), 2000);
            }
            Global.handleResponse(response);
			return response.json();
		}).then((body: any) => {
            var machines: Machine[] = []
            for (var i = 0; i < body.machines.length; i++) {
                machines.push(Object.setPrototypeOf(body.machines[i], Machine.prototype));
            }
            if (JSON.stringify(body) !== JSON.stringify(this.previousMachines)) {
                this.safeSetState({ machines: machines });
                this.previousMachines = body
            }
		});
    }

	// The contents of the component
	public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        var machines: JSX.Element[] = new Array();
        for (var i = 0; i < this.state.machines.length; i++) {
            var machine: Machine = this.state.machines[i]
            if (Global.user.userExpertise >= 2 || Machine.getStateMessage(machine.state) != 'Releasing') {
                machines.push(
                    <div key={machine.uuid} style={{display: 'inline-flex', width: '100%', padding: '6px 0px'}}>
                        {machine.getComponent()}
                    </div>
                );
            }
        } 
		return (
			<div style={Object.assign({display: 'flex', flexFlow: 'column', overflow: 'hidden'}, this.props.style)}>
                <div style={{margin: '0px 20px'}}>
                    <Rate />
                    <Divider variant='middle' />
                    {Global.user.userExpertise > 0 ? (<Budget />) : (<Credits />)}
                    <Divider variant='middle' />
                </div>
                <div style={{flexGrow: 1, overflowY: 'auto', padding: '6px'}}>
                    {machines.length == 0 ? (
                        <div style={{ textAlign: 'center', margin: '12px'}}>
                            Running machines will appear here.
                        </div>
                    ) : (
                        machines
                    )}
                </div>
			</div>
		);
	}

	// Will be called automatically when the component is mounted
	public componentDidMount = () => {
        this._isMounted = true;
        this.startPolling()
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
        this.stopPolling()
        Global.lastMachines = this.state.machines;
        this._isMounted = false;
    }
    
    public shouldComponentUpdate = (nextProps: IProps, nextState: IState): boolean => {
        try {
            if (JSON.stringify(this.props) != JSON.stringify(nextProps)) return true;
            if (JSON.stringify(this.state) != JSON.stringify(nextState)) return true;
            if (Global.shouldLogOnRender) console.log('SuppressedRender (' + new Date().getSeconds() + ')');
            return false;
        } catch (error) {
            return true;
        }
    }

    private safeSetState = (map: any) => {
		if (this._isMounted) {
			let update = false
			try {
				for (const key of Object.keys(map)) {
					if (JSON.stringify(map[key]) !== JSON.stringify((this.state as any)[key])) {
						update = true
						break
					}
				}
			} catch (error) {
				update = true
			}
			if (update) {
				if (Global.shouldLogOnSafeSetState) console.log('SafeSetState (' + new Date().getSeconds() + ')');
				this.setState(map)
			} else {
				if (Global.shouldLogOnSafeSetState) console.log('SuppressedSetState (' + new Date().getSeconds() + ')');
			}
		}
	}
    
    public startPolling() {
		this.polling = true;
		this.updateMachines();
	}

	public stopPolling() {
		this.polling = false;
	}
}
