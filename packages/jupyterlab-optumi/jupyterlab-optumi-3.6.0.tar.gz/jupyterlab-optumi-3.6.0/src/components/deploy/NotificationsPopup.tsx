/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { Dialog, IconButton, withStyles } from '@material-ui/core';
import { CSSProperties } from '@material-ui/core/styles/withStyles';
import { AddAlert, Close } from '@material-ui/icons';
import * as React from 'react'
import { Global } from '../../Global';
import MuiDialogTitle from '@material-ui/core/DialogTitle';
import { ShadowedDivider } from '../../core';
import { OptumiConfig } from '../../models/OptumiConfig';
import { NotificationContent } from '../../core/NotificationContent'

const StyledDialog = withStyles({
    paper: {
        width: 'calc(min(80%, 600px + 150px + 2px))',
        // width: '100%',
        height: '80%',
        overflowY: 'visible',
        backgroundColor: 'var(--jp-layout-color1)',
        maxWidth: 'inherit',
    },
})(Dialog);

interface IProps {
    style?: CSSProperties
    onOpen?: () => void
    onClose?: () => void
    disabled?: boolean
	openUserDialogTo?: (page: number) => Promise<void> // This is somewhat spaghetti code-y, maybe think about revising
}

interface IState {
    open: boolean,
}

// TODO:Beck The popup needs to be abstracted out, there is too much going on to reproduce it in more than one file
export class NotificationsPopup extends React.Component<IProps, IState> {
    private _isMounted = false

    constructor(props: IProps) {
        super(props);
		this.state = {
            open: false,
		};
    }
    
    private handleClickOpen = () => {
        if (this.props.onOpen) this.props.onOpen()
		this.safeSetState({ open: true });
	}

	private handleClose = () => {
        this.safeSetState({ open: false });
        if (this.props.onClose) this.props.onClose()
    }

    private handleKeyDown = (event: KeyboardEvent) => {
        if (event.key === 'Escape') this.handleClose();
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <div style={Object.assign({margin: 'auto'}, this.props.style)}>
                <IconButton
                    onClick={this.handleClickOpen}
                    style={{padding: '0px', marginRight: '-3px', width: '30px', height: '30px'}}
                    disabled={this.props.disabled}
                    >
                    <AddAlert style={{height: '21px'}}/>
                </IconButton>
                <StyledDialog
					open={this.state.open}
					onClose={this.handleClose}
                    scroll='paper'
				>
					<MuiDialogTitle
					    disableTypography
                        style={{
                            display: 'inline-flex',
                            backgroundColor: 'var(--jp-layout-color2)',
                            height: '60px',
                            padding: '6px',
                            borderRadius: '4px',
                        }}
                    >
                        <div style={{
                            display: 'inline-flex',
                            minWidth: '225px',
                            fontSize: '16px',
                            fontWeight: 'bold',
                            paddingRight: '12px', // this is 6px counteracting the MuiDialogTitle padding and 6px aligning the padding to the right of the tabs
                        }}>
                            <div style={{margin: 'auto', paddingLeft: '12px'}}>
            					Configure Notifications
                            </div>
                        </div>
                        <div style={{flexGrow: 1}} />
                        <IconButton
                            onClick={this.handleClose}
                            style={{
                                display: 'inline-block',
                                width: '36px',
                                height: '36px',
                                padding: '3px',
                                margin: '6px',
                            }}
                        >
                            <Close
                                style={{
                                    width: '30px',
                                    height: '30px',
                                    padding: '3px',
                                }}
                            />
                        </IconButton>
					</MuiDialogTitle>
                    <ShadowedDivider />
                    <div style={{
                        padding: '12px',
                        fontSize: 'var(--jp-ui-font-size1)',
                    }}>
                        <NotificationContent 
                            getValue={() => Global.metadata.getMetadata().config}
                            saveValue={(config: OptumiConfig) => {
                                const metadata = Global.metadata.getMetadata();
                                metadata.config = config;
                                Global.metadata.setMetadata(metadata);
                            }}
                            openUserDialogTo={this.props.openUserDialogTo}
                            handleClose={this.handleClose}
                        />
                    </div>
				</StyledDialog>
            </div>
        )
    }

    public componentDidMount = () => {
        this._isMounted = true
        document.addEventListener('keydown', this.handleKeyDown, false)
    }

    public componentWillUnmount = () => {
        document.removeEventListener('keydown', this.handleKeyDown, false)
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
}
