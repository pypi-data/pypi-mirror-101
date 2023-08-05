/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { Button, CircularProgress, Dialog, DialogContent, withStyles } from '@material-ui/core';
import { CSSProperties } from '@material-ui/core/styles/withStyles';
import { ArrowBackIos } from '@material-ui/icons';
import * as React from 'react'
import { Global } from '../Global';
import MuiDialogTitle from '@material-ui/core/DialogTitle';
import { ShadowedDivider } from './ShadowedDivider';
import { TextBox } from './TextBox';

import { ServerConnection } from '@jupyterlab/services';
import { DataConnectorIdentity } from '../components/deploy/DataConnectorIdentity'
import { DataService } from '../components/deploy/dataConnectorBrowser/DataConnectorDirListingItemIcon';
import { NotebookPanel } from '@jupyterlab/notebook';
import { DataConnectorUploadConfig } from '../models/DataConnectorUploadConfig';
import { OptumiMetadataTracker } from '../models/OptumiMetadataTracker';
import { UploadConfig } from '../models/UploadConfig';
import ExtraInfo from '../utils/ExtraInfo';

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

const StyledButton = withStyles({
    startIcon: {
        marginRight: '0px',
    },
    iconSizeMedium: {
        '& > *:first-child': {
            fontSize: '12px',
        },
    }
})(Button);

interface IProps {
    onClose?: () => any
    style?: CSSProperties
    dataService: DataService
    iconClass: string
    description: string
    header: string
    downloadPath: string
    getInfo: () => any
    getContents: (waiting: boolean) => JSX.Element
}

interface IState {
    waiting: boolean
    open: boolean
    addSpinning: boolean
    createSpinning: boolean
    name: string
    errorMessage: string
}

const defaultState = {
    waiting: false,
    open: false,
    addSpinning: false,
    createSpinning: false,
    name: '',
    errorMessage: '',
}

export class BaseConnectorPopup extends React.Component<IProps, IState> {
    _isMounted = false;

    static LABEL_WIDTH = '144px'

    constructor(props: IProps) {
        super(props);
        this.state = defaultState;
    }

    private handleClickOpen = () => {
        this.safeSetState({ open: true });
    }

    private handleClose = () => {
        if (!this.state.waiting) {
            if (this.props.onClose) this.props.onClose();
            this.safeSetState(defaultState);
        }
    }

    private nameHasError = (name: string): boolean => {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const upload: UploadConfig = optumi.config.upload;
        const dataConnectors = upload.dataConnectors;
        for (var i = 0; i < dataConnectors.length; i++) {
            if (dataConnectors[i].name === name) return true;
        }
        return false;
    }

    private handleCreate = (add?: boolean) => {
        this.safeSetState({ waiting: true, addSpinning: false, createSpinning: false })
        if (add) {
            setTimeout(() => {
                if (this.state.waiting) this.safeSetState({ addSpinning: true });
            }, 1000)
        } else {
            setTimeout(() => {
                if (this.state.waiting) this.safeSetState({ createSpinning: true });
            }, 1000)
        }
        const settings = ServerConnection.makeSettings();
        const url = settings.baseUrl + 'optumi/add-data-connector';
        const init: RequestInit = {
            method: 'POST',
            body: JSON.stringify({
                dataService: this.props.dataService,
                name: this.state.name,
                info: JSON.stringify(this.props.getInfo()),
            }),
        };
        ServerConnection.makeRequest(
            url,
            init,
            settings
        ).then((response: Response) => {
            Global.handleResponse(response);
        }).then(() => {
            this.safeSetState({ waiting: false, addSpinning: false, createSpinning: false })
            if (add && !this.nameHasError(this.state.name)) {
                const tracker = Global.metadata
                const optumi = tracker.getMetadata()
                var dataConnectors = optumi.config.upload.dataConnectors
                dataConnectors.push(new DataConnectorUploadConfig({
                    name: this.state.name,
                    dataService: this.props.dataService,
                }))
                tracker.setMetadata(optumi)
            }
            // Success
            this.handleClose()
        }, (error: ServerConnection.ResponseError) => {
            error.response.text().then((text: string) => {
                // Show what went wrong
                this.safeSetState({ waiting: false, addSpinning: false, createSpinning: false, errorMessage: text });
            });
        });
    }

