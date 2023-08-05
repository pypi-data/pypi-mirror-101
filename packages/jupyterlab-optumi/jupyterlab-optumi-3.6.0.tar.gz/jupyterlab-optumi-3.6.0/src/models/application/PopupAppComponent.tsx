/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { Button, Dialog, DialogContent, IconButton, InputAdornment, Tab, Tabs, TextField, withStyles } from '@material-ui/core';
import * as React from 'react';
import { Global } from '../../Global';
import PopupIcon from '@material-ui/icons/MoreVert';
import MuiDialogTitle from '@material-ui/core/DialogTitle';
import { CSSProperties } from '@material-ui/core/styles/withStyles';
import CloseIcon from '@material-ui/icons/Close';
import { App } from './App';
import { ScrollableDiv } from '../../components/monitor/ScrollableDiv';
import { OutputFileList } from '../../components/deploy/OutputFileList';
import CodeIcon from '@material-ui/icons/Code';
import { Status } from '../Module';
import { MachineCapability } from '../machine/MachineCapabilities';
import { ShadowedDivider } from '../../core';

import OpenInNewIcon from '@material-ui/icons/OpenInNew';
import Notebook from '../../core/notebook/Notebook';
import FileServerUtils from '../../utils/FileServerUtils';
import { NotificationContent } from '../../core/NotificationContent';
import { OptumiConfig } from '../OptumiConfig';
import ExtraInfo from '../../utils/ExtraInfo';

const StyledDialog = withStyles({
    paper: {
        width: '80%',
        height: '80%',
        overflowY: 'visible',
        backgroundColor: 'var(--jp-layout-color1)',
        maxWidth: 'inherit',
    },
})(Dialog);

const enum Page {
    SUMMARY = 0,
    NOTIFICATIONS = 1,
    NOTEBOOK = 2,
    FILES = 3,
    MACHINE = 4,
    TERMINAL = 5,
}

