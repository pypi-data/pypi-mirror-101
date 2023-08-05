/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../Global';
import { CSSProperties } from '@material-ui/core/styles/withStyles';
import { OptumiConfig } from '../models/OptumiConfig';
import { Dropdown, Switch } from '.';
import { IconButton } from '@material-ui/core';
import { Page } from '../components/UserDialog';
import { OpenInNew } from '@material-ui/icons';


interface IProps {
    style?: CSSProperties
    getValue: () => OptumiConfig
    saveValue: (config: OptumiConfig) => void
    disabled?: boolean
	openUserDialogTo?: (page: number) => Promise<void> // This is somewhat spaghetti code-y, maybe think about revising
    handleClose?: () => void
}

interface IState {
    value: string
}

const LABEL_WIDTH = '80px'
const VALUES = [{value: 'succeeds or fails', description: ''}, {value: 'fails', description: ''}];

export class NotificationContent extends React.Component<IProps, IState> {
    private _isMounted = false

    constructor(props: IProps) {
        super(props);
        this.state = {
            value: this.props.getValue().notifications.jobCompletedSMSEnabled ? VALUES[0].value : VALUES[1].value,
        }
    }
    
    private handleJobStartedSMSChange = (value: boolean) => {
        const config = this.props.getValue().copy()
        config.notifications.jobStartedSMSEnabled = value;
        this.props.saveValue(config);
    }

    private handleChange = (value: string, enabled: boolean) => {
        const config = this.props.getValue().copy()
        config.notifications.jobCompletedSMSEnabled = value == VALUES[0].value && enabled;
        config.notifications.jobFailedSMSEnabled = enabled;
        this.props.saveValue(config);
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const disabled = !Global.user.notificationsEnabled || Global.user.phoneNumber == null || Global.user.phoneNumber == ""
        return (
            <>
                <Switch
                    getValue={() => (disabled && !this.props.disabled) ? false : this.props.getValue().notifications.jobStartedSMSEnabled}
                    saveValue={this.handleJobStartedSMSChange}
                    label='Send a text when my job starts'
                    labelWidth={LABEL_WIDTH}
                    disabled={disabled || this.props.disabled || this.props.disabled}
                />
                <div style={{display: 'inline-flex'}}>
                    <Switch
                        getValue={() => (disabled && !this.props.disabled) ? false : this.props.getValue().notifications.jobFailedSMSEnabled}
                        saveValue={(enabled: boolean) => this.handleChange(this.state.value, enabled)}
                        label='Send a text when my job '
                        labelWidth={LABEL_WIDTH}
                        disabled={disabled || this.props.disabled}
                    />
                    <Dropdown
                        getValue={() => this.state.value}
                        saveValue={(value: string) => {
                            this.safeSetState({ value: value});
                            this.handleChange(value, this.props.getValue().notifications.jobFailedSMSEnabled);
                        }}
                        values={VALUES}
                        disabled={disabled || this.props.disabled}
                        // Wipe out the width being set internally in Dropdown
                        style={{width: '', marginLeft: '-6px'}}
                    />
                    
                </div>
                {(disabled && !this.props.disabled) && (
                    <div style={{display: 'inline-flex', width: '100%',margin: '12px 36px'}}>
                        <div style={{margin: 'auto 0px', fontStyle: 'italic'}}>
                            Notifications can be enabled in settings
                        </div>
                        <IconButton
                            onClick={() => {
                                if (this.props.openUserDialogTo) this.props.openUserDialogTo(Page.GENERAL);
                                if (this.props.handleClose) this.props.handleClose();
                            }}
                            style={{
                                display: 'inline-block',
                                width: '36px',
                                height: '36px',
                                padding: '3px',
                            }}
                        >
                            <OpenInNew style={{height: '20px', width: '20px'}}/>
                        </IconButton>
                    </div>
                )}
            </>
        )
    }

    public componentDidMount = () => {
        this._isMounted = true
    }

    public componentWillUnmount = () => {
        this._isMounted = false
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
}