    private handleKeyDown = (event: KeyboardEvent) => {
        if (!this.state.open) return;
        if (event.key === 'Enter') this.handleCreate();
        if (event.key === 'Escape') this.handleClose();
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('CreateConnectorPopup (' + new Date().getSeconds() + ')');
        return (
            <div style={Object.assign({}, this.props.style)}>
                <DataConnectorIdentity
                    iconClass={this.props.iconClass}
                    dataService={this.props.dataService}
                    description={this.props.description}
                    handleClick={this.handleClickOpen}
                />
                <StyledDialog
                    disableBackdropClick
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
                            flexGrow: 1,
                            marginLeft: '-6px', // this is to counteract the padding in CreateDataConnector so we can reuse it without messing with it
                        }}>
                            <DataConnectorIdentity
                                iconClass={this.props.iconClass}
                                dataService={this.props.dataService}
                                style={{ zoom: 1.4 }}
                            />
                        </div>
                        <div>
                            <StyledButton
                                disableElevation
                                style={{ margin: '6px', height: '36px' }}
                                variant='outlined'
                                onClick={this.handleClose}
                                disabled={this.state.waiting}
                                startIcon={<ArrowBackIos />}
                            >
                                Back
                            </StyledButton>
                        </div>
                        <div>
                            <Button
                                disableElevation
                                style={{ margin: '6px', height: '36px' }}
                                variant='contained'
                                color='primary'
                                onClick={() => this.handleCreate(false)}
                                disabled={this.state.waiting}
                            >
                                {this.state.waiting && this.state.createSpinning ? <CircularProgress size='1.75em' /> : 'Create'}
                            </Button>
                            <ExtraInfo reminder='Create and add to your notebook' >
                                <Button
                                    disableElevation
                                    style={{ margin: '6px', height: '36px' }}
                                    variant='contained'
                                    color='primary'
                                    onClick={() => this.handleCreate(true)}
                                    disabled={(!(Global.labShell.currentWidget instanceof NotebookPanel) && Global.tracker.currentWidget != null) || this.state.waiting}
                                >
                                    {this.state.waiting && this.state.addSpinning ? <CircularProgress size='1.75em' /> : 'Create + Add'}
                                </Button>
                            </ExtraInfo>
                        </div>
                    </MuiDialogTitle>
                    <ShadowedDivider />
                    <DialogContent style={{ padding: '0px', display: 'flex' }}>
                        <div style={{ padding: '12px', display: 'flex', flexDirection: 'column' }}>
                            <div style={{ margin: '12px 18px 18px 18px' }}>
                                {this.props.header + " Files from this connector will be accessible in your notebook's working directory."}
                            </div>
                            <TextBox<string>
                                getValue={() => this.state.name}
                                saveValue={(value: string) => this.safeSetState({ name: value })}
                                label='Connector Name'
                                helperText='The unique identifier for this connector.'
                                labelWidth={BaseConnectorPopup.LABEL_WIDTH}
                                disabled={this.state.waiting}
                                required
                            />
                            {/* <TextBox<string>
                                getValue={() => this.props.downloadPath}
                                label='Download Path'
                                helperText='We will create a directory with this name and place your files in it.'
                                labelWidth={BaseConnectorPopup.LABEL_WIDTH}
                                disabled
                                required
                            /> */}
                            {this.props.getContents(this.state.waiting)}
                            {this.state.errorMessage && (
                                <div style={{
                                    color: '#f48f8d',
                                    margin: '36px 12px',
                                    wordBreak: 'break-all',
                                    fontSize: '12px',
                                }}>
                                    {this.state.errorMessage}
                                </div>
                            )}
                            <div style={{flexGrow: 1}}/>
                            <div style={{
                                margin: '12px 18px',
                                fontStyle: 'italic',
                                fontSize: '14px',
                                textAlign: 'end',
                                // TODO:Beck how do I do this with the theme
                                color: 'gray'
                            }}>
                                *required fields
                            </div>
                        </div>
                    </DialogContent>
                </StyledDialog>
            </div>
        )
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

    public componentDidMount = () => {
        this._isMounted = true
        document.addEventListener('keydown', this.handleKeyDown, false)
    }

    public componentWillUnmount = () => {
        document.removeEventListener('keydown', this.handleKeyDown, false)
        this._isMounted = false
    }
}