interface IProps {
    style?: CSSProperties
    app: App
    onOpen?: () => void
	onClose?: () => void
    onMouseOver?: (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void
    onMouseOut?: (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void
    openUserDialogTo?: (page: number) => Promise<void> // This is somewhat spaghetti code-y, maybe think about revising
}

interface IState {
    open: boolean,
	selectedPanel: number,
	inputLine: string
}

// TODO:Beck The popup needs to be abstracted out, there is too much going on to reproduce it in more than one file
export class PopupAppComponent extends React.Component<IProps, IState> {
    private _isMounted = false

    constructor(props: IProps) {
        super(props);
		this.state = {
            open: false,
			selectedPanel: Page.SUMMARY,
			inputLine: ''
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
	
	private handleInputLineChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        this.safeSetState({ inputLine: event.target.value });
    }

    private handleKeyDown = (event: React.KeyboardEvent) => {
        if (event.key == 'Enter') {
            this.safeSetState({ inputLine: ''}), 
            this.props.app.modules[0].pushModuleInput(this.state.inputLine);
        }
    }
    
    private handleMouseOver = (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
        if (this.props.onMouseOver) this.props.onMouseOver(event);
    }

    private handleMouseOut = (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
        if (this.props.onMouseOut) this.props.onMouseOut(event);
    }

    private openSession = () => {
        window.open('http://localhost:' + this.props.app.sessionPort + '?token=' + this.props.app.sessionToken, '_blank');
    }

    private openAsNewNotebook = () => {
        const path = this.props.app.path.replace('.ipynb', '-run' + (this.props.app.runNum) + '.ipynb');
        var notebook: any = this.props.app.notebook;
        FileServerUtils.saveNotebook(path, notebook).then((success: boolean) => { Global.docManager.open(path) });
        // Close the dialog
        this.handleClose();
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        var i = 0;
        return (
            <>
                <IconButton
                    onClick={this.handleClickOpen}
                    style={{
                        display: 'inline-block',
                        width: '36px',
                        height: '36px',
                        padding: '3px',
                    }}
                    onMouseOver={this.handleMouseOver}
                    onMouseOut={this.handleMouseOut}
                >
                    <PopupIcon
                        style={{
                            width: '30px',
                            height: '30px',
                            padding: '3px',
                        }}
                    />
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
                            minWidth: '150px',
                            fontSize: '16px',
                            fontWeight: 'bold',
                            paddingRight: '12px', // this is 6px counteracting the MuiDialogTitle padding and 6px aligning the padding to the right of the tabs
                        }}>
                            <div style={{margin: 'auto', paddingLeft: '12px'}}>
            					{this.props.app.interactive ? "Session" : "Job"}
                            </div>
                        </div>
						<div style={{width: '100%', display: 'inline-flex', overflowX: 'hidden', fontSize: '16px', paddingLeft: '8px'}}>
	                        <div style={{flexGrow: 1, margin: 'auto 0px'}}>
                                {this.props.app.path}
                            </div>
                            {this.props.app.interactive && (
                                <Button
                                    style={{margin: '6px'}}
                                    disableElevation
                                    variant='contained'
                                    color='primary'
                                    onClick={this.openSession}
                                    disabled={this.props.app.getAppStatus() == Status.COMPLETED || !(this.props.app.modules.length > 0 && this.props.app.modules[0].sessionReady)}
                                    endIcon={<OpenInNewIcon />}
                                >
                                    Open session
                                </Button>
                            )}
                            {!this.props.app.interactive && (
                                <ExtraInfo reminder='Create as a new notebook' >
                                    <Button
                                        style={{margin: '6px'}}
                                        disableElevation
                                        variant='contained'
                                        color='primary'
                                        onClick={this.openAsNewNotebook}
                                        disabled={this.props.app.getAppStatus() != Status.COMPLETED}
                                        endIcon={<OpenInNewIcon />}
                                    >
                                        Create
                                    </Button>
                                </ExtraInfo>
                            )}
						</div>
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
                            <CloseIcon
                                style={{
                                    width: '30px',
                                    height: '30px',
                                    padding: '3px',
                                }}
                            />
                        </IconButton>
					</MuiDialogTitle>
                    <ShadowedDivider />
                    <div style={{display: 'flex', height: 'calc(100% - 60px - 2px'}}>
                        <div style={{width: '150px'}}>
                            <DialogContent style={{padding: '0px'}}>
                                <div style={{padding: '12px 6px'}}>
                                    <Tabs
                                        value={this.state.selectedPanel}
                                        onChange={(event, newValue) => this.safeSetState({selectedPanel: newValue})}
                                        orientation='vertical'
                                        variant='fullWidth'
                                        indicatorColor='primary'
                                        textColor='primary'
                                        style={{minHeight: '24px'}}
                                    >
                                        <Tab
                                            label='SUMMARY'
                                            style={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                            value={Page.SUMMARY}
                                        />
                                        {!this.props.app.interactive && <Tab
                                            label='NOTIFICATIONS'
                                            style={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                            value={Page.NOTIFICATIONS}
                                        />}
                                        {!this.props.app.interactive && <Tab
                                            label='NOTEBOOK'
                                            style={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                            value={Page.NOTEBOOK}
                                        />}
                                        <Tab
                                            label='FILES'
                                            style={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                            value={Page.FILES}
                                        />
                                        <Tab
                                            label='MACHINE'
                                            style={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                            value={Page.MACHINE}
                                        />
                                        {this.props.app.modules.length > 0 && this.props.app.interactive && <Tab
                                            label='TERMINAL'
                                            style={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                            value={Page.TERMINAL}
                                        />}
                                    </Tabs>
                                </div>
                            </DialogContent>
                        </div>
                        <ShadowedDivider orientation='vertical' />
                        <div style={{display: 'flex', flexFlow: 'column', overflow: 'hidden', width: 'calc(100% - 150px)', height: '100%'}}>
                            <DialogContent style={{
                                flexGrow: 1, 
                                overflowY: 'auto',
                                width: '100%',
                                height: '100%',
                                padding: '0px',
                                marginBottom: '0px', // This is because MuiDialogContentText-root is erroneously setting the bottom to 12
                                // lineHeight: 'var(--jp-code-line-height)',
                                fontSize: 'var(--jp-ui-font-size1)',
                                // fontFamily: 'var(--jp-code-font-family)',
                            }}>
                                {this.state.selectedPanel == Page.SUMMARY ? (
                                    <div style={{padding: '20px'}}>
                                        {this.props.app.interactive ? 'Session' : 'Job'} launched at {this.props.app.timestamp.toLocaleTimeString('en-US', { 
                                            hour: 'numeric', minute: 'numeric',
                                        })} on {this.props.app.timestamp.toLocaleDateString('en-US', { 
                                            weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' 
                                        })}
                                        <br/>
                                        {this.props.app.runNum ? (
                                            <>
                                                Run #{this.props.app.runNum + (this.props.app.config.annotation != '' ? ': ' + this.props.app.config.annotation : '')}<br/>
                                            </>
                                        ) : (
                                            <></>
                                        )}
                                        {this.props.app.getTimeElapsed() ? (
                                            <>
                                                Duration: {this.props.app.getTimeElapsed()}<br/>
                                            </>
                                        ) : (
                                            <></>
                                        )}
                                        {this.props.app.getCost() ? (
                                            <>
                                                Estimated cost: {this.props.app.getCost()}<br/>
                                            </>
                                        ) : (
                                            <></>
                                        )}
                                        <br/>
                                        {/* The must have unique key error apparently applies to fragments as well, despite not being able to hold keys */}
                                        {(this.props.app.initializing.messages + this.props.app.uploading.messages + this.props.app.requisitioning.messages + this.props.app.running.messages).split('\n').map((value: string) => (<span style={{whiteSpace: 'pre'}} key={value + i++}>{value}<br /></span>))}
                                    </div>
                                ) : this.state.selectedPanel == Page.NOTIFICATIONS ? (
                                    <div style={{padding: '20px'}}>
                                        <NotificationContent 
                                            getValue={() => this.props.app.config}
                                            saveValue={(config: OptumiConfig) => this.props.app.config = config}
                                            disabled={this.props.app.getAppStatus() == Status.COMPLETED}
                                            openUserDialogTo={this.props.openUserDialogTo}
                                            handleClose={this.handleClose}
                                        />
                                    </div>
                            ) : this.state.selectedPanel == Page.NOTEBOOK ? (
                                    <div style={{overflow: 'hidden', width: '100%', height: '100%'}}>
                                        <div style={{width: '100%', height: 'calc(100% - 68px)', overflow: 'auto'}}>
                                            <Notebook notebook={this.props.app.notebook} />
                                        </div>
                                        <div style={{padding: '6px', width: '100%'}}>
                                                <TextField
                                                    variant='outlined' 
                                                    disabled={this.props.app.modules.length > 0 && this.props.app.modules[0].modStatus == Status.COMPLETED}
                                                    value={this.state.inputLine} 
                                                    onChange={this.handleInputLineChange} 
                                                    onKeyDown={this.handleKeyDown}
                                                    style={{height: '56px', width: '100%'}}
                                                    InputProps={{startAdornment: 
                                                        (<InputAdornment position="start">
                                                            <CodeIcon />
                                                        </InputAdornment>)
                                                    }}
                                                />
                                            </div>
                                    </div>
                                ) : this.state.selectedPanel == Page.FILES ? (
                                    <div style={{padding: '8px'}}>
                                        {this.props.app.interactive && this.props.app.getAppStatus() != Status.COMPLETED ? (
                                            <div style={{padding: '12px'}}>
                                                Files will appear here after your session has completed. Until then, you can upload/download files directly from the session tab.
                                            </div>
                                        ) : (
                                            <OutputFileList app={this.props.app} />
                                        )}
                                    </div>
                                ) : this.state.selectedPanel == Page.MACHINE ? (
                                    <div style={{padding: '14px 8px'}}>
                                         {this.props.app.machine ? (
									        <MachineCapability machine={this.props.app.machine} />
                                        ) : (
                                            <div style={{padding: '6px 12px'}}>
                                                Machine information will appear when the {this.props.app.interactive ? ' session ' : ' job '} starts.
                                            </div>
                                        )}
                                    </div>
                                    
								) : this.state.selectedPanel == Page.TERMINAL && (
                                    <div style={{overflow: 'hidden', width: '100%', height: '100%'}}>
                                        <ScrollableDiv
                                            key='output'
                                            source={Object.assign([], this.props.app.modules[0].output)}
                                            autoScroll={true}
                                        />
                                    </div>
								)}
                            </DialogContent>
                        </div>
                    </div>
				</StyledDialog>
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
}
